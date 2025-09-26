"""
Commission Intelligence Platform - API Application
Built on api-platform branch - does not touch main app
"""
import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import json

# Import shared utilities from main app (read-only)
import sys
sys.path.append('..')
from column_mapping_config import column_mapper, get_mapped_column
from commission_app import get_supabase_client, load_policies_data, format_currency

# Load environment variables
load_dotenv()

# API Platform specific configurations
st.set_page_config(
    page_title="Commission Intelligence Platform - API Dashboard",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check if API platform is enabled
API_PLATFORM_ENABLED = os.getenv("API_PLATFORM_ENABLED", "false").lower() == "true"

def check_api_access():
    """Check if user has API platform access."""
    if not API_PLATFORM_ENABLED:
        st.error("🔒 API Platform is not enabled. Please contact support.")
        st.stop()
    
    # Check if user is logged in (reuse main app session)
    if not st.session_state.get("password_correct", False):
        st.warning("Please login through the main application first.")
        st.stop()
    
    return True

def display_api_header():
    """Display API platform header."""
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background-color: #f0f0f0; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: #0066cc;'>🔌 Commission Intelligence Platform</h1>
            <p style='color: #666;'>API Dashboard & Developer Portal</p>
        </div>
        """, unsafe_allow_html=True)

def show_api_dashboard():
    """Main API dashboard showing usage and metrics."""
    st.title("📊 API Dashboard")
    
    # Get user's API usage data
    user_email = st.session_state.get("user_email", "demo@example.com")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("API Calls Today", "2,847", "+12%")
    
    with col2:
        st.metric("Active Webhooks", "5", "+1")
    
    with col3:
        st.metric("Response Time", "142ms", "-8ms")
    
    with col4:
        st.metric("Success Rate", "99.7%", "+0.2%")
    
    st.divider()
    
    # API Usage Chart
    st.subheader("📈 API Usage (Last 7 Days)")
    
    # Sample data for demo
    dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    usage_data = pd.DataFrame({
        'Date': dates,
        'API Calls': [2100, 2400, 2650, 2300, 2800, 2600, 2847],
        'Webhook Events': [120, 145, 160, 130, 180, 165, 190]
    })
    
    st.line_chart(usage_data.set_index('Date'))
    
    st.divider()
    
    # Recent API Activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🕒 Recent API Calls")
        recent_calls = pd.DataFrame({
            'Time': ['2 min ago', '5 min ago', '12 min ago', '15 min ago', '22 min ago'],
            'Endpoint': ['/policies', '/commissions/calculate', '/policies/123', '/webhooks/trigger', '/analytics/agent'],
            'Method': ['GET', 'POST', 'PUT', 'POST', 'GET'],
            'Status': ['200', '201', '200', '200', '200'],
            'Duration': ['89ms', '234ms', '67ms', '156ms', '298ms']
        })
        st.dataframe(recent_calls, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("🔔 Recent Webhook Events")
        webhook_events = pd.DataFrame({
            'Time': ['1 min ago', '8 min ago', '25 min ago', '1 hour ago', '2 hours ago'],
            'Event': ['policy.created', 'commission.calculated', 'policy.renewed', 'reconciliation.completed', 'policy.created'],
            'Endpoint': ['https://agency.com/hook', 'https://crm.co/webhook', 'https://agency.com/hook', 'https://accounting.io/api', 'https://agency.com/hook'],
            'Status': ['Delivered', 'Delivered', 'Delivered', 'Pending', 'Delivered']
        })
        st.dataframe(webhook_events, use_container_width=True, hide_index=True)

def show_api_keys():
    """Manage API keys."""
    st.title("🔑 API Key Management")
    
    # Create new API key section
    with st.expander("➕ Create New API Key", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            key_name = st.text_input("Key Name", placeholder="Production API Key")
            permissions = st.multiselect(
                "Permissions",
                ["policies:read", "policies:write", "commissions:read", "commissions:write", 
                 "analytics:read", "webhooks:write"],
                default=["policies:read", "commissions:read"]
            )
        with col2:
            rate_limit = st.number_input("Rate Limit (calls/hour)", value=1000, min_value=100, max_value=10000)
            expires = st.date_input("Expiration Date (Optional)", value=None)
        
        if st.button("Generate API Key", type="primary"):
            # Generate mock API key
            import secrets
            new_key = f"ck_{secrets.token_urlsafe(32)}"
            st.success(f"✅ API Key Created!")
            st.code(new_key)
            st.warning("⚠️ Save this key securely - it won't be shown again!")
    
    st.divider()
    
    # Existing API keys
    st.subheader("📋 Active API Keys")
    
    api_keys = pd.DataFrame({
        'Name': ['Production API', 'Development API', 'Mobile App Key', 'CRM Integration'],
        'Key': ['ck_1a2b3c...def', 'ck_4e5f6g...hij', 'ck_7k8l9m...nop', 'ck_0q1r2s...tuv'],
        'Permissions': ['Full Access', 'Read Only', 'policies:read, commissions:read', 'Full Access'],
        'Rate Limit': ['5000/hr', '1000/hr', '2000/hr', '5000/hr'],
        'Last Used': ['2 minutes ago', '1 hour ago', '3 hours ago', 'Yesterday'],
        'Created': ['Jan 15, 2025', 'Jan 10, 2025', 'Dec 28, 2024', 'Dec 15, 2024'],
        'Status': ['🟢 Active', '🟢 Active', '🟢 Active', '🟢 Active']
    })
    
    # Display with actions
    for idx, row in api_keys.iterrows():
        col1, col2, col3, col4, col5 = st.columns([3, 3, 2, 2, 2])
        with col1:
            st.text(row['Name'])
            st.caption(row['Key'])
        with col2:
            st.text(row['Permissions'])
            st.caption(f"Rate: {row['Rate Limit']}")
        with col3:
            st.text(row['Last Used'])
            st.caption(f"Created: {row['Created']}")
        with col4:
            st.text(row['Status'])
        with col5:
            if st.button("🗑️ Revoke", key=f"revoke_{idx}"):
                st.error(f"Key {row['Key']} has been revoked!")

def show_webhooks():
    """Manage webhooks."""
    st.title("🔔 Webhook Management")
    
    # Create webhook section
    with st.expander("➕ Register New Webhook", expanded=False):
        webhook_url = st.text_input("Webhook URL", placeholder="https://your-domain.com/webhook")
        
        events = st.multiselect(
            "Subscribe to Events",
            ["policy.created", "policy.updated", "policy.renewed", "policy.cancelled",
             "commission.calculated", "commission.paid", "reconciliation.completed",
             "renewal.upcoming", "renewal.missed"],
            default=["policy.created", "commission.calculated"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            secret = st.text_input("Webhook Secret (for signature verification)", type="password")
        with col2:
            retry_policy = st.selectbox("Retry Policy", ["Standard (3x)", "Extended (5x)", "No Retry"])
        
        if st.button("Register Webhook", type="primary"):
            st.success("✅ Webhook registered successfully!")
            st.info("Test event sent to verify endpoint.")
    
    st.divider()
    
    # Active webhooks
    st.subheader("📋 Active Webhooks")
    
    webhooks = pd.DataFrame({
        'URL': ['https://agency.com/webhook', 'https://crm.example.com/api/webhook', 'https://accounting.io/webhooks/commission'],
        'Events': ['All Events', 'policy.*, commission.*', 'commission.paid, reconciliation.*'],
        'Status': ['🟢 Active', '🟢 Active', '🟡 Warning'],
        'Success Rate': ['99.8%', '100%', '87.2%'],
        'Last Triggered': ['5 minutes ago', '1 hour ago', '3 hours ago']
    })
    
    for idx, row in webhooks.iterrows():
        col1, col2, col3, col4, col5 = st.columns([4, 3, 2, 2, 2])
        with col1:
            st.text(row['URL'])
            st.caption(row['Events'])
        with col2:
            st.text(f"Success: {row['Success Rate']}")
            st.caption(row['Last Triggered'])
        with col3:
            st.text(row['Status'])
        with col4:
            if st.button("🧪 Test", key=f"test_{idx}"):
                st.info("Test event sent!")
        with col5:
            if st.button("🗑️ Delete", key=f"delete_{idx}"):
                st.error("Webhook deleted!")

def show_api_docs():
    """Show API documentation."""
    st.title("📚 API Documentation")
    
    # API Overview
    st.markdown("""
    ## Overview
    
    The Commission Intelligence Platform API provides programmatic access to your commission data, 
    enabling seamless integration with your agency's tech stack.
    
    **Base URL**: `https://api.commissiontracker.io/v1`  
    **Authentication**: Bearer token (API Key)  
    **Rate Limits**: Based on your plan (default 1000/hour)
    """)
    
    # Quick Start
    with st.expander("🚀 Quick Start", expanded=True):
        st.markdown("""
        ### 1. Get your API Key
        Navigate to API Keys section and generate a new key.
        
        ### 2. Make your first request
        ```bash
        curl -X GET https://api.commissiontracker.io/v1/policies \\
          -H "Authorization: Bearer YOUR_API_KEY" \\
          -H "Content-Type: application/json"
        ```
        
        ### 3. Handle the response
        ```json
        {
          "data": [
            {
              "id": "123",
              "policy_number": "HOME-456789",
              "effective_date": "2025-09-01",
              "premium": 1200.00,
              "commission": 144.00
            }
          ],
          "meta": {
            "page": 1,
            "total": 150
          }
        }
        ```
        """)
    
    # Endpoints
    st.subheader("📍 Available Endpoints")
    
    endpoints = {
        "Policies": [
            ("GET /policies", "List all policies"),
            ("GET /policies/:id", "Get specific policy"),
            ("POST /policies", "Create new policy"),
            ("PUT /policies/:id", "Update policy"),
            ("DELETE /policies/:id", "Delete policy")
        ],
        "Commissions": [
            ("GET /commissions", "List commissions"),
            ("POST /commissions/calculate", "Calculate commission"),
            ("POST /commissions/reconcile", "Reconcile statement"),
            ("GET /commissions/pending", "Get pending commissions")
        ],
        "Analytics": [
            ("GET /analytics/summary", "Commission summary"),
            ("GET /analytics/agent/:id", "Agent performance"),
            ("GET /analytics/trends", "Commission trends")
        ],
        "Webhooks": [
            ("POST /webhooks", "Register webhook"),
            ("GET /webhooks", "List webhooks"),
            ("DELETE /webhooks/:id", "Delete webhook")
        ]
    }
    
    for category, items in endpoints.items():
        st.markdown(f"### {category}")
        for endpoint, description in items:
            col1, col2 = st.columns([2, 3])
            with col1:
                st.code(endpoint)
            with col2:
                st.markdown(description)

def show_playground():
    """Interactive API playground."""
    st.title("🎮 API Playground")
    st.markdown("Test API endpoints interactively")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE"])
        endpoint = st.selectbox(
            "Endpoint",
            ["/policies", "/policies/123", "/commissions/calculate", "/analytics/summary", "/webhooks"]
        )
        
        if method in ["POST", "PUT"]:
            st.text_area("Request Body", value='{\n  "key": "value"\n}', height=150)
        
        if st.button("Send Request", type="primary", use_container_width=True):
            st.success("✅ Request sent!")
    
    with col2:
        st.markdown("### Response")
        st.code("""
{
  "status": 200,
  "data": {
    "policies": [
      {
        "id": "123",
        "policy_number": "HOME-456789",
        "customer": "John Doe",
        "premium": 1200.00,
        "commission": 144.00,
        "status": "active"
      }
    ]
  },
  "meta": {
    "total": 1,
    "page": 1,
    "per_page": 20
  }
}
        """, language="json")

def main():
    """Main API Platform application."""
    check_api_access()
    
    # Sidebar navigation
    st.sidebar.title("🔌 API Platform")
    
    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "API Keys",
            "Webhooks",
            "Documentation",
            "Playground",
            "Settings"
        ]
    )
    
    # Add back link to main app
    st.sidebar.divider()
    st.sidebar.info("📱 [Back to Main App](../)")
    
    # Page routing
    if page == "Dashboard":
        display_api_header()
        show_api_dashboard()
    elif page == "API Keys":
        display_api_header()
        show_api_keys()
    elif page == "Webhooks":
        display_api_header()
        show_webhooks()
    elif page == "Documentation":
        display_api_header()
        show_api_docs()
    elif page == "Playground":
        display_api_header()
        show_playground()
    elif page == "Settings":
        display_api_header()
        st.title("⚙️ API Settings")
        st.info("Configure rate limits, CORS, and security settings here.")

if __name__ == "__main__":
    main()