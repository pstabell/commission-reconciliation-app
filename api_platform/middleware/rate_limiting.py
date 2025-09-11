"""
Advanced rate limiting middleware with multiple strategies
Supports sliding window, distributed rate limiting, and plan-based limits
"""
import time
import json
import os
from typing import Dict, Tuple, Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import redis
from datetime import datetime, timedelta
import asyncio
from functools import wraps

# Redis connection for rate limiting
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
    password=os.getenv("REDIS_PASSWORD")
)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Advanced rate limiting with multiple strategies."""
    
    def __init__(self, app, redis_client: redis.Redis = None):
        super().__init__(app)
        self.redis = redis_client or globals()['redis_client']
        
        # Rate limit configurations by plan
        self.rate_limits = {
            "free": {
                "requests_per_hour": 100,
                "requests_per_day": 1000,
                "concurrent_requests": 2,
                "burst_size": 10
            },
            "starter": {
                "requests_per_hour": 1000,
                "requests_per_day": 10000,
                "concurrent_requests": 5,
                "burst_size": 50
            },
            "professional": {
                "requests_per_hour": 10000,
                "requests_per_day": 100000,
                "concurrent_requests": 20,
                "burst_size": 200
            },
            "enterprise": {
                "requests_per_hour": 100000,
                "requests_per_day": 1000000,
                "concurrent_requests": 100,
                "burst_size": 1000
            }
        }
        
        # Endpoint-specific rate limits
        self.endpoint_limits = {
            "/v1/commissions/calculate": {"requests_per_minute": 60},
            "/v1/policies/batch": {"requests_per_minute": 10},
            "/v1/webhooks": {"requests_per_hour": 100}
        }
    
    async def dispatch(self, request: Request, call_next):
        """Apply rate limiting to incoming requests."""
        # Extract API key from request
        api_key = self._extract_api_key(request)
        if not api_key:
            return await call_next(request)
        
        # Get user plan from cache or database
        plan = await self._get_user_plan(api_key)
        
        # Check concurrent request limit
        concurrent_ok = await self._check_concurrent_limit(api_key, plan)
        if not concurrent_ok:
            raise HTTPException(
                status_code=429,
                detail="Too many concurrent requests",
                headers={"Retry-After": "1"}
            )
        
        try:
            # Check rate limits
            rate_limit_result = await self._check_rate_limits(api_key, plan, request.url.path)
            
            if not rate_limit_result["allowed"]:
                # Build rate limit headers
                headers = {
                    "X-RateLimit-Limit": str(rate_limit_result["limit"]),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(rate_limit_result["reset"]),
                    "Retry-After": str(rate_limit_result["retry_after"])
                }
                
                raise HTTPException(
                    status_code=429,
                    detail=rate_limit_result.get("message", "Rate limit exceeded"),
                    headers=headers
                )
            
            # Process request and add rate limit headers
            response = await call_next(request)
            
            # Add rate limit headers to successful response
            for key, value in rate_limit_result["headers"].items():
                response.headers[key] = str(value)
            
            return response
            
        finally:
            # Release concurrent request slot
            await self._release_concurrent_slot(api_key)
    
    def _extract_api_key(self, request: Request) -> Optional[str]:
        """Extract API key from Authorization header."""
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:]
        return None
    
    async def _get_user_plan(self, api_key: str) -> str:
        """Get user plan from cache or database."""
        # Check cache first
        cache_key = f"user_plan:{api_key}"
        cached_plan = self.redis.get(cache_key)
        if cached_plan:
            return cached_plan
        
        # TODO: Fetch from database
        # For now, return default plan
        plan = "starter"
        
        # Cache for 5 minutes
        self.redis.setex(cache_key, 300, plan)
        return plan
    
    async def _check_concurrent_limit(self, api_key: str, plan: str) -> bool:
        """Check and acquire concurrent request slot."""
        limit = self.rate_limits[plan]["concurrent_requests"]
        key = f"concurrent:{api_key}"
        
        # Use Redis INCR with pipeline for atomicity
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, 60)  # Auto-cleanup after 1 minute
        results = pipe.execute()
        
        current_count = results[0]
        
        if current_count > limit:
            # Release the slot we just took
            self.redis.decr(key)
            return False
        
        return True
    
    async def _release_concurrent_slot(self, api_key: str):
        """Release concurrent request slot."""
        key = f"concurrent:{api_key}"
        self.redis.decr(key)
    
    async def _check_rate_limits(self, api_key: str, plan: str, endpoint: str) -> Dict:
        """Check multiple rate limits and return detailed result."""
        plan_limits = self.rate_limits[plan]
        now = time.time()
        
        # Check hourly limit
        hourly_result = await self._check_sliding_window(
            f"rate_hour:{api_key}",
            plan_limits["requests_per_hour"],
            3600,
            now
        )
        
        if not hourly_result["allowed"]:
            return {
                "allowed": False,
                "limit": plan_limits["requests_per_hour"],
                "reset": hourly_result["reset"],
                "retry_after": hourly_result["retry_after"],
                "message": "Hourly rate limit exceeded",
                "headers": self._build_headers(hourly_result, plan_limits["requests_per_hour"])
            }
        
        # Check daily limit
        daily_result = await self._check_sliding_window(
            f"rate_day:{api_key}",
            plan_limits["requests_per_day"],
            86400,
            now
        )
        
        if not daily_result["allowed"]:
            return {
                "allowed": False,
                "limit": plan_limits["requests_per_day"],
                "reset": daily_result["reset"],
                "retry_after": daily_result["retry_after"],
                "message": "Daily rate limit exceeded",
                "headers": self._build_headers(daily_result, plan_limits["requests_per_day"])
            }
        
        # Check endpoint-specific limits
        endpoint_limit = self.endpoint_limits.get(endpoint)
        if endpoint_limit:
            endpoint_result = await self._check_sliding_window(
                f"rate_endpoint:{api_key}:{endpoint}",
                endpoint_limit.get("requests_per_minute", float('inf')),
                60,
                now
            )
            
            if not endpoint_result["allowed"]:
                return {
                    "allowed": False,
                    "limit": endpoint_limit["requests_per_minute"],
                    "reset": endpoint_result["reset"],
                    "retry_after": endpoint_result["retry_after"],
                    "message": f"Endpoint rate limit exceeded for {endpoint}",
                    "headers": self._build_headers(endpoint_result, endpoint_limit["requests_per_minute"])
                }
        
        # All checks passed - return the most restrictive remaining limit
        return {
            "allowed": True,
            "headers": self._build_headers(hourly_result, plan_limits["requests_per_hour"])
        }
    
    async def _check_sliding_window(self, key: str, limit: int, window: int, 
                                  now: float) -> Dict:
        """Check rate limit using sliding window algorithm."""
        # Use Redis sorted set for sliding window
        pipe = self.redis.pipeline()
        
        # Remove old entries outside the window
        pipe.zremrangebyscore(key, 0, now - window)
        
        # Count requests in current window
        pipe.zcard(key)
        
        # Get oldest request timestamp for retry-after calculation
        pipe.zrange(key, 0, 0, withscores=True)
        
        results = pipe.execute()
        current_count = results[1]
        oldest_request = results[2]
        
        if current_count >= limit:
            # Calculate retry-after based on oldest request
            if oldest_request:
                oldest_timestamp = oldest_request[0][1]
                retry_after = int(oldest_timestamp + window - now)
                reset_time = int(oldest_timestamp + window)
            else:
                retry_after = window
                reset_time = int(now + window)
            
            return {
                "allowed": False,
                "remaining": 0,
                "reset": reset_time,
                "retry_after": max(1, retry_after)
            }
        
        # Add current request
        self.redis.zadd(key, {str(now): now})
        self.redis.expire(key, window + 1)
        
        # Calculate reset time
        if oldest_request:
            reset_time = int(oldest_request[0][1] + window)
        else:
            reset_time = int(now + window)
        
        return {
            "allowed": True,
            "remaining": limit - current_count - 1,
            "reset": reset_time,
            "retry_after": 0
        }
    
    def _build_headers(self, result: Dict, limit: int) -> Dict[str, str]:
        """Build rate limit headers for response."""
        return {
            "X-RateLimit-Limit": str(limit),
            "X-RateLimit-Remaining": str(result.get("remaining", 0)),
            "X-RateLimit-Reset": str(result.get("reset", 0)),
            "X-RateLimit-Policy": "sliding-window"
        }

# Distributed rate limiter for multiple API servers
class DistributedRateLimiter:
    """Rate limiter that works across multiple API servers using Redis."""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        
        # Lua script for atomic rate limit check
        self.lua_script = """
        local key = KEYS[1]
        local limit = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local current_time = tonumber(ARGV[3])
        local identifier = ARGV[4]
        
        -- Clean old entries
        local trim_time = current_time - window
        redis.call('ZREMRANGEBYSCORE', key, 0, trim_time)
        
        -- Count current requests
        local current_count = redis.call('ZCARD', key)
        
        -- Check if limit exceeded
        if current_count >= limit then
            -- Get oldest entry for retry-after calculation
            local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
            if oldest[1] then
                local reset_time = oldest[2] + window
                return {0, 0, reset_time}
            else
                return {0, 0, current_time + window}
            end
        end
        
        -- Add new request
        redis.call('ZADD', key, current_time, identifier)
        redis.call('EXPIRE', key, window + 1)
        
        -- Calculate reset time
        local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
        local reset_time = oldest[2] and (oldest[2] + window) or (current_time + window)
        
        return {1, limit - current_count - 1, reset_time}
        """
        
        # Load script into Redis
        self.script_sha = self.redis.script_load(self.lua_script)
    
    def check_limit(self, key: str, limit: int, window: int) -> Tuple[bool, int, int]:
        """
        Check if request is allowed using distributed rate limiting.
        
        Returns:
            tuple: (allowed, remaining, reset_timestamp)
        """
        current_time = time.time()
        identifier = f"{current_time}:{os.getpid()}:{id(self)}"
        
        try:
            result = self.redis.evalsha(
                self.script_sha,
                1,
                key,
                limit,
                window,
                current_time,
                identifier
            )
            
            return bool(result[0]), int(result[1]), int(result[2])
            
        except redis.NoScriptError:
            # Script was flushed, reload it
            self.script_sha = self.redis.script_load(self.lua_script)
            return self.check_limit(key, limit, window)

# Token bucket rate limiter for burst handling
class TokenBucketRateLimiter:
    """Token bucket algorithm for handling burst traffic."""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        
        self.lua_script = """
        local key = KEYS[1]
        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local current_time = tonumber(ARGV[3])
        local requested_tokens = tonumber(ARGV[4] or 1)
        
        -- Get current bucket state
        local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
        local tokens = tonumber(bucket[1] or capacity)
        local last_refill = tonumber(bucket[2] or current_time)
        
        -- Calculate new tokens based on time elapsed
        local elapsed = current_time - last_refill
        local new_tokens = math.min(capacity, tokens + (elapsed * refill_rate))
        
        -- Check if we have enough tokens
        if new_tokens >= requested_tokens then
            -- Consume tokens
            new_tokens = new_tokens - requested_tokens
            redis.call('HMSET', key, 'tokens', new_tokens, 'last_refill', current_time)
            redis.call('EXPIRE', key, 3600)
            return {1, new_tokens}
        else
            -- Not enough tokens
            return {0, new_tokens}
        end
        """
        
        self.script_sha = self.redis.script_load(self.lua_script)
    
    def consume_tokens(self, key: str, capacity: int, refill_rate: float, 
                      tokens_requested: int = 1) -> Tuple[bool, float]:
        """
        Try to consume tokens from the bucket.
        
        Args:
            key: Redis key for the bucket
            capacity: Maximum tokens in bucket
            refill_rate: Tokens refilled per second
            tokens_requested: Number of tokens to consume
            
        Returns:
            tuple: (allowed, remaining_tokens)
        """
        try:
            result = self.redis.evalsha(
                self.script_sha,
                1,
                key,
                capacity,
                refill_rate,
                time.time(),
                tokens_requested
            )
            
            return bool(result[0]), float(result[1])
            
        except redis.NoScriptError:
            self.script_sha = self.redis.script_load(self.lua_script)
            return self.consume_tokens(key, capacity, refill_rate, tokens_requested)

# Rate limit decorator for specific endpoints
def rate_limit(requests_per_minute: int = 60):
    """Decorator to apply rate limiting to specific endpoints."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request from args
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request:
                # Apply rate limiting logic
                limiter = DistributedRateLimiter(redis_client)
                
                # Get API key or IP for rate limiting
                api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
                if not api_key:
                    api_key = request.client.host
                
                key = f"endpoint_limit:{func.__name__}:{api_key}"
                allowed, remaining, reset = limiter.check_limit(
                    key,
                    requests_per_minute,
                    60
                )
                
                if not allowed:
                    raise HTTPException(
                        status_code=429,
                        detail="Rate limit exceeded for this endpoint",
                        headers={
                            "X-RateLimit-Limit": str(requests_per_minute),
                            "X-RateLimit-Remaining": "0",
                            "X-RateLimit-Reset": str(reset),
                            "Retry-After": str(max(1, reset - int(time.time())))
                        }
                    )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator

# Initialize global instances
distributed_limiter = DistributedRateLimiter(redis_client)
token_bucket_limiter = TokenBucketRateLimiter(redis_client)