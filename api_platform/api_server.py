"""
Commission Intelligence Platform - FastAPI Server
RESTful API implementation
"""
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import os
import sys
import secrets
import hashlib
import json
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append('..')
from commission_app import get_supabase_client

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Commission Intelligence Platform API",
    description="API for integrating commission tracking into your insurance tech stack",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Models
class PolicyBase(BaseModel):
    policy_number: str
    customer: str
    effective_date: date
    expiration_date: Optional[date] = None
    premium: float
    policy_type: Optional[str] = None
    carrier: Optional[str] = None
    transaction_type: str = "NEW"
    
class PolicyCreate(PolicyBase):
    commission_rate: Optional[float] = None
    agent_id: Optional[str] = None
    external_id: Optional[str] = None

class PolicyResponse(PolicyBase):
    id: str
    commission: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class CommissionCalculateRequest(BaseModel):
    premium: float
    commission_rate: float
    policy_type: str
    transaction_type: str = "NEW"
    
class CommissionResponse(BaseModel):
    gross_commission: float
    agent_commission: float
    agency_commission: float
    calculation_details: Dict[str, Any]

class WebhookCreate(BaseModel):
    url: str
    events: List[str]
    secret: Optional[str] = None
    
class WebhookResponse(BaseModel):
    id: str
    url: str
    events: List[str]
    created_at: datetime
    is_active: bool

# Utility functions
def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API key and return user context."""
    api_key = credentials.credentials
    
    # Get Supabase client
    supabase = get_supabase_client()
    
    # Check API key in database
    result = supabase.table('api_keys').select("*").eq('api_key', api_key).eq('is_active', True).execute()
    
    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    key_data = result.data[0]
    
    # Update last used
    supabase.table('api_keys').update({'last_used': datetime.now().isoformat()}).eq('id', key_data['id']).execute()
    
    return key_data

def calculate_commission(premium: float, rate: float, policy_type: str, transaction_type: str) -> Dict[str, float]:
    """Calculate commission based on parameters."""
    if transaction_type == "CXL":
        # Cancellation - negative commission
        gross = -(premium * rate / 100)
    else:
        gross = premium * rate / 100
    
    # Default splits (these would come from database)
    agent_split = 0.5 if transaction_type == "NEW" else 0.25
    
    return {
        "gross_commission": round(gross, 2),
        "agent_commission": round(gross * agent_split, 2),
        "agency_commission": round(gross * (1 - agent_split), 2)
    }

# Routes
@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "name": "Commission Intelligence Platform API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Policies endpoints
@app.get("/v1/policies", response_model=List[PolicyResponse])
async def list_policies(
    page: int = 1,
    per_page: int = 20,
    status: Optional[str] = None,
    api_key: dict = Depends(verify_api_key)
):
    """List all policies for authenticated user."""
    supabase = get_supabase_client()
    
    # Build query
    query = supabase.table('policies').select("*")
    
    # Filter by user
    if 'user_email' in api_key:
        query = query.eq('user_email', api_key['user_email'])
    
    # Filter by status if provided
    if status:
        query = query.eq('status', status)
    
    # Pagination
    start = (page - 1) * per_page
    end = start + per_page - 1
    query = query.range(start, end)
    
    result = query.execute()
    
    # Format response
    policies = []
    for policy in result.data:
        policies.append(PolicyResponse(
            id=policy.get('_id', ''),
            policy_number=policy.get('Policy Number', ''),
            customer=policy.get('Customer', ''),
            effective_date=policy.get('Effective Date', ''),
            expiration_date=policy.get('X-Date', ''),
            premium=float(policy.get('Premium Sold', 0)),
            policy_type=policy.get('Policy Type', ''),
            carrier=policy.get('MGA/Carrier', ''),
            commission=float(policy.get('Agent Estimated Comm $', 0)),
            status='active',  # Calculate based on dates
            created_at=policy.get('created_at', datetime.now()),
            transaction_type=policy.get('Transaction Type', 'NEW')
        ))
    
    return policies

@app.post("/v1/policies", response_model=PolicyResponse)
async def create_policy(
    policy: PolicyCreate,
    api_key: dict = Depends(verify_api_key)
):
    """Create a new policy."""
    supabase = get_supabase_client()
    
    # Calculate commission if rate provided
    commission = 0
    if policy.commission_rate:
        calc = calculate_commission(
            policy.premium, 
            policy.commission_rate, 
            policy.policy_type or "AUTO",
            policy.transaction_type
        )
        commission = calc['agent_commission']
    
    # Create policy data
    policy_data = {
        'Policy Number': policy.policy_number,
        'Customer': policy.customer,
        'Effective Date': policy.effective_date.isoformat(),
        'X-Date': policy.expiration_date.isoformat() if policy.expiration_date else None,
        'Premium Sold': policy.premium,
        'Policy Type': policy.policy_type,
        'MGA/Carrier': policy.carrier,
        'Transaction Type': policy.transaction_type,
        'Agent Estimated Comm $': commission,
        'api_source': 'api_platform',
        'external_id': policy.external_id,
        'created_at': datetime.now().isoformat()
    }
    
    # Add user email if in production
    if 'user_email' in api_key:
        policy_data['user_email'] = api_key['user_email']
    
    # Insert policy
    result = supabase.table('policies').insert(policy_data).execute()
    
    if result.data:
        created = result.data[0]
        return PolicyResponse(
            id=created.get('_id', ''),
            policy_number=created.get('Policy Number', ''),
            customer=created.get('Customer', ''),
            effective_date=created.get('Effective Date', ''),
            expiration_date=created.get('X-Date', ''),
            premium=float(created.get('Premium Sold', 0)),
            policy_type=created.get('Policy Type', ''),
            carrier=created.get('MGA/Carrier', ''),
            commission=float(created.get('Agent Estimated Comm $', 0)),
            status='active',
            created_at=created.get('created_at', datetime.now())
        )
    
    raise HTTPException(status_code=400, detail="Failed to create policy")

# Commission endpoints
@app.post("/v1/commissions/calculate", response_model=CommissionResponse)
async def calculate_commission_endpoint(
    request: CommissionCalculateRequest,
    api_key: dict = Depends(verify_api_key)
):
    """Calculate commission for given parameters."""
    calc = calculate_commission(
        request.premium,
        request.commission_rate,
        request.policy_type,
        request.transaction_type
    )
    
    return CommissionResponse(
        gross_commission=calc['gross_commission'],
        agent_commission=calc['agent_commission'],
        agency_commission=calc['agency_commission'],
        calculation_details={
            'premium': request.premium,
            'rate': request.commission_rate,
            'type': request.transaction_type,
            'formula': f"{request.premium} x {request.commission_rate}% = {calc['gross_commission']}"
        }
    )

# Webhook endpoints
@app.post("/v1/webhooks", response_model=WebhookResponse)
async def create_webhook(
    webhook: WebhookCreate,
    api_key: dict = Depends(verify_api_key)
):
    """Register a new webhook."""
    supabase = get_supabase_client()
    
    # Generate webhook secret if not provided
    if not webhook.secret:
        webhook.secret = secrets.token_urlsafe(32)
    
    webhook_data = {
        'user_email': api_key.get('user_email'),
        'url': webhook.url,
        'events': webhook.events,
        'secret': webhook.secret,
        'is_active': True,
        'created_at': datetime.now().isoformat()
    }
    
    result = supabase.table('webhook_endpoints').insert(webhook_data).execute()
    
    if result.data:
        created = result.data[0]
        return WebhookResponse(
            id=created.get('id', ''),
            url=created.get('url', ''),
            events=created.get('events', []),
            created_at=created.get('created_at', datetime.now()),
            is_active=created.get('is_active', True)
        )
    
    raise HTTPException(status_code=400, detail="Failed to create webhook")

@app.get("/v1/webhooks", response_model=List[WebhookResponse])
async def list_webhooks(api_key: dict = Depends(verify_api_key)):
    """List all webhooks for authenticated user."""
    supabase = get_supabase_client()
    
    query = supabase.table('webhook_endpoints').select("*")
    
    if 'user_email' in api_key:
        query = query.eq('user_email', api_key['user_email'])
    
    result = query.execute()
    
    webhooks = []
    for hook in result.data:
        webhooks.append(WebhookResponse(
            id=hook.get('id', ''),
            url=hook.get('url', ''),
            events=hook.get('events', []),
            created_at=hook.get('created_at', datetime.now()),
            is_active=hook.get('is_active', True)
        ))
    
    return webhooks

# Analytics endpoints
@app.get("/v1/analytics/summary")
async def get_analytics_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    api_key: dict = Depends(verify_api_key)
):
    """Get commission analytics summary."""
    supabase = get_supabase_client()
    
    # This would aggregate data from policies table
    # For demo, return mock data
    return {
        "period": {
            "start": start_date or date(2025, 1, 1),
            "end": end_date or date.today()
        },
        "totals": {
            "policies": 156,
            "premium": 187500.00,
            "commission_earned": 22500.00,
            "commission_paid": 18750.00,
            "commission_pending": 3750.00
        },
        "by_type": {
            "NEW": {"count": 45, "commission": 15000.00},
            "RWL": {"count": 98, "commission": 7000.00},
            "END": {"count": 13, "commission": 500.00}
        },
        "by_carrier": [
            {"carrier": "Progressive", "policies": 45, "commission": 8500.00},
            {"carrier": "State Farm", "policies": 38, "commission": 7200.00},
            {"carrier": "Allstate", "policies": 29, "commission": 4800.00}
        ]
    }

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return {
        "error": {
            "status": exc.status_code,
            "message": exc.detail
        }
    }

# Additional endpoints for comprehensive API

# Renewal Management
@app.get("/v1/renewals/upcoming")
async def get_upcoming_renewals(
    days_ahead: int = 30,
    api_key: dict = Depends(verify_api_key)
):
    """Get policies with upcoming renewals."""
    supabase = get_supabase_client()
    
    from datetime import timedelta
    future_date = (datetime.now() + timedelta(days=days_ahead)).date()
    
    query = supabase.table('policies').select("*")
    if 'user_email' in api_key:
        query = query.eq('user_email', api_key['user_email'])
    
    # Filter for policies expiring soon
    query = query.gte('X-Date', datetime.now().date().isoformat())
    query = query.lte('X-Date', future_date.isoformat())
    
    result = query.execute()
    
    renewals = []
    for policy in result.data:
        renewals.append({
            'policy_id': policy.get('_id'),
            'policy_number': policy.get('Policy Number'),
            'customer': policy.get('Customer'),
            'expiration_date': policy.get('X-Date'),
            'days_until_expiration': (
                datetime.fromisoformat(policy.get('X-Date')) - datetime.now()
            ).days,
            'premium': float(policy.get('Premium Sold', 0)),
            'estimated_renewal_commission': float(policy.get('Agent Estimated Comm $', 0)) * 0.5
        })
    
    return {"renewals": renewals, "count": len(renewals)}

# Batch Operations
@app.post("/v1/policies/batch")
async def create_policies_batch(
    policies: List[PolicyCreate],
    api_key: dict = Depends(verify_api_key)
):
    """Create multiple policies in one request."""
    created_policies = []
    errors = []
    
    for idx, policy in enumerate(policies):
        try:
            # Reuse single policy creation logic
            result = await create_policy(policy, api_key)
            created_policies.append(result)
        except Exception as e:
            errors.append({
                'index': idx,
                'policy_number': policy.policy_number,
                'error': str(e)
            })
    
    return {
        'created': created_policies,
        'errors': errors,
        'success_count': len(created_policies),
        'error_count': len(errors)
    }

# Search functionality
@app.get("/v1/search")
async def search_policies(
    q: str,
    search_fields: List[str] = ["Policy Number", "Customer"],
    api_key: dict = Depends(verify_api_key)
):
    """Search across multiple fields."""
    supabase = get_supabase_client()
    
    results = []
    for field in search_fields:
        query = supabase.table('policies').select("*")
        
        if 'user_email' in api_key:
            query = query.eq('user_email', api_key['user_email'])
        
        # Case-insensitive search
        query = query.ilike(field, f'%{q}%')
        result = query.execute()
        
        for policy in result.data:
            # Avoid duplicates
            if not any(p.get('_id') == policy.get('_id') for p in results):
                results.append({
                    'id': policy.get('_id'),
                    'policy_number': policy.get('Policy Number'),
                    'customer': policy.get('Customer'),
                    'matched_field': field,
                    'premium': float(policy.get('Premium Sold', 0))
                })
    
    return {"results": results, "count": len(results), "query": q}

# Commission history
@app.get("/v1/commissions/history")
async def get_commission_history(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    transaction_type: Optional[str] = None,
    api_key: dict = Depends(verify_api_key)
):
    """Get historical commission data with filters."""
    supabase = get_supabase_client()
    
    query = supabase.table('policies').select("*")
    
    if 'user_email' in api_key:
        query = query.eq('user_email', api_key['user_email'])
    
    # Date filtering
    if start_date:
        query = query.gte('Effective Date', start_date.isoformat())
    if end_date:
        query = query.lte('Effective Date', end_date.isoformat())
    
    # Transaction type filter
    if transaction_type:
        query = query.eq('Transaction Type', transaction_type)
    
    result = query.execute()
    
    # Calculate totals
    total_premium = sum(float(p.get('Premium Sold', 0)) for p in result.data)
    total_commission = sum(float(p.get('Agent Estimated Comm $', 0)) for p in result.data)
    
    return {
        'period': {
            'start': start_date.isoformat() if start_date else None,
            'end': end_date.isoformat() if end_date else None
        },
        'totals': {
            'premium': total_premium,
            'commission': total_commission,
            'policy_count': len(result.data),
            'average_commission': total_commission / len(result.data) if result.data else 0
        },
        'by_type': self._group_by_type(result.data)
    }

def _group_by_type(self, policies):
    """Group policies by transaction type."""
    grouped = {}
    for policy in policies:
        t_type = policy.get('Transaction Type', 'OTHER')
        if t_type not in grouped:
            grouped[t_type] = {'count': 0, 'commission': 0}
        grouped[t_type]['count'] += 1
        grouped[t_type]['commission'] += float(policy.get('Agent Estimated Comm $', 0))
    return grouped

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)