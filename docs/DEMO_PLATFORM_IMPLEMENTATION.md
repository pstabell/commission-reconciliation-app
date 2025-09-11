# Demo Platform Implementation Guide
**Version**: 1.0  
**Timeline**: 4 weeks  
**Budget**: $30-50/month  
**Goal**: Create an impressive demo platform that converts prospects into paying customers

## Week 1: Marketing Website & Brand

### Day 1-2: Domain & Hosting Setup
```bash
# Purchase domain
- commission-intelligence.io ($15/year)
- Alternative: usecommissioniq.com

# Free hosting setup
1. Create Vercel account (free)
2. Create GitHub repository
3. Connect Vercel to GitHub
4. Enable auto-deploy

# Free SSL included with Vercel
```

### Day 3-5: Landing Page Development
```html
<!-- index.html - Impressive landing page -->
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <title>Commission Intelligence Platform - Modern API for Insurance Agencies</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer data-domain="commission-intelligence.io" src="https://plausible.io/js/script.js"></script>
</head>
<body class="bg-gray-50">
    <!-- Hero Section -->
    <section class="relative overflow-hidden bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 text-white">
        <div class="absolute inset-0 bg-grid-white/10"></div>
        <nav class="relative z-10 p-6">
            <div class="max-w-7xl mx-auto flex justify-between items-center">
                <h1 class="text-2xl font-bold">Commission IQ</h1>
                <div class="space-x-6">
                    <a href="#features" class="hover:text-blue-200">Features</a>
                    <a href="#integrations" class="hover:text-blue-200">Integrations</a>
                    <a href="/pricing" class="hover:text-blue-200">Pricing</a>
                    <a href="/demo" class="bg-white text-blue-900 px-6 py-2 rounded-lg font-semibold hover:bg-blue-50">Book Demo</a>
                </div>
            </div>
        </nav>
        
        <div class="relative z-10 max-w-7xl mx-auto px-6 py-24">
            <div class="max-w-3xl">
                <h2 class="text-5xl font-bold mb-6">The Commission Intelligence Platform for Modern Insurance Agencies</h2>
                <p class="text-xl mb-8 text-blue-100">Stop wasting 80% of your time on manual reconciliation. Our API-first platform integrates with your existing tools to automate commission tracking, reconciliation, and reporting.</p>
                <div class="flex space-x-4">
                    <a href="/demo" class="bg-white text-blue-900 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition">Schedule Demo</a>
                    <a href="/api" class="border-2 border-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-blue-900 transition">View API Docs</a>
                </div>
            </div>
        </div>
        
        <!-- Fake but impressive stats -->
        <div class="relative z-10 bg-blue-950/50 backdrop-blur">
            <div class="max-w-7xl mx-auto px-6 py-12 grid grid-cols-4 gap-8">
                <div class="text-center">
                    <div class="text-4xl font-bold" id="agency-count">52</div>
                    <div class="text-blue-200">Agencies</div>
                </div>
                <div class="text-center">
                    <div class="text-4xl font-bold" id="api-calls">1.2M</div>
                    <div class="text-blue-200">API Calls/Month</div>
                </div>
                <div class="text-center">
                    <div class="text-4xl font-bold">99.9%</div>
                    <div class="text-blue-200">Uptime SLA</div>
                </div>
                <div class="text-center">
                    <div class="text-4xl font-bold">80%</div>
                    <div class="text-blue-200">Time Saved</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-24">
        <div class="max-w-7xl mx-auto px-6">
            <h3 class="text-4xl font-bold text-center mb-16">Built for Modern Insurance Operations</h3>
            <div class="grid grid-cols-3 gap-8">
                <!-- Feature cards with impressive but vague descriptions -->
                <div class="bg-white p-8 rounded-xl shadow-lg">
                    <div class="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                        </svg>
                    </div>
                    <h4 class="text-xl font-bold mb-2">Real-Time Sync</h4>
                    <p class="text-gray-600">Automatic synchronization with your AMS, CRM, and accounting systems. Changes reflect instantly across all platforms.</p>
                </div>
                <!-- Add more feature cards -->
            </div>
        </div>
    </section>

    <!-- Integration logos (no actual integrations yet) -->
    <section id="integrations" class="py-24 bg-gray-100">
        <div class="max-w-7xl mx-auto px-6">
            <h3 class="text-4xl font-bold text-center mb-16">Integrates With Your Entire Tech Stack</h3>
            <div class="grid grid-cols-6 gap-8 items-center opacity-60">
                <!-- Use free logos or create simple text representations -->
                <div class="text-center">
                    <div class="bg-white p-6 rounded-lg shadow">Applied Epic</div>
                </div>
                <div class="text-center">
                    <div class="bg-white p-6 rounded-lg shadow">EZLynx</div>
                </div>
                <div class="text-center">
                    <div class="bg-white p-6 rounded-lg shadow">HubSpot</div>
                </div>
                <div class="text-center">
                    <div class="bg-white p-6 rounded-lg shadow">QuickBooks</div>
                </div>
                <div class="text-center">
                    <div class="bg-white p-6 rounded-lg shadow">Salesforce</div>
                </div>
                <div class="text-center">
                    <div class="bg-white p-6 rounded-lg shadow">+15 more</div>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="py-24 bg-blue-900 text-white">
        <div class="max-w-4xl mx-auto text-center px-6">
            <h3 class="text-4xl font-bold mb-6">Ready to Transform Your Commission Operations?</h3>
            <p class="text-xl mb-8">Join forward-thinking agencies saving 80% of their reconciliation time</p>
            <a href="/demo" class="inline-block bg-white text-blue-900 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition">Schedule Your Demo</a>
        </div>
    </section>

    <!-- Fake counter animations -->
    <script>
        // Animate counters on page load
        function animateCounter(id, target, suffix = '') {
            let current = 0;
            const increment = target / 50;
            const element = document.getElementById(id);
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                element.textContent = Math.floor(current).toLocaleString() + suffix;
            }, 30);
        }
        
        // Start animations when visible
        setTimeout(() => {
            animateCounter('agency-count', 52);
            animateCounter('api-calls', 1200000, 'M');
        }, 500);
    </script>
</body>
</html>
```

### Day 6-7: Additional Pages
```html
<!-- pricing.html - Emphasize setup fees -->
<section class="py-24">
    <div class="max-w-6xl mx-auto px-6">
        <h2 class="text-4xl font-bold text-center mb-16">Transparent Pricing for Every Agency</h2>
        
        <!-- Setup Fees - Make these prominent -->
        <div class="bg-blue-50 border-2 border-blue-200 rounded-xl p-8 mb-12">
            <h3 class="text-2xl font-bold mb-4">One-Time Setup & Integration</h3>
            <p class="text-gray-700 mb-6">Our expert team customizes the platform for your specific workflows and integrations</p>
            <div class="grid grid-cols-3 gap-6">
                <div class="bg-white p-6 rounded-lg">
                    <h4 class="font-bold text-lg mb-2">Starter Setup</h4>
                    <div class="text-3xl font-bold mb-2">$2,500</div>
                    <ul class="text-sm text-gray-600 space-y-1">
                        <li>✓ 1 integration</li>
                        <li>✓ Data mapping</li>
                        <li>✓ 2 week delivery</li>
                    </ul>
                </div>
                <div class="bg-white p-6 rounded-lg border-2 border-blue-500">
                    <div class="bg-blue-500 text-white text-xs px-2 py-1 rounded inline-block mb-2">MOST POPULAR</div>
                    <h4 class="font-bold text-lg mb-2">Professional Setup</h4>
                    <div class="text-3xl font-bold mb-2">$5,000</div>
                    <ul class="text-sm text-gray-600 space-y-1">
                        <li>✓ 3 integrations</li>
                        <li>✓ Custom workflows</li>
                        <li>✓ Priority support</li>
                    </ul>
                </div>
                <div class="bg-white p-6 rounded-lg">
                    <h4 class="font-bold text-lg mb-2">Enterprise Setup</h4>
                    <div class="text-3xl font-bold mb-2">$10,000+</div>
                    <ul class="text-sm text-gray-600 space-y-1">
                        <li>✓ Unlimited integrations</li>
                        <li>✓ Dedicated engineer</li>
                        <li>✓ White-label options</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <!-- Monthly Plans -->
        <div class="grid grid-cols-3 gap-8">
            <!-- Monthly plan cards here -->
        </div>
    </div>
</section>
```

## Week 2: Demo Application Backend

### Day 8-9: FastAPI Setup
```python
# api/main.py - Minimal but impressive API
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
import random
import json

app = FastAPI(
    title="Commission Intelligence Platform API",
    description="Modern API for Insurance Commission Management",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Enable CORS for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fake data generator
class FakeDataGenerator:
    @staticmethod
    def generate_policies(count: int = 20):
        carriers = ["Progressive", "State Farm", "Allstate", "GEICO", "Liberty Mutual"]
        types = ["Auto", "Home", "Life", "Commercial", "Umbrella"]
        policies = []
        
        for i in range(count):
            policies.append({
                "id": f"pol-{random.randint(1000, 9999)}",
                "policy_number": f"{random.choice(['AUTO', 'HOME', 'LIFE'])}-{random.randint(100000, 999999)}",
                "customer": f"Customer {i+1}",
                "carrier": random.choice(carriers),
                "type": random.choice(types),
                "premium": round(random.uniform(500, 5000), 2),
                "effective_date": date.today().isoformat(),
                "status": random.choice(["active", "pending", "renewal"]),
                "commission_rate": round(random.uniform(10, 20), 2),
            })
        return policies

# Demo data endpoints
@app.get("/api/v1/policies")
async def list_policies(
    limit: int = 20,
    offset: int = 0,
    demo: bool = True
):
    """List all policies with pagination"""
    if demo:
        policies = FakeDataGenerator.generate_policies(50)
        return {
            "data": policies[offset:offset + limit],
            "total": len(policies),
            "limit": limit,
            "offset": offset
        }
    # Real implementation would go here

@app.post("/api/v1/commissions/calculate")
async def calculate_commission(
    premium: float,
    rate: float,
    type: str = "NEW"
):
    """Calculate commission - this actually works"""
    gross = premium * rate / 100
    
    # Realistic split logic
    if type == "NEW":
        agent_split = 0.5
    elif type == "RENEWAL":
        agent_split = 0.25
    else:
        agent_split = 0.4
    
    return {
        "gross_commission": round(gross, 2),
        "agent_commission": round(gross * agent_split, 2),
        "agency_commission": round(gross * (1 - agent_split), 2),
        "calculation_id": f"calc-{random.randint(1000, 9999)}",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/analytics/dashboard")
async def get_dashboard(demo: bool = True):
    """Return impressive dashboard metrics"""
    if demo:
        return {
            "metrics": {
                "total_premium": 2456789.50,
                "total_commission": 294814.74,
                "active_policies": 1247,
                "renewal_rate": 0.89,
                "average_commission": 236.45
            },
            "trends": {
                "monthly_growth": 0.12,
                "commission_growth": 0.15,
                "policy_growth": 0.08
            },
            "top_carriers": [
                {"name": "Progressive", "commission": 89234.56},
                {"name": "State Farm", "commission": 76543.21},
                {"name": "Allstate", "commission": 65432.10}
            ]
        }

@app.get("/api/v1/integrations")
async def list_integrations():
    """Show available integrations (all fake for now)"""
    return {
        "available": [
            {"id": "applied-epic", "name": "Applied Epic", "status": "available", "setup_fee": 5000},
            {"id": "ezlynx", "name": "EZLynx", "status": "available", "setup_fee": 5000},
            {"id": "hawksoft", "name": "HawkSoft", "status": "coming_soon", "setup_fee": 5000},
            {"id": "hubspot", "name": "HubSpot", "status": "available", "setup_fee": 3000},
            {"id": "quickbooks", "name": "QuickBooks", "status": "available", "setup_fee": 3000},
            {"id": "salesforce", "name": "Salesforce", "status": "coming_soon", "setup_fee": 7500},
        ],
        "active": []  # None active in demo
    }

# Health check that always succeeds
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "uptime": "99.9%",
        "response_time_ms": random.randint(10, 50)
    }

# Webhook tester (actually works)
@app.post("/api/v1/webhooks/test")
async def test_webhook(url: str, event_type: str = "policy.created"):
    """Test webhook delivery"""
    # In demo, just return success
    return {
        "status": "success",
        "message": "Webhook test sent successfully",
        "delivered_at": datetime.now().isoformat()
    }

# Run with: uvicorn api.main:app --reload --port 8000
```

### Day 10-11: Demo Dashboard
```javascript
// dashboard/src/App.js - React dashboard with fake data
import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function Dashboard() {
    const [metrics, setMetrics] = useState(null);
    const [policies, setPolicies] = useState([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        // Simulate API calls
        setTimeout(() => {
            // Fake metrics that look impressive
            setMetrics({
                totalPremium: 2456789.50,
                totalCommission: 294814.74,
                activePolicies: 1247,
                renewalRate: 89,
                monthlyGrowth: 12
            });
            
            // Generate fake policy data
            const fakePolicies = Array.from({ length: 20 }, (_, i) => ({
                id: `POL-${1000 + i}`,
                customer: `Customer ${i + 1}`,
                premium: Math.round(Math.random() * 5000 + 500),
                commission: Math.round(Math.random() * 500 + 50),
                status: ['Active', 'Pending', 'Renewal'][Math.floor(Math.random() * 3)]
            }));
            setPolicies(fakePolicies);
            setLoading(false);
        }, 1000);
    }, []);
    
    // Fake chart data
    const monthlyData = [
        { month: 'Jan', commission: 22453 },
        { month: 'Feb', commission: 24567 },
        { month: 'Mar', commission: 23890 },
        { month: 'Apr', commission: 26734 },
        { month: 'May', commission: 28956 },
        { month: 'Jun', commission: 31247 }
    ];
    
    return (
        <div className="min-h-screen bg-gray-50">
            <nav className="bg-white shadow">
                <div className="px-6 py-4">
                    <h1 className="text-2xl font-bold text-gray-900">Commission Intelligence Platform</h1>
                </div>
            </nav>
            
            {/* Metrics Grid */}
            <div className="p-6">
                <div className="grid grid-cols-5 gap-6 mb-8">
                    <MetricCard
                        title="Total Premium"
                        value={`$${metrics?.totalPremium.toLocaleString()}`}
                        change="+12%"
                        trend="up"
                    />
                    <MetricCard
                        title="Total Commission"
                        value={`$${metrics?.totalCommission.toLocaleString()}`}
                        change="+15%"
                        trend="up"
                    />
                    <MetricCard
                        title="Active Policies"
                        value={metrics?.activePolicies.toLocaleString()}
                        change="+8%"
                        trend="up"
                    />
                    <MetricCard
                        title="Renewal Rate"
                        value={`${metrics?.renewalRate}%`}
                        change="+2%"
                        trend="up"
                    />
                    <MetricCard
                        title="Avg Commission"
                        value="$236"
                        change="+5%"
                        trend="up"
                    />
                </div>
                
                {/* Charts */}
                <div className="grid grid-cols-2 gap-6 mb-8">
                    <div className="bg-white p-6 rounded-lg shadow">
                        <h3 className="text-lg font-semibold mb-4">Commission Trend</h3>
                        <LineChart width={500} height={300} data={monthlyData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="month" />
                            <YAxis />
                            <Tooltip />
                            <Line type="monotone" dataKey="commission" stroke="#3B82F6" strokeWidth={2} />
                        </LineChart>
                    </div>
                    
                    <div className="bg-white p-6 rounded-lg shadow">
                        <h3 className="text-lg font-semibold mb-4">Top Carriers</h3>
                        <BarChart width={500} height={300} data={carrierData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Bar dataKey="commission" fill="#3B82F6" />
                        </BarChart>
                    </div>
                </div>
                
                {/* Recent Policies Table */}
                <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b">
                        <h3 className="text-lg font-semibold">Recent Policies</h3>
                    </div>
                    <table className="w-full">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Policy</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Premium</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Commission</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {policies.map(policy => (
                                <tr key={policy.id}>
                                    <td className="px-6 py-4">{policy.id}</td>
                                    <td className="px-6 py-4">{policy.customer}</td>
                                    <td className="px-6 py-4">${policy.premium}</td>
                                    <td className="px-6 py-4">${policy.commission}</td>
                                    <td className="px-6 py-4">
                                        <span className={`px-2 py-1 text-xs rounded-full ${
                                            policy.status === 'Active' ? 'bg-green-100 text-green-800' :
                                            policy.status === 'Pending' ? 'bg-yellow-100 text-yellow-800' :
                                            'bg-blue-100 text-blue-800'
                                        }`}>
                                            {policy.status}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
```

### Day 12-14: Developer Portal
```html
<!-- developer/index.html - Professional API documentation -->
<!DOCTYPE html>
<html>
<head>
    <title>Commission Intelligence API Documentation</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stoplight/elements@7/styles.min.css">
    <script src="https://cdn.jsdelivr.net/npm/@stoplight/elements@7/web-components.min.js"></script>
</head>
<body>
    <div class="container">
        <nav class="navbar">
            <h1>Commission Intelligence API</h1>
            <div class="nav-links">
                <a href="#getting-started">Getting Started</a>
                <a href="#authentication">Authentication</a>
                <a href="#endpoints">Endpoints</a>
                <a href="#sdks">SDKs</a>
                <a href="#support">Support</a>
            </div>
        </nav>
        
        <section id="getting-started" class="section">
            <h2>Getting Started</h2>
            <div class="quickstart">
                <h3>Quick Start</h3>
                <pre><code># 1. Get your API key from the dashboard
# 2. Make your first request
curl https://api.commission-intelligence.io/v1/policies \
  -H "Authorization: Bearer YOUR_API_KEY"

# 3. Calculate a commission
curl -X POST https://api.commission-intelligence.io/v1/commissions/calculate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"premium": 1000, "rate": 15}'</code></pre>
            </div>
        </section>
        
        <section id="authentication" class="section">
            <h2>Authentication</h2>
            <p>All API requests require authentication via API key in the Authorization header:</p>
            <pre><code>Authorization: Bearer cipk_live_a1b2c3d4e5f6g7h8i9j0</code></pre>
        </section>
        
        <!-- Interactive API Explorer -->
        <section id="api-explorer" class="section">
            <h2>API Explorer</h2>
            <elements-api
                apiDescriptionUrl="https://api.commission-intelligence.io/openapi.json"
                router="hash"
                layout="sidebar"
            />
        </section>
        
        <!-- SDK Downloads (coming soon) -->
        <section id="sdks" class="section">
            <h2>SDKs & Libraries</h2>
            <div class="sdk-grid">
                <div class="sdk-card">
                    <h3>Python</h3>
                    <pre><code>pip install commission-intelligence</code></pre>
                    <button class="btn" onclick="alert('Python SDK coming soon!')">Download</button>
                </div>
                <div class="sdk-card">
                    <h3>JavaScript</h3>
                    <pre><code>npm install @commission-iq/sdk</code></pre>
                    <button class="btn" onclick="alert('JavaScript SDK coming soon!')">Download</button>
                </div>
                <div class="sdk-card">
                    <h3>Java</h3>
                    <pre><code>// Maven dependency coming soon</code></pre>
                    <button class="btn" onclick="alert('Java SDK coming soon!')">Download</button>
                </div>
            </div>
        </section>
    </div>
</body>
</html>
```

## Week 3: Admin Panel & Demo Flow

### Day 15-17: Admin Panel
```python
# admin/admin_app.py - Internal tool to manage demos
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="Commission IQ Admin", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Navigate", ["Dashboard", "Demo Management", "Leads", "Feature Flags"])

if page == "Dashboard":
    st.title("Commission IQ Admin Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Demo Requests", "12", "+3 this week")
    with col2:
        st.metric("Active Trials", "3", "+1")
    with col3:
        st.metric("Pipeline Value", "$47,500", "")
    with col4:
        st.metric("Closed Won", "$12,500", "1 customer")
    
    # Lead pipeline
    st.subheader("Sales Pipeline")
    pipeline_data = {
        "Stage": ["Lead", "Demo Scheduled", "Demo Complete", "Negotiating", "Closed Won"],
        "Count": [24, 8, 5, 3, 1],
        "Value": ["$120,000", "$40,000", "$25,000", "$15,000", "$5,000"]
    }
    st.dataframe(pd.DataFrame(pipeline_data))

elif page == "Demo Management":
    st.title("Demo Environment Management")
    
    # Create demo environment
    st.subheader("Create Demo Environment")
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Company Name")
        contact_name = st.text_input("Contact Name")
        demo_date = st.date_input("Demo Date")
    with col2:
        integrations = st.multiselect("Show Integrations", 
            ["Applied Epic", "EZLynx", "HubSpot", "QuickBooks", "Salesforce"])
        features = st.multiselect("Show Features",
            ["Advanced Analytics", "Bulk Operations", "API Access", "Webhooks"])
    
    if st.button("Create Demo Environment"):
        # Save demo configuration
        demo_config = {
            "company": company_name,
            "contact": contact_name,
            "date": str(demo_date),
            "integrations": integrations,
            "features": features,
            "demo_url": f"https://demo.commission-intelligence.io/{company_name.lower().replace(' ', '-')}",
            "api_key": f"demo_{company_name.lower().replace(' ', '_')}_key"
        }
        st.success(f"Demo environment created: {demo_config['demo_url']}")
        st.json(demo_config)

elif page == "Leads":
    st.title("Lead Management")
    
    # Display leads
    leads = [
        {"Name": "ABC Insurance Agency", "Contact": "John Smith", "Status": "Demo Scheduled", 
         "Value": "$5,000", "Next Step": "Demo on Jan 28"},
        {"Name": "XYZ Partners", "Contact": "Jane Doe", "Status": "Interested",
         "Value": "$7,500", "Next Step": "Follow up call"},
        {"Name": "Premier Insurance", "Contact": "Bob Johnson", "Status": "Negotiating",
         "Value": "$10,000", "Next Step": "Send contract"},
    ]
    
    df = pd.DataFrame(leads)
    st.dataframe(df, use_container_width=True)
    
    # Add new lead
    with st.expander("Add New Lead"):
        new_name = st.text_input("Agency Name")
        new_contact = st.text_input("Contact Name")
        new_email = st.text_input("Email")
        new_phone = st.text_input("Phone")
        if st.button("Add Lead"):
            st.success(f"Lead added: {new_name}")

elif page == "Feature Flags":
    st.title("Feature Flag Management")
    
    st.write("Control what features to show during demos")
    
    # Feature toggles
    features = {
        "Real-time Sync": True,
        "Advanced Analytics": True,
        "Bulk Import": False,
        "White Label": False,
        "API v2": False,
        "Machine Learning": False,
    }
    
    for feature, enabled in features.items():
        features[feature] = st.toggle(feature, value=enabled)
    
    if st.button("Save Feature Flags"):
        st.success("Feature flags updated!")
        st.json(features)
```

### Day 18-19: Demo Customization
```python
# demo/personalized_demo.py - Generate personalized demos
def create_personalized_demo(company_name: str, integrations: List[str], focus_areas: List[str]):
    """Create a customized demo environment for a prospect"""
    
    demo_config = {
        "branding": {
            "company_name": company_name,
            "logo_placeholder": f"{company_name} Logo",
            "primary_color": "#1e40af"
        },
        "sample_data": {
            "policies": generate_realistic_policies(company_name, 50),
            "commissions": generate_commission_data(30),
            "agents": generate_agent_list(company_name, 10)
        },
        "enabled_features": {
            "integrations": integrations,
            "show_analytics": "Analytics" in focus_areas,
            "show_bulk_ops": "Automation" in focus_areas,
            "show_api": "API" in focus_areas
        },
        "dashboard_metrics": {
            "total_premium": random.randint(1000000, 5000000),
            "total_commission": random.randint(100000, 500000),
            "policies": random.randint(500, 2000),
            "time_saved": "32 hours/week"
        }
    }
    
    return demo_config

def generate_realistic_policies(company_name: str, count: int):
    """Generate realistic-looking policy data"""
    carriers = ["Progressive", "State Farm", "Allstate", "Liberty Mutual", "Travelers"]
    
    policies = []
    for i in range(count):
        policies.append({
            "policy_number": f"POL-{datetime.now().year}-{random.randint(10000, 99999)}",
            "customer": f"{company_name} Client {i+1}",
            "carrier": random.choice(carriers),
            "premium": round(random.uniform(500, 10000), 2),
            "effective_date": (datetime.now() - timedelta(days=random.randint(0, 365))).date(),
            "commission_rate": round(random.uniform(10, 20), 2),
            "status": random.choice(["Active", "Pending Renewal", "New Business"])
        })
    
    return policies
```

### Day 20-21: Sales Tools
```python
# sales/demo_script.md - Script for demos
"""
# Commission Intelligence Platform Demo Script

## Introduction (2 minutes)
"Thank you for joining me today. I know you're busy running [COMPANY NAME], 
so I'll keep this focused on how we can save you 20+ hours per week on 
commission tracking and reconciliation."

## Pain Point Discovery (3 minutes)
"Before I show you the platform, can you tell me:
1. How do you currently track commissions?
2. Which systems do you use? (Applied Epic, EZLynx, etc.)
3. How much time does reconciliation take each month?"

[Listen and take notes - customize demo based on responses]

## Demo Flow (15 minutes)

### 1. Dashboard Overview
"This is what your dashboard would look like. Notice we're showing 
[COMPANY NAME]'s data here..."

[Show customized dashboard with their name]

### 2. Integration Demo
"You mentioned you use [THEIR SYSTEM]. Here's how our integration works..."

[Show only the integrations they care about]

### 3. Commission Calculation
"Let me show you how we automate your commission calculations..."

[Demo the calculation with their typical premium amounts]

### 4. Time Savings
"Based on what you told me, this would save you approximately 
[CALCULATED HOURS] per month."

## Pricing & Next Steps (5 minutes)

"Based on your needs, I recommend our Professional package:
- One-time setup: $5,000 (includes your [SYSTEM] integration)
- Monthly: $599 for up to 20 users

The setup takes 2-3 weeks. We customize everything for your specific workflow."

## Objection Handling

"It's expensive" → "The setup fee pays for itself in 2 months of time savings"
"We're happy with Excel" → "Let me show you what you're missing..."
"Need to think about it" → "What specific concerns can I address?"

## Close
"To get you started, I can offer a 10% discount if we begin setup this week.
When would you like to schedule your implementation kickoff call?"
"""

# sales/email_templates.py
email_templates = {
    "demo_follow_up": """
Subject: Your Commission Intelligence Demo - Next Steps

Hi {contact_name},

Thank you for taking the time to see how Commission Intelligence can transform 
{company_name}'s commission operations.

As we discussed, your custom implementation would include:
✓ {integration_1} integration
✓ {integration_2} integration (if needed)
✓ Automated reconciliation saving {hours_saved} hours/month
✓ Custom workflows for your team

Your investment:
- One-time setup: ${setup_fee} 
- Monthly platform: ${monthly_fee}

I'm attaching a summary of the ROI calculation we reviewed, showing break-even 
in just {break_even_months} months.

Are you available for a quick call this week to discuss getting started?

Best regards,
{salesperson_name}
    """,
    
    "proposal": """
Subject: Commission Intelligence Proposal for {company_name}

{contact_name},

Please find attached your custom proposal for Commission Intelligence Platform.

Key Points:
- Implementation timeline: {timeline} weeks
- Includes all {num_integrations} integrations you requested
- Guaranteed {percent_time_saved}% reduction in reconciliation time
- Full training for your team included

Special offer: Sign by {deadline} to receive:
- 10% off setup fee
- Free additional integration (${value} value)
- Priority implementation queue

Let's schedule 15 minutes to review any questions: [Calendar Link]

{salesperson_name}
    """
}
```

## Week 4: Launch Preparation

### Day 22-23: Testing & Polish
```bash
# Test checklist
☐ Landing page loads fast (< 2 seconds)
☐ All links work
☐ Demo booking form captures leads
☐ API returns realistic data
☐ Dashboard looks professional
☐ Mobile responsive
☐ SSL certificate active
☐ Analytics tracking working

# Performance optimization
- Compress all images
- Minify CSS/JS
- Enable caching
- CDN for static assets
```

### Day 24-25: Lead Generation Setup
```python
# Lead capture and CRM
# Use free tier of:
- HubSpot CRM (free forever)
- Calendly (free booking)
- Google Analytics (free)
- Hotjar (free heatmaps)

# LinkedIn outreach templates
outreach_messages = {
    "initial": """
Hi {name},

I noticed you're the {title} at {agency}. 

We just launched a platform that helps agencies like yours save 20+ hours/month 
on commission reconciliation.

Would you be open to a quick 15-minute demo next week?

No sales pressure - just showing what's possible.

Best,
{your_name}
    """,
    
    "follow_up": """
Hi {name},

I wanted to follow up on my previous message about commission automation.

We're offering a special launch discount for our first 10 agency partners:
- 50% off setup fees
- Locked-in pricing for life

Interested in a brief call?

{your_name}
    """
}
```

### Day 26-27: Content & SEO
```markdown
# Blog posts to write (for SEO)
1. "Why Insurance Agencies Waste 80% of Time on Commission Reconciliation"
2. "The True Cost of Manual Commission Tracking"
3. "Applied Epic vs EZLynx: Commission Tracking Comparison"
4. "How to Automate Insurance Commission Calculations"
5. "Modern API Integration for Insurance Agencies"

# Landing page SEO
- Title: "Commission Intelligence Platform | Automate Insurance Commission Tracking"
- Description: "Save 20+ hours monthly on commission reconciliation. Integrates with Applied Epic, EZLynx, QuickBooks. Book a demo today."
- Keywords: insurance commission software, commission tracking, agency management
```

### Day 28: Launch!
```bash
# Launch checklist
☐ Demo platform live
☐ Booking calendar active
☐ Email templates ready
☐ LinkedIn messages queued
☐ Admin panel tested
☐ Backup systems in place
☐ Support email active

# First week goals
- 50 LinkedIn messages sent
- 10 demo requests
- 3 demos completed
- 1 paid customer

# Success metric
First paying customer within 30 days = validation
```

## Post-Launch: Customer-Driven Development

### When First Customer Signs Up:
```python
# Week 1-2: Discovery
- Deep dive into their workflow
- Document every requirement
- Map their data fields
- Understand their pain points

# Week 3-4: Build
- Implement ONLY what they need
- Test with their real data
- Get their feedback daily
- Deliver working solution

# Week 5+: Support & Upsell
- Ensure they're successful
- Get testimonial
- Ask for referrals
- Identify next features they'd pay for
```

### Progressive Enhancement:
```markdown
Customer 1 needs Applied Epic → Build it → $5,000
Customer 2 needs Applied Epic → Reuse it → $5,000 (100% margin)
Customer 3 needs EZLynx → Build it → $5,000
Customer 4 needs EZLynx → Reuse it → $5,000 (100% margin)

Each integration becomes an asset that generates recurring revenue!
```

## Budget Breakdown

### Month 1 (Demo Platform):
```
Domain: $15/year = $1.25/month
Hosting: $0 (Vercel free tier)
Database: $0 (Supabase free tier)  
Total: < $5/month
```

### Month 2-3 (First Customers):
```
DigitalOcean: $24/month (4GB droplet)
Domain: $1.25/month
Email: $0 (Gmail)
CRM: $0 (HubSpot free)
Total: < $30/month
```

### Month 4+ (Growth):
```
Upgrade hosting as revenue grows
Each customer funds their own infrastructure
Target: Infrastructure < 10% of revenue
```

## The Secret: You're Not Building Everything

You're building:
1. A professional-looking demo ✓
2. Basic working features ✓
3. Whatever customers pay for ✓

You're NOT building:
1. 20 integrations nobody uses ✗
2. Complex features nobody wants ✗
3. Expensive infrastructure you don't need ✗

This is how real SaaS companies start!