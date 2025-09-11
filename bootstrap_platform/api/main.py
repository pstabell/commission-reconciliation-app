"""
Commission Intelligence Platform - Bootstrap Demo API
Minimal but impressive API for demos and initial customers
"""
from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date, timedelta
import random
import json
import secrets
from decimal import Decimal

# Initialize FastAPI app
app = FastAPI(
    title="Commission Intelligence Platform API",
    description="Modern API for Insurance Commission Management",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Enable CORS for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple API key validation (for demo)
DEMO_API_KEYS = {
    "demo_key_12345": {"name": "Demo User", "plan": "professional"},
    "cipk_live_demo123": {"name": "Live Demo", "plan": "enterprise"}
}

def verify_api_key(authorization: Optional[str] = Header(None)):
    """Simple API key verification for demos"""
    if not authorization or not authorization.startswith("Bearer "):
        # Allow some endpoints without auth for demo
        return {"name": "Anonymous", "plan": "demo"}
    
    api_key = authorization.replace("Bearer ", "")
    if api_key in DEMO_API_KEYS:
        return DEMO_API_KEYS[api_key]
    
    raise HTTPException(status_code=401, detail="Invalid API key")

# Data models
class PolicyCreate(BaseModel):
    policy_number: str
    customer: str
    carrier: str
    policy_type: str = "AUTO"
    premium: float = Field(gt=0)
    effective_date: date
    expiration_date: Optional[date] = None
    commission_rate: Optional[float] = Field(ge=0, le=100, default=15.0)
    
class CommissionCalculation(BaseModel):
    premium: float = Field(gt=0)
    rate: float = Field(ge=0, le=100)
    type: str = "NEW"
    policy_type: str = "AUTO"

class WebhookTest(BaseModel):
    url: str
    event_type: str = "policy.created"
    
# Fake data generators
class FakeDataGenerator:
    """Generate realistic-looking fake data for demos"""
    
    carriers = ["Progressive", "State Farm", "Allstate", "GEICO", "Liberty Mutual", "Travelers", "Nationwide"]
    policy_types = ["AUTO", "HOME", "LIFE", "COMMERCIAL", "UMBRELLA"]
    customer_names = [
        "Johnson Insurance Group", "Smith Family Protection", "ABC Corp Coverage",
        "Premier Risk Management", "Coastal Insurance Services", "Mountain View Agency",
        "City Center Insurance", "Regional Coverage Partners", "National Risk Solutions"
    ]
    
    @staticmethod
    def generate_policies(count: int = 20) -> List[Dict]:
        policies = []
        for i in range(count):
            effective_date = datetime.now() - timedelta(days=random.randint(0, 365))
            
            policy = {
                "id": f"pol-{random.randint(1000, 9999)}",
                "policy_number": f"{random.choice(['AUTO', 'HOME', 'LIFE'])}-{random.randint(100000, 999999)}",
                "customer": random.choice(FakeDataGenerator.customer_names),
                "carrier": random.choice(FakeDataGenerator.carriers),
                "type": random.choice(FakeDataGenerator.policy_types),
                "premium": round(random.uniform(500, 5000), 2),
                "effective_date": effective_date.date().isoformat(),
                "expiration_date": (effective_date + timedelta(days=365)).date().isoformat(),
                "status": random.choice(["active", "pending_renewal", "new"]),
                "commission_rate": round(random.uniform(10, 20), 2),
                "commission_amount": 0  # Will be calculated
            }
            policy["commission_amount"] = round(policy["premium"] * policy["commission_rate"] / 100, 2)
            policies.append(policy)
            
        return sorted(policies, key=lambda x: x["effective_date"], reverse=True)
    
    @staticmethod
    def generate_dashboard_metrics() -> Dict:
        """Generate impressive dashboard metrics"""
        total_premium = round(random.uniform(2000000, 5000000), 2)
        avg_commission_rate = 12.5
        total_commission = round(total_premium * avg_commission_rate / 100, 2)
        
        return {
            "metrics": {
                "total_premium": total_premium,
                "total_commission": total_commission,
                "active_policies": random.randint(800, 1500),
                "renewal_rate": round(random.uniform(85, 95), 2),
                "average_commission": round(total_commission / random.randint(800, 1500), 2),
                "policies_at_risk": random.randint(50, 150),
                "new_business_ytd": round(random.uniform(300000, 600000), 2),
                "pending_renewals": random.randint(100, 300)
            },
            "trends": {
                "monthly_growth": round(random.uniform(8, 15), 2),
                "commission_growth": round(random.uniform(10, 18), 2),
                "policy_growth": round(random.uniform(5, 12), 2),
                "retention_trend": "improving"
            },
            "top_carriers": [
                {"name": "Progressive", "commission": round(random.uniform(50000, 100000), 2), "policies": random.randint(200, 400)},
                {"name": "State Farm", "commission": round(random.uniform(40000, 80000), 2), "policies": random.randint(150, 350)},
                {"name": "Allstate", "commission": round(random.uniform(30000, 60000), 2), "policies": random.randint(100, 300)}
            ],
            "top_agents": [
                {"name": "Sarah Johnson", "commission": round(random.uniform(20000, 40000), 2), "policies": random.randint(50, 150)},
                {"name": "Mike Chen", "commission": round(random.uniform(18000, 35000), 2), "policies": random.randint(40, 120)},
                {"name": "Jennifer Adams", "commission": round(random.uniform(15000, 30000), 2), "policies": random.randint(35, 100)}
            ],
            "monthly_commission": [
                {"month": "Jan", "amount": round(random.uniform(180000, 220000), 2)},
                {"month": "Feb", "amount": round(random.uniform(190000, 230000), 2)},
                {"month": "Mar", "amount": round(random.uniform(200000, 240000), 2)},
                {"month": "Apr", "amount": round(random.uniform(210000, 250000), 2)},
                {"month": "May", "amount": round(random.uniform(220000, 260000), 2)},
                {"month": "Jun", "amount": round(random.uniform(230000, 270000), 2)}
            ]
        }

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Commission Intelligence Platform API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/api/docs",
        "health": "/api/health",
        "message": "Welcome to the future of commission tracking"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "uptime": "99.9%",
        "response_time_ms": random.randint(10, 50)
    }

@app.get("/api/v1/policies")
async def list_policies(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    carrier: Optional[str] = None,
    sort: str = "effective_date",
    api_key: dict = Depends(verify_api_key)
):
    """List policies with pagination and filtering"""
    # Generate fake data for demo
    all_policies = FakeDataGenerator.generate_policies(100)
    
    # Apply filters
    if status:
        all_policies = [p for p in all_policies if p["status"] == status]
    if carrier:
        all_policies = [p for p in all_policies if p["carrier"].lower() == carrier.lower()]
    
    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    policies = all_policies[start:end]
    
    return {
        "data": policies,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": len(all_policies),
            "pages": (len(all_policies) + per_page - 1) // per_page
        },
        "summary": {
            "total_premium": sum(p["premium"] for p in all_policies),
            "total_commission": sum(p["commission_amount"] for p in all_policies),
            "average_rate": sum(p["commission_rate"] for p in all_policies) / len(all_policies) if all_policies else 0
        }
    }

@app.post("/api/v1/policies")
async def create_policy(
    policy: PolicyCreate,
    api_key: dict = Depends(verify_api_key)
):
    """Create a new policy"""
    # Calculate commission
    commission_amount = round(policy.premium * policy.commission_rate / 100, 2)
    
    # Create response
    new_policy = {
        "id": f"pol-{random.randint(10000, 99999)}",
        "policy_number": policy.policy_number,
        "customer": policy.customer,
        "carrier": policy.carrier,
        "type": policy.policy_type,
        "premium": policy.premium,
        "effective_date": policy.effective_date.isoformat(),
        "expiration_date": policy.expiration_date.isoformat() if policy.expiration_date else None,
        "commission_rate": policy.commission_rate,
        "commission_amount": commission_amount,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "created_by": api_key["name"]
    }
    
    return {
        "success": True,
        "data": new_policy,
        "message": "Policy created successfully"
    }

@app.post("/api/v1/commissions/calculate")
async def calculate_commission(
    calculation: CommissionCalculation,
    api_key: dict = Depends(verify_api_key)
):
    """Calculate commission with detailed breakdown"""
    # Base calculation
    gross_commission = calculation.premium * calculation.rate / 100
    
    # Determine splits based on transaction type
    if calculation.type == "NEW":
        agent_split = 0.5  # 50% for new business
        description = "New business commission"
    elif calculation.type == "RENEWAL":
        agent_split = 0.25  # 25% for renewals
        description = "Renewal commission"
    elif calculation.type == "ENDORSEMENT":
        agent_split = 0.4  # 40% for endorsements
        description = "Endorsement commission"
    else:
        agent_split = 0.5
        description = "Standard commission"
    
    agent_commission = gross_commission * agent_split
    agency_commission = gross_commission * (1 - agent_split)
    
    return {
        "calculation_id": f"calc-{random.randint(10000, 99999)}",
        "timestamp": datetime.now().isoformat(),
        "input": {
            "premium": calculation.premium,
            "rate": calculation.rate,
            "type": calculation.type
        },
        "results": {
            "gross_commission": round(gross_commission, 2),
            "agent_commission": round(agent_commission, 2),
            "agency_commission": round(agency_commission, 2),
            "agent_split_percentage": agent_split * 100,
            "agency_split_percentage": (1 - agent_split) * 100
        },
        "description": description,
        "breakdown": {
            "formula": f"${calculation.premium:,.2f} × {calculation.rate}% = ${gross_commission:,.2f}",
            "agent_calculation": f"${gross_commission:,.2f} × {agent_split*100}% = ${agent_commission:,.2f}",
            "agency_calculation": f"${gross_commission:,.2f} × {(1-agent_split)*100}% = ${agency_commission:,.2f}"
        }
    }

@app.get("/api/v1/analytics/dashboard")
async def get_dashboard(
    period: str = Query("month", description="Period: day, week, month, year"),
    api_key: dict = Depends(verify_api_key)
):
    """Get comprehensive dashboard analytics"""
    return FakeDataGenerator.generate_dashboard_metrics()

@app.get("/api/v1/analytics/performance")
async def get_performance_metrics(
    group_by: str = Query("agent", description="Group by: agent, carrier, policy_type"),
    period: str = Query("month"),
    api_key: dict = Depends(verify_api_key)
):
    """Get performance metrics grouped by various dimensions"""
    if group_by == "agent":
        data = [
            {"agent": "Sarah Johnson", "policies": 125, "premium": 156000, "commission": 19500, "growth": 12.5},
            {"agent": "Mike Chen", "policies": 98, "premium": 134000, "commission": 16750, "growth": 8.3},
            {"agent": "Jennifer Adams", "policies": 87, "premium": 115000, "commission": 14375, "growth": 15.2},
            {"agent": "Robert Wilson", "policies": 76, "premium": 98000, "commission": 12250, "growth": -2.1},
            {"agent": "Lisa Thompson", "policies": 65, "premium": 89000, "commission": 11125, "growth": 22.4}
        ]
    elif group_by == "carrier":
        data = [
            {"carrier": "Progressive", "policies": 234, "premium": 456000, "commission": 57000, "loss_ratio": 0.65},
            {"carrier": "State Farm", "policies": 198, "premium": 398000, "commission": 49750, "loss_ratio": 0.58},
            {"carrier": "Allstate", "policies": 156, "premium": 334000, "commission": 41750, "loss_ratio": 0.72}
        ]
    else:
        data = [
            {"type": "AUTO", "policies": 456, "premium": 567000, "commission": 70875, "avg_premium": 1243},
            {"type": "HOME", "policies": 234, "premium": 890000, "commission": 111250, "avg_premium": 3803},
            {"type": "LIFE", "policies": 123, "premium": 234000, "commission": 35100, "avg_premium": 1902}
        ]
    
    return {
        "period": period,
        "group_by": group_by,
        "data": data,
        "generated_at": datetime.now().isoformat()
    }

@app.get("/api/v1/integrations")
async def list_integrations(api_key: dict = Depends(verify_api_key)):
    """List available integrations and their status"""
    integrations = [
        {
            "id": "applied-epic",
            "name": "Applied Epic",
            "category": "AMS",
            "status": "available",
            "description": "Full bi-directional sync with Applied Epic",
            "features": ["Policy sync", "Commission download", "Document management", "Real-time updates"],
            "setup_fee": 5000,
            "monthly_fee": 100
        },
        {
            "id": "ezlynx",
            "name": "EZLynx",
            "category": "AMS",
            "status": "available",
            "description": "Complete integration with EZLynx Management System",
            "features": ["Policy sync", "Applicant data", "Commission tracking", "Activity log"],
            "setup_fee": 5000,
            "monthly_fee": 100
        },
        {
            "id": "hawksoft",
            "name": "HawkSoft",
            "category": "AMS",
            "status": "coming_soon",
            "description": "HawkSoft CMS integration",
            "features": ["Policy management", "Client data sync", "Commission tracking"],
            "setup_fee": 5000,
            "monthly_fee": 100
        },
        {
            "id": "hubspot",
            "name": "HubSpot",
            "category": "CRM",
            "status": "available",
            "description": "HubSpot CRM integration with custom objects",
            "features": ["Contact sync", "Deal tracking", "Renewal workflows", "Email automation"],
            "setup_fee": 3000,
            "monthly_fee": 50
        },
        {
            "id": "quickbooks",
            "name": "QuickBooks Online",
            "category": "Accounting",
            "status": "available",
            "description": "Automated accounting integration",
            "features": ["Journal entries", "Invoice creation", "Payment tracking", "Financial reports"],
            "setup_fee": 3000,
            "monthly_fee": 50
        },
        {
            "id": "salesforce",
            "name": "Salesforce",
            "category": "CRM",
            "status": "coming_soon",
            "description": "Salesforce platform integration",
            "features": ["Custom objects", "Workflow automation", "Lightning components"],
            "setup_fee": 7500,
            "monthly_fee": 150
        }
    ]
    
    # Filter based on user's plan
    if api_key["plan"] == "demo":
        integrations = [i for i in integrations if i["status"] == "available"][:2]
    
    return {
        "integrations": integrations,
        "summary": {
            "available": len([i for i in integrations if i["status"] == "available"]),
            "coming_soon": len([i for i in integrations if i["status"] == "coming_soon"]),
            "total": len(integrations)
        }
    }

@app.post("/api/v1/webhooks/test")
async def test_webhook(
    webhook: WebhookTest,
    api_key: dict = Depends(verify_api_key)
):
    """Test webhook delivery (demo only)"""
    # In production, this would actually send a webhook
    return {
        "success": True,
        "test_id": f"test-{random.randint(10000, 99999)}",
        "url": webhook.url,
        "event_type": webhook.event_type,
        "message": "Webhook test sent successfully",
        "delivered_at": datetime.now().isoformat(),
        "response_time_ms": random.randint(100, 500)
    }

@app.get("/api/v1/reconciliation/preview")
async def reconciliation_preview(
    carrier: Optional[str] = None,
    month: Optional[str] = None,
    api_key: dict = Depends(verify_api_key)
):
    """Preview reconciliation results"""
    # Generate fake reconciliation data
    matches = random.randint(150, 250)
    discrepancies = random.randint(5, 20)
    missing = random.randint(2, 10)
    
    return {
        "preview_id": f"recon-{random.randint(10000, 99999)}",
        "period": month or datetime.now().strftime("%Y-%m"),
        "carrier": carrier or "All Carriers",
        "summary": {
            "total_statements": matches + discrepancies + missing,
            "matched": matches,
            "discrepancies": discrepancies,
            "missing_commissions": missing,
            "match_rate": round(matches / (matches + discrepancies + missing) * 100, 2)
        },
        "financial_impact": {
            "expected_commission": round(random.uniform(50000, 100000), 2),
            "actual_commission": round(random.uniform(48000, 95000), 2),
            "variance": round(random.uniform(-5000, 5000), 2),
            "missing_commission_value": round(random.uniform(1000, 5000), 2)
        },
        "sample_discrepancies": [
            {
                "policy_number": f"AUTO-{random.randint(100000, 999999)}",
                "expected": round(random.uniform(100, 1000), 2),
                "actual": round(random.uniform(90, 900), 2),
                "variance": round(random.uniform(-100, 100), 2),
                "reason": "Rate mismatch"
            },
            {
                "policy_number": f"HOME-{random.randint(100000, 999999)}",
                "expected": round(random.uniform(200, 1500), 2),
                "actual": round(random.uniform(180, 1400), 2),
                "variance": round(random.uniform(-150, 150), 2),
                "reason": "Premium adjustment"
            }
        ]
    }

@app.get("/api/v1/reports/available")
async def list_available_reports(api_key: dict = Depends(verify_api_key)):
    """List available report types"""
    reports = [
        {
            "id": "commission-summary",
            "name": "Commission Summary Report",
            "description": "Monthly commission summary by agent, carrier, and policy type",
            "parameters": ["period", "group_by", "include_details"],
            "formats": ["pdf", "excel", "csv"]
        },
        {
            "id": "renewal-forecast",
            "name": "Renewal Forecast Report",
            "description": "Upcoming renewals with probability scoring",
            "parameters": ["days_ahead", "min_premium", "include_at_risk"],
            "formats": ["pdf", "excel"]
        },
        {
            "id": "agent-performance",
            "name": "Agent Performance Report",
            "description": "Detailed agent performance metrics and rankings",
            "parameters": ["period", "comparison_period", "metrics"],
            "formats": ["pdf", "excel"]
        },
        {
            "id": "reconciliation",
            "name": "Reconciliation Report",
            "description": "Detailed reconciliation results with variance analysis",
            "parameters": ["carrier", "period", "include_matched"],
            "formats": ["pdf", "excel", "csv"]
        }
    ]
    
    return {
        "reports": reports,
        "total": len(reports)
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "NOT_FOUND",
                "message": "The requested resource was not found",
                "path": str(request.url.path)
            }
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred. Please try again later.",
                "request_id": f"req-{random.randint(10000, 99999)}"
            }
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)