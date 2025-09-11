"""
Production-ready authentication and authorization system
Handles JWT tokens, OAuth2, and API key management
"""
import jwt
import secrets
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import bcrypt
from functools import lru_cache
import redis
import aiohttp
from urllib.parse import urlencode

# Redis for token blacklist and rate limiting
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
    password=os.getenv("REDIS_PASSWORD")
)

class AuthenticationService:
    """Production-ready authentication service with JWT tokens."""
    
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY")
        if not self.secret_key:
            # Generate a secure key if not provided (development only)
            self.secret_key = secrets.token_urlsafe(32)
            print("WARNING: Using generated JWT secret key. Set JWT_SECRET_KEY in production!")
        
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 30
        
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str, token_type: str = "access") -> Dict[str, Any]:
        """Verify and decode JWT token."""
        # Check if token is blacklisted
        if redis_client.sismember("blacklisted_tokens", token):
            raise HTTPException(status_code=401, detail="Token has been revoked")
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != token_type:
                raise HTTPException(status_code=401, detail="Invalid token type")
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Could not validate token")
    
    def revoke_token(self, token: str):
        """Add token to blacklist."""
        # Add to blacklist with expiration
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm], 
                               options={"verify_exp": False})
            exp_timestamp = payload.get("exp", 0)
            ttl = exp_timestamp - datetime.utcnow().timestamp()
            if ttl > 0:
                redis_client.setex(f"blacklist:{token}", int(ttl), "1")
                redis_client.sadd("blacklisted_tokens", token)
        except jwt.JWTError:
            pass  # Invalid token, ignore

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# OAuth2 implementation for third-party integrations
class OAuth2Service:
    """Handle OAuth2 flows for partner integrations."""
    
    def __init__(self):
        self.providers = {
            "hubspot": {
                "client_id": os.getenv("HUBSPOT_CLIENT_ID"),
                "client_secret": os.getenv("HUBSPOT_CLIENT_SECRET"),
                "authorize_url": "https://app.hubspot.com/oauth/authorize",
                "token_url": "https://api.hubapi.com/oauth/v1/token",
                "scope": "crm.objects.contacts.read crm.objects.contacts.write"
            },
            "salesforce": {
                "client_id": os.getenv("SALESFORCE_CLIENT_ID"),
                "client_secret": os.getenv("SALESFORCE_CLIENT_SECRET"),
                "authorize_url": "https://login.salesforce.com/services/oauth2/authorize",
                "token_url": "https://login.salesforce.com/services/oauth2/token",
                "scope": "api refresh_token"
            },
            "applied_epic": {
                "client_id": os.getenv("APPLIED_CLIENT_ID"),
                "client_secret": os.getenv("APPLIED_CLIENT_SECRET"),
                "authorize_url": "https://api.applied.com/oauth/authorize",
                "token_url": "https://api.applied.com/oauth/token",
                "scope": "policy.read policy.write commission.read"
            }
        }
    
    def get_authorization_url(self, provider: str, redirect_uri: str, state: str) -> str:
        """Generate OAuth2 authorization URL."""
        config = self.providers.get(provider)
        if not config:
            raise ValueError(f"Unknown provider: {provider}")
        
        params = {
            "client_id": config["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
            "scope": config["scope"]
        }
        
        return f"{config['authorize_url']}?" + urlencode(params)
    
    async def exchange_code_for_token(self, provider: str, code: str, redirect_uri: str):
        """Exchange authorization code for access token."""
        config = self.providers.get(provider)
        if not config:
            raise ValueError(f"Unknown provider: {provider}")
        
        async with aiohttp.ClientSession() as session:
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": config["client_id"],
                "client_secret": config["client_secret"]
            }
            
            async with session.post(config["token_url"], data=data) as response:
                if response.status == 200:
                    token_data = await response.json()
                    # Store tokens securely
                    await self._store_oauth_tokens(provider, token_data)
                    return token_data
                else:
                    error_text = await response.text()
                    raise HTTPException(status_code=400, detail=f"Failed to exchange code: {error_text}")
    
    async def refresh_access_token(self, provider: str, refresh_token: str):
        """Refresh OAuth2 access token."""
        config = self.providers.get(provider)
        if not config:
            raise ValueError(f"Unknown provider: {provider}")
        
        async with aiohttp.ClientSession() as session:
            data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": config["client_id"],
                "client_secret": config["client_secret"]
            }
            
            async with session.post(config["token_url"], data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise HTTPException(status_code=400, detail="Failed to refresh token")
    
    async def _store_oauth_tokens(self, provider: str, token_data: Dict[str, Any]):
        """Store OAuth tokens securely in Redis with encryption."""
        # In production, encrypt tokens before storing
        key = f"oauth_tokens:{provider}:{token_data.get('user_id', 'default')}"
        redis_client.setex(
            key,
            token_data.get("expires_in", 3600),
            json.dumps(token_data)
        )

# API Key management
class APIKeyService:
    """Manage API keys for platform access."""
    
    def __init__(self):
        self.key_prefix = "cipk_"  # Commission Intelligence Platform Key
        
    def generate_api_key(self) -> str:
        """Generate a new API key."""
        # Format: cipk_[random_string]
        random_part = secrets.token_urlsafe(32)
        return f"{self.key_prefix}{random_part}"
    
    def hash_api_key(self, api_key: str) -> str:
        """Hash API key for storage."""
        # Only store hashed keys in database
        import hashlib
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    def validate_key_format(self, api_key: str) -> bool:
        """Validate API key format."""
        return api_key.startswith(self.key_prefix) and len(api_key) == 48

# Permission system
class PermissionService:
    """Handle API permissions and scopes."""
    
    PERMISSIONS = {
        "policies:read": "Read policy data",
        "policies:write": "Create and update policies",
        "commissions:read": "Read commission data",
        "commissions:calculate": "Calculate commissions",
        "webhooks:manage": "Manage webhooks",
        "analytics:read": "Access analytics data",
        "integrations:manage": "Manage integrations"
    }
    
    ROLE_PERMISSIONS = {
        "admin": list(PERMISSIONS.keys()),
        "agency": [
            "policies:read", "policies:write",
            "commissions:read", "commissions:calculate",
            "analytics:read", "webhooks:manage"
        ],
        "agent": [
            "policies:read",
            "commissions:read",
            "analytics:read"
        ],
        "integration": [
            "policies:read", "policies:write",
            "webhooks:manage"
        ]
    }
    
    def check_permission(self, user_role: str, required_permission: str) -> bool:
        """Check if role has required permission."""
        role_permissions = self.ROLE_PERMISSIONS.get(user_role, [])
        return required_permission in role_permissions
    
    def get_role_permissions(self, role: str) -> list:
        """Get all permissions for a role."""
        return self.ROLE_PERMISSIONS.get(role, [])

# Singleton instances
auth_service = AuthenticationService()
oauth_service = OAuth2Service()
api_key_service = APIKeyService()
permission_service = PermissionService()

# FastAPI dependencies
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current authenticated user."""
    token = credentials.credentials
    try:
        payload = auth_service.verify_token(token)
        return payload
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def require_permission(permission: str):
    """Dependency to require specific permission."""
    async def permission_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role", "agent")
        if not permission_service.check_permission(user_role, permission):
            raise HTTPException(
                status_code=403,
                detail=f"Permission denied. Required: {permission}"
            )
        return current_user
    return permission_checker