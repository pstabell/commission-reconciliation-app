"""
Comprehensive monitoring and observability for Commission Intelligence Platform
Includes Prometheus metrics, OpenTelemetry tracing, and structured logging
"""
import os
import time
import json
from typing import Optional, Dict, Any
from datetime import datetime
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.core import CollectorRegistry
from opentelemetry import trace, metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import asyncio
import aiohttp

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create custom registry for Prometheus metrics
registry = CollectorRegistry()

# API Metrics
api_requests_total = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status', 'plan'],
    registry=registry
)

api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
    registry=registry
)

active_connections = Gauge(
    'active_api_connections',
    'Number of active API connections',
    registry=registry
)

# Commission Metrics
commission_calculations_total = Counter(
    'commission_calculations_total',
    'Total commission calculations',
    ['policy_type', 'transaction_type', 'status'],
    registry=registry
)

commission_amount_histogram = Histogram(
    'commission_amount_dollars',
    'Commission amounts in dollars',
    ['policy_type', 'transaction_type'],
    buckets=[10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000],
    registry=registry
)

# Webhook Metrics
webhook_deliveries_total = Counter(
    'webhook_deliveries_total',
    'Total webhook delivery attempts',
    ['event_type', 'status', 'retry_count'],
    registry=registry
)

webhook_delivery_duration = Histogram(
    'webhook_delivery_duration_seconds',
    'Webhook delivery duration',
    ['event_type', 'status'],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
    registry=registry
)

webhook_queue_size = Gauge(
    'webhook_queue_size',
    'Number of webhooks in queue',
    ['priority'],
    registry=registry
)

# Integration Metrics
integration_sync_total = Counter(
    'integration_sync_total',
    'Total integration sync operations',
    ['integration', 'direction', 'status'],
    registry=registry
)

integration_sync_duration = Histogram(
    'integration_sync_duration_seconds',
    'Integration sync duration',
    ['integration', 'direction'],
    buckets=[1.0, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0],
    registry=registry
)

# Database Metrics
database_queries_total = Counter(
    'database_queries_total',
    'Total database queries',
    ['operation', 'table', 'status'],
    registry=registry
)

database_query_duration = Histogram(
    'database_query_duration_seconds',
    'Database query duration',
    ['operation', 'table'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
    registry=registry
)

# Rate Limit Metrics
rate_limit_exceeded_total = Counter(
    'rate_limit_exceeded_total',
    'Total rate limit exceeded events',
    ['api_key_prefix', 'limit_type'],
    registry=registry
)

class MonitoringService:
    """Centralized monitoring and observability service."""
    
    def __init__(self, service_name: str = "commission-intelligence-api"):
        self.service_name = service_name
        
        # Initialize OpenTelemetry tracing
        resource = Resource.create({
            ResourceAttributes.SERVICE_NAME: service_name,
            ResourceAttributes.SERVICE_VERSION: "1.0.0",
        })
        
        # Setup Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name=os.getenv("JAEGER_AGENT_HOST", "localhost"),
            agent_port=int(os.getenv("JAEGER_AGENT_PORT", 6831)),
        )
        
        provider = TracerProvider(resource=resource)
        processor = BatchSpanProcessor(jaeger_exporter)
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        
        self.tracer = trace.get_tracer(__name__)
        
        # Initialize metrics
        self.meter = metrics.get_meter(__name__)
        
        # Custom metrics
        self.api_latency = self.meter.create_histogram(
            name="api_endpoint_latency",
            description="API endpoint latency in milliseconds",
            unit="ms"
        )
        
        self.commission_amount_metric = self.meter.create_histogram(
            name="commission_amount",
            description="Commission amounts calculated",
            unit="USD"
        )
        
        self.active_users = self.meter.create_up_down_counter(
            name="active_users",
            description="Number of active users"
        )
    
    def track_api_request(self, method: str, endpoint: str, status: int, 
                         duration: float, user_id: Optional[str] = None,
                         plan: str = "unknown"):
        """Track API request metrics."""
        # Prometheus metrics
        api_requests_total.labels(
            method=method, 
            endpoint=endpoint, 
            status=status,
            plan=plan
        ).inc()
        
        api_request_duration.labels(
            method=method, 
            endpoint=endpoint
        ).observe(duration)
        
        # Structured logging
        logger.info(
            "api_request",
            method=method,
            endpoint=endpoint,
            status=status,
            duration_ms=duration * 1000,
            user_id=user_id,
            plan=plan,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # OpenTelemetry metrics
        self.api_latency.record(
            duration * 1000,
            {"method": method, "endpoint": endpoint, "status": str(status)}
        )
        
        # Track slow requests
        if duration > 1.0:
            logger.warning(
                "slow_api_request",
                method=method,
                endpoint=endpoint,
                duration_ms=duration * 1000,
                user_id=user_id
            )
    
    def track_commission_calculation(self, policy_type: str, transaction_type: str,
                                   amount: float, status: str = "success",
                                   user_id: Optional[str] = None):
        """Track commission calculation metrics."""
        commission_calculations_total.labels(
            policy_type=policy_type,
            transaction_type=transaction_type,
            status=status
        ).inc()
        
        if status == "success":
            commission_amount_histogram.labels(
                policy_type=policy_type,
                transaction_type=transaction_type
            ).observe(abs(amount))
            
            self.commission_amount_metric.record(
                abs(amount),
                {"policy_type": policy_type, "transaction_type": transaction_type}
            )
        
        logger.info(
            "commission_calculated",
            policy_type=policy_type,
            transaction_type=transaction_type,
            amount=amount,
            status=status,
            user_id=user_id
        )
    
    def track_webhook_delivery(self, event_type: str, url: str, 
                             status: str, duration: float,
                             retry_count: int = 0):
        """Track webhook delivery metrics."""
        webhook_deliveries_total.labels(
            event_type=event_type,
            status=status,
            retry_count=str(retry_count)
        ).inc()
        
        webhook_delivery_duration.labels(
            event_type=event_type,
            status=status
        ).observe(duration)
        
        logger.info(
            "webhook_delivery",
            event_type=event_type,
            url=url,
            status=status,
            duration_ms=duration * 1000,
            retry_count=retry_count
        )
    
    def track_integration_sync(self, integration: str, direction: str,
                             status: str, duration: float, 
                             records_synced: int = 0):
        """Track integration sync operations."""
        integration_sync_total.labels(
            integration=integration,
            direction=direction,
            status=status
        ).inc()
        
        integration_sync_duration.labels(
            integration=integration,
            direction=direction
        ).observe(duration)
        
        logger.info(
            "integration_sync",
            integration=integration,
            direction=direction,
            status=status,
            duration_seconds=duration,
            records_synced=records_synced
        )
    
    def track_database_query(self, operation: str, table: str,
                           duration: float, status: str = "success"):
        """Track database query metrics."""
        database_queries_total.labels(
            operation=operation,
            table=table,
            status=status
        ).inc()
        
        database_query_duration.labels(
            operation=operation,
            table=table
        ).observe(duration)
        
        if duration > 0.5:  # Log slow queries
            logger.warning(
                "slow_database_query",
                operation=operation,
                table=table,
                duration_ms=duration * 1000
            )
    
    def track_rate_limit_exceeded(self, api_key_prefix: str, limit_type: str):
        """Track rate limit exceeded events."""
        rate_limit_exceeded_total.labels(
            api_key_prefix=api_key_prefix[:8],  # Only first 8 chars for privacy
            limit_type=limit_type
        ).inc()
        
        logger.warning(
            "rate_limit_exceeded",
            api_key_prefix=api_key_prefix[:8],
            limit_type=limit_type
        )

class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to automatically track request metrics."""
    
    def __init__(self, app, monitoring_service: MonitoringService):
        super().__init__(app)
        self.monitoring = monitoring_service
    
    async def dispatch(self, request: Request, call_next):
        """Track metrics for each request."""
        # Track active connections
        active_connections.inc()
        
        # Start timing
        start_time = time.time()
        
        # Create span for distributed tracing
        with self.monitoring.tracer.start_as_current_span(
            f"{request.method} {request.url.path}"
        ) as span:
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.url", str(request.url))
            span.set_attribute("http.scheme", request.url.scheme)
            
            try:
                # Process request
                response = await call_next(request)
                
                # Calculate duration
                duration = time.time() - start_time
                
                # Extract user info if available
                user_id = request.state.__dict__.get("user_id")
                plan = request.state.__dict__.get("plan", "unknown")
                
                # Track metrics
                self.monitoring.track_api_request(
                    method=request.method,
                    endpoint=request.url.path,
                    status=response.status_code,
                    duration=duration,
                    user_id=user_id,
                    plan=plan
                )
                
                # Add response headers
                response.headers["X-Request-ID"] = span.get_span_context().trace_id.to_bytes(16, 'big').hex()
                response.headers["X-Response-Time"] = f"{duration * 1000:.2f}ms"
                
                # Update span
                span.set_attribute("http.status_code", response.status_code)
                
                return response
                
            except Exception as e:
                duration = time.time() - start_time
                
                # Track error
                self.monitoring.track_api_request(
                    method=request.method,
                    endpoint=request.url.path,
                    status=500,
                    duration=duration
                )
                
                # Update span
                span.record_exception(e)
                span.set_attribute("http.status_code", 500)
                
                logger.error(
                    "request_error",
                    method=request.method,
                    endpoint=request.url.path,
                    error=str(e),
                    duration_ms=duration * 1000
                )
                
                raise
                
            finally:
                # Decrement active connections
                active_connections.dec()

class HealthCheckService:
    """Comprehensive health checking service."""
    
    def __init__(self, redis_client: redis.Redis, database_client, 
                 rabbitmq_connection=None):
        self.redis = redis_client
        self.database = database_client
        self.rabbitmq = rabbitmq_connection
        
        self.checks = {
            "redis": self._check_redis,
            "database": self._check_database,
            "rabbitmq": self._check_rabbitmq,
            "api_gateway": self._check_api_gateway,
            "disk_space": self._check_disk_space,
            "memory": self._check_memory
        }
    
    async def check_health(self) -> Dict[str, Any]:
        """Run all health checks and return comprehensive status."""
        results = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "commission-intelligence-api",
            "version": "1.0.0",
            "checks": {}
        }
        
        for name, check_func in self.checks.items():
            try:
                start_time = time.time()
                is_healthy, details = await check_func()
                duration = time.time() - start_time
                
                results["checks"][name] = {
                    "status": "healthy" if is_healthy else "unhealthy",
                    "duration_ms": duration * 1000,
                    "details": details
                }
                
                if not is_healthy:
                    results["status"] = "degraded"
                    
            except Exception as e:
                results["checks"][name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                results["status"] = "unhealthy"
                
                logger.error(
                    "health_check_failed",
                    check=name,
                    error=str(e)
                )
        
        # Determine overall status
        unhealthy_count = sum(
            1 for check in results["checks"].values() 
            if check["status"] == "unhealthy"
        )
        
        if unhealthy_count > 0:
            results["status"] = "unhealthy"
        elif any(check["status"] == "degraded" for check in results["checks"].values()):
            results["status"] = "degraded"
        
        return results
    
    async def _check_redis(self) -> tuple[bool, dict]:
        """Check Redis connectivity and performance."""
        try:
            start = time.time()
            self.redis.ping()
            latency = (time.time() - start) * 1000
            
            # Check memory usage
            info = self.redis.info("memory")
            used_memory_mb = info["used_memory"] / 1024 / 1024
            
            return True, {
                "latency_ms": latency,
                "used_memory_mb": round(used_memory_mb, 2),
                "connected_clients": self.redis.info("clients")["connected_clients"]
            }
        except Exception as e:
            return False, {"error": str(e)}
    
    async def _check_database(self) -> tuple[bool, dict]:
        """Check database connectivity and performance."""
        try:
            start = time.time()
            # Simple query to check connectivity
            result = self.database.table('api_keys').select("count").limit(1).execute()
            latency = (time.time() - start) * 1000
            
            return True, {"latency_ms": latency}
        except Exception as e:
            return False, {"error": str(e)}
    
    async def _check_rabbitmq(self) -> tuple[bool, dict]:
        """Check RabbitMQ connectivity."""
        if not self.rabbitmq:
            return True, {"status": "not_configured"}
        
        try:
            is_open = self.rabbitmq and not self.rabbitmq.is_closed
            return is_open, {"connection_state": "open" if is_open else "closed"}
        except Exception as e:
            return False, {"error": str(e)}
    
    async def _check_api_gateway(self) -> tuple[bool, dict]:
        """Check API gateway functionality."""
        try:
            # Test rate limiting functionality
            test_key = "health_check_rate_limit_test"
            self.redis.setex(test_key, 10, "1")
            value = self.redis.get(test_key)
            
            return value == "1", {"rate_limiting": "operational"}
        except Exception as e:
            return False, {"error": str(e)}
    
    async def _check_disk_space(self) -> tuple[bool, dict]:
        """Check available disk space."""
        import shutil
        try:
            stat = shutil.disk_usage("/")
            free_gb = stat.free / (1024**3)
            used_percent = (stat.used / stat.total) * 100
            
            is_healthy = used_percent < 90  # Alert if >90% used
            
            return is_healthy, {
                "free_gb": round(free_gb, 2),
                "used_percent": round(used_percent, 2)
            }
        except Exception as e:
            return False, {"error": str(e)}
    
    async def _check_memory(self) -> tuple[bool, dict]:
        """Check system memory usage."""
        import psutil
        try:
            memory = psutil.virtual_memory()
            
            is_healthy = memory.percent < 90  # Alert if >90% used
            
            return is_healthy, {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_percent": memory.percent
            }
        except Exception as e:
            return False, {"error": str(e)}

# Metrics endpoint handler
async def metrics_handler(request: Request) -> Response:
    """Prometheus metrics endpoint handler."""
    metrics_data = generate_latest(registry)
    return Response(
        content=metrics_data,
        media_type=CONTENT_TYPE_LATEST,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache"
        }
    )

# Create global monitoring instance
monitoring_service = MonitoringService()