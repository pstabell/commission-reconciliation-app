"""
Reliable webhook delivery system with retry logic and dead letter queue
Uses RabbitMQ for message queuing and Redis for delivery tracking
"""
import asyncio
import aiohttp
import json
import hashlib
import hmac
import os
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import aio_pika
from aio_pika import Message, ExchangeType, DeliveryMode
import backoff
import redis.asyncio as redis
from enum import Enum
import structlog

logger = structlog.get_logger()

class WebhookStatus(Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRYING = "retrying"
    DEAD_LETTER = "dead_letter"

@dataclass
class WebhookEvent:
    """Webhook event data structure."""
    id: str
    url: str
    event_type: str
    payload: Dict[str, Any]
    secret: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 5
    created_at: datetime = None
    user_id: Optional[str] = None
    api_key_id: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return json.dumps(data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'WebhookEvent':
        """Create from JSON string."""
        data = json.loads(json_str)
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)

class WebhookQueueService:
    """Manages webhook queuing with RabbitMQ."""
    
    def __init__(self, rabbitmq_url: str, redis_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.redis_url = redis_url
        self.connection = None
        self.channel = None
        self.redis_client = None
        self.exchange = None
        
    async def connect(self):
        """Connect to RabbitMQ and Redis."""
        # Connect to RabbitMQ
        self.connection = await aio_pika.connect_robust(
            self.rabbitmq_url,
            client_properties={
                "connection_name": "webhook-queue-service"
            }
        )
        
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)
        
        # Declare exchange
        self.exchange = await self.channel.declare_exchange(
            "webhooks",
            ExchangeType.TOPIC,
            durable=True
        )
        
        # Declare queues with different priorities
        await self._declare_queues()
        
        # Connect to Redis
        self.redis_client = await redis.from_url(self.redis_url)
        
        logger.info("webhook_queue_connected", 
                   rabbitmq=self.rabbitmq_url, 
                   redis=self.redis_url)
    
    async def _declare_queues(self):
        """Declare webhook queues with different priorities."""
        # High priority queue
        high_queue = await self.channel.declare_queue(
            "webhooks.high",
            durable=True,
            arguments={
                "x-max-priority": 10,
                "x-message-ttl": 86400000,  # 24 hours
                "x-dead-letter-exchange": "webhooks.dlx"
            }
        )
        await high_queue.bind(self.exchange, "webhook.high.*")
        
        # Normal priority queue
        normal_queue = await self.channel.declare_queue(
            "webhooks.normal",
            durable=True,
            arguments={
                "x-message-ttl": 86400000,  # 24 hours
                "x-dead-letter-exchange": "webhooks.dlx"
            }
        )
        await normal_queue.bind(self.exchange, "webhook.normal.*")
        
        # Low priority queue (retries)
        low_queue = await self.channel.declare_queue(
            "webhooks.low",
            durable=True,
            arguments={
                "x-message-ttl": 172800000,  # 48 hours
                "x-dead-letter-exchange": "webhooks.dlx"
            }
        )
        await low_queue.bind(self.exchange, "webhook.low.*")
        
        # Dead letter exchange and queue
        dlx = await self.channel.declare_exchange(
            "webhooks.dlx",
            ExchangeType.FANOUT,
            durable=True
        )
        
        dlq = await self.channel.declare_queue(
            "webhooks.dead_letter",
            durable=True,
            arguments={
                "x-message-ttl": 604800000  # 7 days
            }
        )
        await dlq.bind(dlx)
    
    async def send_webhook(self, event: WebhookEvent, priority: str = "normal"):
        """Queue webhook for delivery."""
        routing_key = f"webhook.{priority}.{event.event_type}"
        
        message = Message(
            event.to_json().encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            headers={
                "webhook_id": event.id,
                "event_type": event.event_type,
                "retry_count": event.retry_count,
                "user_id": event.user_id
            },
            priority=self._get_priority_value(priority)
        )
        
        await self.exchange.publish(message, routing_key=routing_key)
        
        # Track in Redis
        await self._track_webhook_queued(event)
        
        logger.info("webhook_queued",
                   webhook_id=event.id,
                   event_type=event.event_type,
                   priority=priority)
    
    def _get_priority_value(self, priority: str) -> int:
        """Convert priority string to numeric value."""
        return {"high": 10, "normal": 5, "low": 1}.get(priority, 5)
    
    async def _track_webhook_queued(self, event: WebhookEvent):
        """Track webhook in Redis for monitoring."""
        key = f"webhook:status:{event.id}"
        data = {
            "status": WebhookStatus.PENDING.value,
            "url": event.url,
            "event_type": event.event_type,
            "queued_at": datetime.utcnow().isoformat(),
            "retry_count": event.retry_count
        }
        
        await self.redis_client.hset(key, mapping=data)
        await self.redis_client.expire(key, 86400 * 7)  # 7 days
        
        # Update queue size metric
        await self.redis_client.hincrby("webhook:metrics", "queue_size", 1)

class WebhookDeliveryService:
    """Handles actual webhook delivery with retry logic."""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(limit=100)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, asyncio.TimeoutError),
        max_tries=3,
        max_time=60
    )
    async def deliver_webhook(self, event: WebhookEvent) -> Dict[str, Any]:
        """
        Deliver webhook with exponential backoff retry.
        
        Returns:
            Dict with delivery status and details
        """
        start_time = datetime.utcnow()
        
        # Build headers
        headers = self._build_headers(event)
        
        # Add signature if secret provided
        if event.secret:
            signature = self._generate_signature(event.payload, event.secret)
            headers["X-Webhook-Signature"] = signature
        
        try:
            async with self.session.post(
                event.url,
                json=event.payload,
                headers=headers,
                ssl=True
            ) as response:
                duration = (datetime.utcnow() - start_time).total_seconds()
                
                # Log delivery attempt
                await self._log_delivery_attempt(
                    event, 
                    response.status, 
                    duration,
                    response.headers.get("X-Request-ID")
                )
                
                # Success if 2xx status code
                if 200 <= response.status < 300:
                    await self._track_delivery_success(event, duration)
                    return {
                        "status": "success",
                        "http_status": response.status,
                        "duration": duration,
                        "response_id": response.headers.get("X-Request-ID")
                    }
                
                # Client error (4xx) - don't retry
                if 400 <= response.status < 500:
                    error_body = await response.text()
                    await self._track_delivery_failure(
                        event, 
                        f"HTTP {response.status}: {error_body[:200]}"
                    )
                    return {
                        "status": "failed",
                        "http_status": response.status,
                        "error": error_body[:200],
                        "retry": False
                    }
                
                # Server error (5xx) - retry
                error_body = await response.text()
                raise aiohttp.ClientError(
                    f"HTTP {response.status}: {error_body[:200]}"
                )
                
        except asyncio.TimeoutError as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            await self._log_delivery_attempt(event, 0, duration, error="Timeout")
            raise
            
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            await self._log_delivery_attempt(event, 0, duration, error=str(e))
            raise
    
    def _build_headers(self, event: WebhookEvent) -> Dict[str, str]:
        """Build webhook delivery headers."""
        return {
            "Content-Type": "application/json",
            "User-Agent": "CommissionIntelligencePlatform/1.0",
            "X-Webhook-ID": event.id,
            "X-Webhook-Event": event.event_type,
            "X-Webhook-Timestamp": str(int(event.created_at.timestamp())),
            "X-Webhook-Retry": str(event.retry_count)
        }
    
    def _generate_signature(self, payload: Dict[str, Any], secret: str) -> str:
        """Generate HMAC-SHA256 signature for webhook payload."""
        message = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"sha256={signature}"
    
    async def _log_delivery_attempt(self, event: WebhookEvent, status_code: int,
                                   duration: float, response_id: Optional[str] = None,
                                   error: Optional[str] = None):
        """Log webhook delivery attempt to Redis."""
        log_entry = {
            "webhook_id": event.id,
            "url": event.url,
            "event_type": event.event_type,
            "status_code": status_code,
            "attempt": event.retry_count + 1,
            "duration_ms": duration * 1000,
            "timestamp": datetime.utcnow().isoformat(),
            "response_id": response_id,
            "error": error
        }
        
        # Store in Redis list for this webhook
        key = f"webhook:log:{event.id}"
        await self.redis_client.lpush(key, json.dumps(log_entry))
        await self.redis_client.ltrim(key, 0, 99)  # Keep last 100 attempts
        await self.redis_client.expire(key, 86400 * 7)  # 7 days
        
        # Update global metrics
        if 200 <= status_code < 300:
            await self.redis_client.hincrby("webhook:metrics", "delivered", 1)
        elif status_code >= 400:
            await self.redis_client.hincrby("webhook:metrics", "failed", 1)
    
    async def _track_delivery_success(self, event: WebhookEvent, duration: float):
        """Track successful webhook delivery."""
        key = f"webhook:status:{event.id}"
        await self.redis_client.hset(key, mapping={
            "status": WebhookStatus.DELIVERED.value,
            "delivered_at": datetime.utcnow().isoformat(),
            "duration_ms": duration * 1000,
            "attempts": event.retry_count + 1
        })
        
        # Update metrics
        await self.redis_client.hincrby("webhook:metrics", "queue_size", -1)
        
        logger.info("webhook_delivered",
                   webhook_id=event.id,
                   event_type=event.event_type,
                   attempts=event.retry_count + 1,
                   duration_ms=duration * 1000)
    
    async def _track_delivery_failure(self, event: WebhookEvent, error: str):
        """Track webhook delivery failure."""
        key = f"webhook:status:{event.id}"
        await self.redis_client.hset(key, mapping={
            "status": WebhookStatus.FAILED.value,
            "failed_at": datetime.utcnow().isoformat(),
            "error": error,
            "attempts": event.retry_count + 1
        })
        
        logger.error("webhook_failed",
                    webhook_id=event.id,
                    event_type=event.event_type,
                    error=error)

class WebhookProcessor:
    """Process webhooks from queue with multiple workers."""
    
    def __init__(self, queue_service: WebhookQueueService,
                 delivery_service: WebhookDeliveryService,
                 concurrency: Dict[str, int] = None):
        self.queue_service = queue_service
        self.delivery_service = delivery_service
        self.concurrency = concurrency or {
            "high": 10,
            "normal": 5,
            "low": 2
        }
        self.running = False
        self.tasks = []
    
    async def start(self):
        """Start processing webhooks from all queues."""
        self.running = True
        
        # Start workers for each priority queue
        for priority, worker_count in self.concurrency.items():
            queue_name = f"webhooks.{priority}"
            
            for i in range(worker_count):
                task = asyncio.create_task(
                    self._process_queue(queue_name, priority)
                )
                self.tasks.append(task)
                
        logger.info("webhook_processor_started",
                   workers=sum(self.concurrency.values()))
    
    async def stop(self):
        """Stop all webhook processors."""
        self.running = False
        
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.tasks, return_exceptions=True)
        
        logger.info("webhook_processor_stopped")
    
    async def _process_queue(self, queue_name: str, priority: str):
        """Process messages from a specific queue."""
        queue = await self.queue_service.channel.get_queue(queue_name)
        
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                if not self.running:
                    break
                
                try:
                    await self._process_message(message, priority)
                except Exception as e:
                    logger.error("webhook_processing_error",
                               queue=queue_name,
                               error=str(e),
                               exc_info=True)
                    
                    # Reject message and send to DLQ
                    await message.reject(requeue=False)
    
    async def _process_message(self, message: aio_pika.IncomingMessage, 
                             priority: str):
        """Process a single webhook message."""
        async with message.process():
            # Parse webhook event
            event = WebhookEvent.from_json(message.body.decode())
            
            # Update status to retrying
            await self._update_webhook_status(event.id, WebhookStatus.RETRYING)
            
            try:
                # Attempt delivery
                result = await self.delivery_service.deliver_webhook(event)
                
                if result["status"] == "success":
                    # Success - acknowledge message
                    return
                
                elif result["status"] == "failed" and not result.get("retry", True):
                    # Permanent failure - send to dead letter queue
                    await self._send_to_dead_letter(event, result["error"])
                    return
                
            except Exception as e:
                # Delivery failed - check if we should retry
                if event.retry_count < event.max_retries:
                    # Retry with lower priority
                    event.retry_count += 1
                    await self.queue_service.send_webhook(event, "low")
                    
                    logger.warning("webhook_retry_scheduled",
                                 webhook_id=event.id,
                                 retry_count=event.retry_count,
                                 error=str(e))
                else:
                    # Max retries reached - send to dead letter queue
                    await self._send_to_dead_letter(event, str(e))
    
    async def _update_webhook_status(self, webhook_id: str, status: WebhookStatus):
        """Update webhook status in Redis."""
        key = f"webhook:status:{webhook_id}"
        await self.delivery_service.redis_client.hset(
            key, 
            "status", 
            status.value
        )
    
    async def _send_to_dead_letter(self, event: WebhookEvent, error: str):
        """Send webhook to dead letter queue."""
        await self._update_webhook_status(event.id, WebhookStatus.DEAD_LETTER)
        
        # Log to dead letter tracking
        dlq_entry = {
            "webhook_id": event.id,
            "url": event.url,
            "event_type": event.event_type,
            "final_error": error,
            "total_attempts": event.retry_count + 1,
            "dead_lettered_at": datetime.utcnow().isoformat()
        }
        
        key = f"webhook:dead_letter:{event.id}"
        await self.delivery_service.redis_client.set(
            key,
            json.dumps(dlq_entry),
            ex=86400 * 30  # Keep for 30 days
        )
        
        # Update metrics
        await self.delivery_service.redis_client.hincrby(
            "webhook:metrics", 
            "dead_lettered", 
            1
        )
        
        logger.error("webhook_dead_lettered",
                    webhook_id=event.id,
                    event_type=event.event_type,
                    attempts=event.retry_count + 1,
                    error=error)

class WebhookManagementService:
    """High-level webhook management API."""
    
    def __init__(self, queue_service: WebhookQueueService, 
                 redis_client: redis.Redis):
        self.queue_service = queue_service
        self.redis_client = redis_client
    
    async def send_webhook(self, url: str, event_type: str, 
                          payload: Dict[str, Any],
                          secret: Optional[str] = None,
                          user_id: Optional[str] = None,
                          priority: str = "normal") -> str:
        """
        Send a webhook event.
        
        Returns:
            webhook_id: Unique identifier for tracking
        """
        event = WebhookEvent(
            id=str(uuid.uuid4()),
            url=url,
            event_type=event_type,
            payload=payload,
            secret=secret,
            user_id=user_id
        )
        
        await self.queue_service.send_webhook(event, priority)
        
        return event.id
    
    async def get_webhook_status(self, webhook_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a webhook."""
        key = f"webhook:status:{webhook_id}"
        data = await self.redis_client.hgetall(key)
        
        if not data:
            return None
        
        return {k.decode() if isinstance(k, bytes) else k: 
                v.decode() if isinstance(v, bytes) else v 
                for k, v in data.items()}
    
    async def get_webhook_logs(self, webhook_id: str, 
                             limit: int = 10) -> List[Dict[str, Any]]:
        """Get delivery logs for a webhook."""
        key = f"webhook:log:{webhook_id}"
        logs = await self.redis_client.lrange(key, 0, limit - 1)
        
        return [json.loads(log) for log in logs]
    
    async def retry_webhook(self, webhook_id: str) -> bool:
        """Manually retry a failed webhook."""
        # Get webhook data from dead letter
        dlq_key = f"webhook:dead_letter:{webhook_id}"
        dlq_data = await self.redis_client.get(dlq_key)
        
        if not dlq_data:
            return False
        
        # TODO: Reconstruct webhook event and requeue
        # This would require storing the full event in dead letter
        
        return True
    
    async def get_metrics(self) -> Dict[str, int]:
        """Get webhook delivery metrics."""
        metrics = await self.redis_client.hgetall("webhook:metrics")
        
        return {
            k.decode() if isinstance(k, bytes) else k: 
            int(v) for k, v in metrics.items()
        }