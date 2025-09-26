# Commission Intelligence Platform - Technical Specification
**Version**: 1.0  
**Date**: January 2025  
**Status**: Complete Build Specification

## Table of Contents
1. [System Architecture](#system-architecture)
2. [API Specifications](#api-specifications)
3. [Integration Specifications](#integration-specifications)
4. [Data Models](#data-models)
5. [Security Specifications](#security-specifications)
6. [Performance Requirements](#performance-requirements)
7. [Deployment Architecture](#deployment-architecture)

## System Architecture

### Microservices Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway (Kong/AWS)                    │
│                 Load Balancing | Caching | Auth             │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                     Service Mesh (Istio)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
     ┌────────────────┼────────────────┬─────────────────┐
     │                │                │                 │
┌────┴─────┐    ┌────┴─────┐    ┌────┴─────┐     ┌─────┴────┐
│ Policy   │    │Commission│    │Analytics │     │Integration│
│ Service  │    │ Service  │    │ Service  │     │ Service  │
└──────────┘    └──────────┘    └──────────┘     └──────────┘
     │                │                │                 │
┌────┴─────────────────────────────────────────────────┴─────┐
│                    PostgreSQL (Supabase)                    │
│                  Row Level Security Enabled                 │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Language: Python 3.11+
- Framework: FastAPI
- Async: asyncio, aiohttp
- ORM: SQLAlchemy (async)

**Infrastructure:**
- Container: Docker
- Orchestration: Kubernetes
- Service Mesh: Istio
- API Gateway: Kong
- Message Queue: RabbitMQ
- Cache: Redis
- Monitoring: Prometheus + Grafana
- Tracing: Jaeger
- Logging: ELK Stack

**Security:**
- Authentication: JWT (RS256)
- API Keys: HMAC-SHA256
- Encryption: AES-256-GCM
- TLS: 1.3 minimum

## API Specifications

### REST API Design

#### Base URL Structure
```
https://api.commissiontracker.io/v1
```

#### Authentication Headers
```http
Authorization: Bearer <JWT_TOKEN>
X-API-Key: <API_KEY>
X-Request-ID: <UUID>
```

### Core Endpoints

#### Policies API
```python
# Policy CRUD Operations
GET    /v1/policies                     # List policies (paginated)
GET    /v1/policies/{id}               # Get specific policy
POST   /v1/policies                     # Create new policy
PUT    /v1/policies/{id}               # Update policy
DELETE /v1/policies/{id}               # Delete policy
PATCH  /v1/policies/{id}               # Partial update

# Bulk Operations
POST   /v1/policies/bulk                # Create multiple policies
PUT    /v1/policies/bulk                # Update multiple policies
DELETE /v1/policies/bulk                # Delete multiple policies

# Policy Lifecycle
POST   /v1/policies/{id}/renew          # Create renewal
POST   /v1/policies/{id}/cancel         # Cancel policy
POST   /v1/policies/{id}/reinstate      # Reinstate policy
GET    /v1/policies/{id}/history        # Get policy history
GET    /v1/policies/{id}/documents      # Get policy documents

# Search and Filters
GET    /v1/policies/search              # Advanced search
GET    /v1/policies/expiring            # Policies expiring soon
GET    /v1/policies/pending-renewal     # Renewal opportunities
```

#### Commissions API
```python
# Commission Calculations
POST   /v1/commissions/calculate        # Calculate commission
POST   /v1/commissions/calculate/bulk   # Bulk calculations
GET    /v1/commissions/schedules        # Get commission schedules
PUT    /v1/commissions/schedules/{id}   # Update schedule

# Commission Tracking
GET    /v1/commissions                  # List commissions
GET    /v1/commissions/{id}            # Get specific commission
GET    /v1/commissions/pending          # Pending commissions
GET    /v1/commissions/paid            # Paid commissions
POST   /v1/commissions/{id}/pay        # Mark as paid

# Reconciliation
POST   /v1/commissions/reconcile        # Start reconciliation
GET    /v1/commissions/reconcile/{id}   # Get reconciliation status
POST   /v1/commissions/statements       # Upload statement
GET    /v1/commissions/discrepancies    # Get discrepancies

# Splits and Overrides
POST   /v1/commissions/splits           # Define split rules
GET    /v1/commissions/splits/{id}      # Get split details
POST   /v1/commissions/overrides        # Create override
```

#### Analytics API
```python
# Dashboard Metrics
GET    /v1/analytics/dashboard          # Main dashboard data
GET    /v1/analytics/kpis               # Key performance indicators
GET    /v1/analytics/trends             # Trend analysis

# Performance Analytics
GET    /v1/analytics/agent/{id}         # Agent performance
GET    /v1/analytics/agency             # Agency performance
GET    /v1/analytics/carrier/{id}       # Carrier performance
GET    /v1/analytics/product/{id}       # Product performance

# Forecasting
GET    /v1/analytics/forecast/revenue   # Revenue forecast
GET    /v1/analytics/forecast/retention # Retention forecast
GET    /v1/analytics/forecast/growth    # Growth forecast

# Custom Reports
POST   /v1/analytics/reports            # Create custom report
GET    /v1/analytics/reports/{id}       # Get report
GET    /v1/analytics/reports            # List saved reports
DELETE /v1/analytics/reports/{id}       # Delete report

# Benchmarking
GET    /v1/analytics/benchmark/agent    # Agent benchmarks
GET    /v1/analytics/benchmark/industry # Industry benchmarks
```

#### Integration API
```python
# Integration Management
GET    /v1/integrations                 # List available integrations
GET    /v1/integrations/{id}           # Get integration details
POST   /v1/integrations/{id}/connect    # Connect integration
DELETE /v1/integrations/{id}/disconnect # Disconnect
GET    /v1/integrations/{id}/status     # Check status

# Sync Operations
POST   /v1/integrations/{id}/sync       # Trigger sync
GET    /v1/integrations/{id}/sync/{job} # Get sync status
GET    /v1/integrations/{id}/logs       # Get sync logs

# Field Mapping
GET    /v1/integrations/{id}/mappings   # Get field mappings
PUT    /v1/integrations/{id}/mappings   # Update mappings
POST   /v1/integrations/{id}/test       # Test connection
```

### Request/Response Formats

#### Standard Request
```json
{
    "data": {
        "type": "policy",
        "attributes": {
            "policy_number": "AUTO-123456",
            "effective_date": "2025-09-01",
            "premium": 1200.00
        },
        "relationships": {
            "customer": {
                "data": {"type": "customer", "id": "cust-789"}
            }
        }
    }
}
```

#### Standard Response
```json
{
    "data": {
        "type": "policy",
        "id": "pol-123",
        "attributes": {
            "policy_number": "AUTO-123456",
            "status": "active"
        },
        "links": {
            "self": "/v1/policies/pol-123"
        }
    },
    "meta": {
        "request_id": "req-456",
        "timestamp": "2025-09-27T10:00:00Z"
    }
}
```

#### Error Response
```json
{
    "error": {
        "status": 400,
        "code": "VALIDATION_ERROR",
        "message": "Invalid policy data",
        "details": [
            {
                "field": "premium",
                "message": "Premium must be positive"
            }
        ],
        "request_id": "req-789"
    }
}
```

## Integration Specifications

### Applied Epic Integration

#### Authentication Flow
```python
# OAuth2 Authorization Code Flow
1. GET https://api.applied.com/oauth/authorize
   ?client_id={CLIENT_ID}
   &redirect_uri={REDIRECT_URI}
   &response_type=code
   &scope=policy.read+policy.write+commission.read

2. POST https://api.applied.com/oauth/token
   {
     "grant_type": "authorization_code",
     "code": "{AUTH_CODE}",
     "client_id": "{CLIENT_ID}",
     "client_secret": "{CLIENT_SECRET}"
   }
```

#### Data Sync Mapping
```python
# Applied Epic -> Commission Intelligence
{
    "Policy.PolicyNumber": "policy_number",
    "Policy.EffectiveDate": "effective_date",
    "Policy.ExpirationDate": "expiration_date",
    "Policy.Premium": "premium",
    "Policy.Status": {
        "Active": "active",
        "Cancelled": "cancelled",
        "Expired": "expired"
    },
    "Customer.Name": "customer_name",
    "Customer.Email": "customer_email",
    "Commission.Rate": "commission_rate",
    "Commission.Amount": "commission_amount"
}
```

### EZLynx Integration

#### API Endpoints
```python
# EZLynx REST API v3
BASE_URL = "https://api.ezlynx.com/v3"

# Authentication
POST   /auth/token
Header: X-API-Key: {API_KEY}

# Policy Operations
GET    /policies?updated_since={timestamp}
GET    /policies/{policyId}
POST   /policies
PUT    /policies/{policyId}

# Commission Downloads
GET    /commissions/statements
GET    /commissions/details/{statementId}
POST   /commissions/reconcile
```

### HubSpot Integration

#### Custom Objects Schema
```json
{
    "name": "insurance_policy",
    "labels": {
        "singular": "Insurance Policy",
        "plural": "Insurance Policies"
    },
    "properties": [
        {
            "name": "policy_number",
            "label": "Policy Number",
            "type": "string",
            "fieldType": "text"
        },
        {
            "name": "premium",
            "label": "Premium",
            "type": "number",
            "fieldType": "number"
        },
        {
            "name": "commission",
            "label": "Commission",
            "type": "number",
            "fieldType": "number"
        },
        {
            "name": "renewal_date",
            "label": "Renewal Date",
            "type": "date",
            "fieldType": "date"
        }
    ]
}
```

#### Workflow Triggers
```python
# Renewal Reminder Workflow
trigger = {
    "type": "property_change",
    "property": "renewal_date",
    "condition": "is_30_days_away"
}

# Commission Paid Workflow  
trigger = {
    "type": "webhook",
    "event": "commission.paid",
    "filters": {
        "amount": {"gt": 1000}
    }
}
```

## Data Models

### Core Schema

```sql
-- Policies table with API extensions
CREATE TABLE policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    policy_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id UUID REFERENCES customers(id),
    effective_date DATE NOT NULL,
    expiration_date DATE,
    premium DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    
    -- API specific columns
    external_id VARCHAR(100),
    source_system VARCHAR(50),
    last_sync_at TIMESTAMP,
    sync_status VARCHAR(20),
    api_metadata JSONB,
    
    -- Audit columns
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by UUID,
    updated_by UUID,
    
    -- Indexes for API performance
    INDEX idx_external_id (external_id),
    INDEX idx_source_system (source_system),
    INDEX idx_sync_status (sync_status)
);

-- Commission calculations with audit trail
CREATE TABLE commission_calculations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    policy_id UUID REFERENCES policies(id),
    calculation_date DATE NOT NULL,
    premium_amount DECIMAL(12,2) NOT NULL,
    commission_rate DECIMAL(5,2) NOT NULL,
    gross_commission DECIMAL(12,2) NOT NULL,
    
    -- Split tracking
    agent_split DECIMAL(5,2),
    agent_commission DECIMAL(12,2),
    agency_split DECIMAL(5,2),
    agency_commission DECIMAL(12,2),
    
    -- Override tracking
    override_amount DECIMAL(12,2),
    override_reason TEXT,
    override_by UUID,
    
    -- API tracking
    calculated_by_api BOOLEAN DEFAULT FALSE,
    api_request_id VARCHAR(100),
    calculation_metadata JSONB,
    
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_policy_calculation (policy_id, calculation_date)
);

-- Integration configurations
CREATE TABLE integration_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    integration_type VARCHAR(50) NOT NULL,
    config JSONB NOT NULL,
    credentials_encrypted TEXT,
    
    -- Sync settings
    sync_enabled BOOLEAN DEFAULT TRUE,
    sync_frequency VARCHAR(20) DEFAULT 'daily',
    last_sync_at TIMESTAMP,
    next_sync_at TIMESTAMP,
    
    -- Field mappings
    field_mappings JSONB,
    transform_rules JSONB,
    
    -- Status tracking
    status VARCHAR(20) DEFAULT 'active',
    error_count INTEGER DEFAULT 0,
    last_error TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- API audit log
CREATE TABLE api_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id VARCHAR(100) UNIQUE NOT NULL,
    api_key_id UUID REFERENCES api_keys(id),
    endpoint VARCHAR(200) NOT NULL,
    method VARCHAR(10) NOT NULL,
    request_body JSONB,
    response_status INTEGER,
    response_body JSONB,
    duration_ms INTEGER,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Partitioned by month for performance
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);
```

## Security Specifications

### API Key Structure
```
Format: cipk_[environment]_[random_32_chars]
Example: cipk_prod_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

Stored as: SHA256(api_key + salt)
```

### JWT Token Claims
```json
{
    "sub": "user-123",
    "email": "user@agency.com",
    "role": "agency_admin",
    "permissions": [
        "policies:read",
        "policies:write",
        "commissions:read",
        "analytics:read"
    ],
    "api_key_id": "key-456",
    "iat": 1706355200,
    "exp": 1706358800,
    "jti": "token-789"
}
```

### Encryption Standards
```python
# Data at rest
- Database: AES-256-GCM
- File storage: AES-256-CBC
- Backups: AES-256-GCM + RSA-4096

# Data in transit
- TLS 1.3 minimum
- Strong ciphers only
- Certificate pinning for mobile SDKs

# Sensitive data handling
- PII: Encrypted + field-level access control
- API credentials: Vault storage
- Logs: Redacted sensitive data
```

## Performance Requirements

### Response Time SLAs
```
GET /policies:          < 200ms (p95)
POST /policies:         < 500ms (p95)
POST /calculate:        < 100ms (p95)
GET /analytics:         < 2s (p95)
Bulk operations:        < 10s for 1000 records
```

### Throughput Requirements
```
API Requests:           10,000 req/sec
Webhook deliveries:     1,000/sec
Bulk imports:           100,000 records/hour
Real-time sync:         < 1 second latency
```

### Scalability Targets
```
Concurrent users:       10,000
Total policies:         100 million
Daily API calls:        1 billion
Data retention:         7 years
```

## Deployment Architecture

### Kubernetes Configuration
```yaml
# Production deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: commission-api
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 0
  template:
    spec:
      containers:
      - name: api
        image: commission-api:1.0.0
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Multi-Region Setup
```
Primary Region: US-East-1
- API servers: 10 instances
- Database: Primary + 2 read replicas
- Redis: Cluster mode (6 nodes)
- RabbitMQ: 3 node cluster

Secondary Region: US-West-2
- API servers: 5 instances
- Database: Read replica
- Redis: Cluster mode (3 nodes)
- Cross-region replication: < 100ms

Disaster Recovery:
- RPO: 5 minutes
- RTO: 15 minutes
- Automated failover
- Daily backup tests
```

This technical specification provides the complete blueprint for building the Commission Intelligence Platform. Every API endpoint, data model, integration point, and security requirement is fully documented and ready for implementation.