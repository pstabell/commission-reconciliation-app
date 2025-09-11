"""
Commission Intelligence Platform - Admin Panel
Internal tool for managing demos, leads, and customer configurations
"""
import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta, date
import random
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional
import secrets

# Page configuration
st.set_page_config(
    page_title="Commission IQ Admin",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .metric-card {
        background-color: #f7fafc;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0fdf4;
        border: 1px solid #86efac;
        color: #166534;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'leads' not in st.session_state:
    st.session_state.leads = [
        {
            "id": 1,
            "company": "ABC Insurance Agency",
            "contact": "John Smith",
            "email": "john@abcinsurance.com",
            "phone": "(555) 123-4567",
            "agents": "10-20",
            "status": "Demo Scheduled",
            "value": 5000,
            "demo_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "notes": "Uses Applied Epic, interested in QuickBooks integration",
            "created": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        },
        {
            "id": 2,
            "company": "XYZ Partners",
            "contact": "Jane Doe",
            "email": "jane@xyzpartners.com",
            "phone": "(555) 234-5678",
            "agents": "20-50",
            "status": "Interested",
            "value": 7500,
            "demo_date": None,
            "notes": "Current pain point: manual reconciliation taking 40+ hours/month",
            "created": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
        },
        {
            "id": 3,
            "company": "Premier Insurance Group",
            "contact": "Bob Johnson",
            "email": "bob@premierins.com",
            "phone": "(555) 345-6789",
            "agents": "50+",
            "status": "Negotiating",
            "value": 10000,
            "demo_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "notes": "Wants custom reporting features, Enterprise plan",
            "created": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        }
    ]

if 'demos' not in st.session_state:
    st.session_state.demos = []

if 'feature_flags' not in st.session_state:
    st.session_state.feature_flags = {
        "real_time_sync": True,
        "advanced_analytics": True,
        "bulk_import": False,
        "white_label": False,
        "api_v2": False,
        "ai_insights": False,
        "custom_workflows": True,
        "mobile_app": False
    }

# Sidebar navigation
st.sidebar.title("🎯 Commission IQ Admin")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "Navigate",
    ["Dashboard", "Lead Management", "Demo Builder", "Customer Setup", "Feature Flags", "Sales Tools"]
)

# Dashboard Page
if page == "Dashboard":
    st.title("📊 Admin Dashboard")
    
    # Calculate metrics
    total_pipeline = sum(lead['value'] for lead in st.session_state.leads)
    demos_scheduled = len([l for l in st.session_state.leads if l['status'] == 'Demo Scheduled'])
    negotiating = len([l for l in st.session_state.leads if l['status'] == 'Negotiating'])
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Pipeline Value", f"${total_pipeline:,}", "+15%")
    
    with col2:
        st.metric("Demo Requests", demos_scheduled, f"+{demos_scheduled} this week")
    
    with col3:
        st.metric("In Negotiation", negotiating, "")
    
    with col4:
        st.metric("Close Rate", "33%", "+5%")
    
    # Pipeline chart
    st.subheader("📈 Sales Pipeline")
    
    pipeline_data = pd.DataFrame({
        'Stage': ['Lead', 'Demo Scheduled', 'Demo Complete', 'Negotiating', 'Closed Won', 'Closed Lost'],
        'Count': [8, 3, 2, 1, 1, 1],
        'Value': [40000, 15000, 10000, 10000, 5000, 5000]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.funnel(pipeline_data, x='Value', y='Stage', title="Pipeline by Value")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(pipeline_data, values='Count', names='Stage', title="Leads by Stage")
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activities
    st.subheader("📋 Recent Activities")
    activities = [
        {"Time": "2 hours ago", "Activity": "Demo completed with ABC Insurance", "Type": "Demo"},
        {"Time": "5 hours ago", "Activity": "New lead: Regional Coverage Partners", "Type": "Lead"},
        {"Time": "1 day ago", "Activity": "Contract sent to Premier Insurance", "Type": "Deal"},
        {"Time": "2 days ago", "Activity": "Follow-up call with XYZ Partners", "Type": "Call"},
    ]
    
    for activity in activities:
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            st.write(activity["Time"])
        with col2:
            st.write(activity["Activity"])
        with col3:
            if activity["Type"] == "Demo":
                st.info(activity["Type"])
            elif activity["Type"] == "Lead":
                st.success(activity["Type"])
            else:
                st.warning(activity["Type"])

# Lead Management Page
elif page == "Lead Management":
    st.title("👥 Lead Management")
    
    # Add new lead
    with st.expander("➕ Add New Lead"):
        col1, col2 = st.columns(2)
        
        with col1:
            company = st.text_input("Company Name")
            contact = st.text_input("Contact Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
        
        with col2:
            agents = st.selectbox("Number of Agents", ["1-5", "6-10", "10-20", "20-50", "50+"])
            status = st.selectbox("Status", ["New", "Contacted", "Interested", "Demo Scheduled"])
            value = st.number_input("Deal Value ($)", min_value=1000, step=500, value=5000)
            notes = st.text_area("Notes")
        
        if st.button("Add Lead", type="primary"):
            new_lead = {
                "id": len(st.session_state.leads) + 1,
                "company": company,
                "contact": contact,
                "email": email,
                "phone": phone,
                "agents": agents,
                "status": status,
                "value": value,
                "demo_date": None,
                "notes": notes,
                "created": datetime.now().strftime("%Y-%m-%d")
            }
            st.session_state.leads.append(new_lead)
            st.success(f"✅ Lead added: {company}")
    
    # Display leads
    st.subheader("📋 Current Leads")
    
    # Convert to DataFrame for display
    leads_df = pd.DataFrame(st.session_state.leads)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All"] + list(leads_df['status'].unique()))
    
    # Apply filters
    if status_filter != "All":
        leads_df = leads_df[leads_df['status'] == status_filter]
    
    # Display table
    st.dataframe(
        leads_df[['company', 'contact', 'email', 'agents', 'status', 'value', 'created']],
        use_container_width=True,
        hide_index=True
    )
    
    # Lead actions
    st.subheader("🎯 Lead Actions")
    
    selected_lead = st.selectbox(
        "Select Lead",
        options=[f"{l['company']} - {l['contact']}" for l in st.session_state.leads]
    )
    
    if selected_lead:
        lead_index = [i for i, l in enumerate(st.session_state.leads) if f"{l['company']} - {l['contact']}" == selected_lead][0]
        lead = st.session_state.leads[lead_index]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            new_status = st.selectbox("Update Status", ["New", "Contacted", "Interested", "Demo Scheduled", "Negotiating", "Closed Won", "Closed Lost"], index=["New", "Contacted", "Interested", "Demo Scheduled", "Negotiating", "Closed Won", "Closed Lost"].index(lead['status']))
        
        with col2:
            demo_date = st.date_input("Demo Date", value=pd.to_datetime(lead['demo_date']) if lead['demo_date'] else None)
        
        with col3:
            if st.button("Update Lead", type="primary"):
                st.session_state.leads[lead_index]['status'] = new_status
                st.session_state.leads[lead_index]['demo_date'] = demo_date.strftime("%Y-%m-%d") if demo_date else None
                st.success("✅ Lead updated!")
                st.rerun()

# Demo Builder Page
elif page == "Demo Builder":
    st.title("🎮 Demo Environment Builder")
    
    st.info("Create personalized demo environments for prospects")
    
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input("Company Name", placeholder="ABC Insurance Agency")
        contact_name = st.text_input("Primary Contact", placeholder="John Smith")
        demo_date = st.date_input("Demo Date", value=datetime.now() + timedelta(days=7))
        demo_time = st.time_input("Demo Time", value=datetime.now().time())
    
    with col2:
        integrations = st.multiselect(
            "Show Integrations",
            ["Applied Epic", "EZLynx", "HawkSoft", "HubSpot", "QuickBooks", "Salesforce"],
            default=["Applied Epic", "QuickBooks"]
        )
        
        features = st.multiselect(
            "Highlight Features",
            ["Real-time Sync", "Advanced Analytics", "Bulk Operations", "API Access", "Webhooks", "Custom Reports"],
            default=["Real-time Sync", "Advanced Analytics"]
        )
        
        agent_count = st.select_slider("Number of Agents", options=["5", "10", "20", "50", "100"], value="20")
    
    # Demo customization
    st.subheader("🎨 Demo Customization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        primary_color = st.color_picker("Primary Brand Color", "#3B82F6")
        show_pricing = st.checkbox("Show Pricing", value=True)
        show_roi_calculator = st.checkbox("Include ROI Calculator", value=True)
    
    with col2:
        demo_duration = st.select_slider("Demo Duration", options=["15 min", "30 min", "45 min", "60 min"], value="30 min")
        focus_area = st.radio("Primary Focus", ["Time Savings", "Accuracy", "Integration", "Analytics"])
    
    # Sample data configuration
    st.subheader("📊 Sample Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_premium = st.number_input("Total Premium ($)", min_value=100000, max_value=10000000, value=2500000, step=100000)
    
    with col2:
        commission_rate = st.slider("Avg Commission Rate (%)", min_value=5.0, max_value=20.0, value=12.5, step=0.5)
    
    with col3:
        time_saved = st.slider("Time Saved (hours/month)", min_value=10, max_value=50, value=30, step=5)
    
    if st.button("🚀 Create Demo Environment", type="primary"):
        # Generate demo credentials
        demo_url = f"https://demo.commission-intelligence.io/{company_name.lower().replace(' ', '-')}"
        api_key = f"demo_{company_name.lower().replace(' ', '_')}_{secrets.token_hex(8)}"
        
        demo_config = {
            "company": company_name,
            "contact": contact_name,
            "demo_date": f"{demo_date} {demo_time}",
            "url": demo_url,
            "api_key": api_key,
            "integrations": integrations,
            "features": features,
            "customization": {
                "agent_count": agent_count,
                "primary_color": primary_color,
                "show_pricing": show_pricing,
                "show_roi": show_roi_calculator,
                "focus_area": focus_area
            },
            "sample_data": {
                "total_premium": total_premium,
                "total_commission": total_premium * commission_rate / 100,
                "commission_rate": commission_rate,
                "time_saved": time_saved
            }
        }
        
        st.session_state.demos.append(demo_config)
        
        # Show success message with details
        st.success("✅ Demo environment created successfully!")
        
        with st.expander("📋 Demo Details", expanded=True):
            st.write(f"**Demo URL:** {demo_url}")
            st.write(f"**API Key:** `{api_key}`")
            st.write(f"**Valid Until:** {(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')}")
            
            st.subheader("Share with Prospect")
            email_template = f"""
Hi {contact_name},

Your personalized Commission Intelligence Platform demo is ready!

**Demo Details:**
- Date: {demo_date} at {demo_time}
- Duration: {demo_duration}
- Demo URL: {demo_url}

We've customized the demo to show:
- {', '.join(integrations)} integrations
- {', '.join(features)}

Looking forward to showing you how we can save {company_name} {time_saved} hours per month!

Best regards,
Your Commission IQ Team
            """
            st.text_area("Email Template", value=email_template, height=300)

# Customer Setup Page
elif page == "Customer Setup":
    st.title("🚀 Customer Onboarding")
    
    st.info("Convert closed deals into active customers")
    
    # Customer selection
    won_deals = [l for l in st.session_state.leads if l['status'] == 'Closed Won']
    
    if won_deals:
        selected_customer = st.selectbox(
            "Select Customer to Onboard",
            options=[f"{d['company']} - {d['contact']}" for d in won_deals]
        )
        
        if selected_customer:
            customer = [d for d in won_deals if f"{d['company']} - {d['contact']}" == selected_customer][0]
            
            st.subheader(f"🏢 {customer['company']} Setup")
            
            # Setup wizard
            setup_stage = st.radio(
                "Setup Stage",
                ["Account Creation", "Integration Configuration", "Data Migration", "Training", "Go Live"],
                horizontal=True
            )
            
            if setup_stage == "Account Creation":
                col1, col2 = st.columns(2)
                
                with col1:
                    subdomain = st.text_input("Subdomain", value=customer['company'].lower().replace(' ', '-'))
                    admin_email = st.text_input("Admin Email", value=customer['email'])
                    plan = st.selectbox("Plan", ["Starter", "Professional", "Enterprise"], index=1)
                
                with col2:
                    users = st.number_input("Number of Users", min_value=1, max_value=100, value=10)
                    billing_cycle = st.radio("Billing Cycle", ["Monthly", "Annual"], horizontal=True)
                    start_date = st.date_input("Start Date", value=datetime.now())
                
                if st.button("Create Account", type="primary"):
                    st.success(f"✅ Account created for {customer['company']}")
                    st.write(f"**Login URL:** https://{subdomain}.commission-intelligence.io")
                    st.write(f"**Admin Email:** {admin_email}")
            
            elif setup_stage == "Integration Configuration":
                st.subheader("🔗 Configure Integrations")
                
                available_integrations = {
                    "Applied Epic": {"status": "ready", "time": "2-3 days"},
                    "EZLynx": {"status": "ready", "time": "2-3 days"},
                    "QuickBooks": {"status": "ready", "time": "1-2 days"},
                    "HubSpot": {"status": "ready", "time": "1 day"},
                    "HawkSoft": {"status": "development", "time": "2 weeks"},
                    "Salesforce": {"status": "development", "time": "3 weeks"}
                }
                
                selected_integrations = st.multiselect(
                    "Select Integrations to Configure",
                    list(available_integrations.keys())
                )
                
                for integration in selected_integrations:
                    with st.expander(f"Configure {integration}"):
                        if available_integrations[integration]["status"] == "ready":
                            st.success(f"✅ {integration} is ready to configure")
                            if integration == "Applied Epic":
                                client_id = st.text_input("Client ID", key=f"{integration}_id")
                                client_secret = st.text_input("Client Secret", type="password", key=f"{integration}_secret")
                                st.write(f"**Setup Time:** {available_integrations[integration]['time']}")
                        else:
                            st.warning(f"⏳ {integration} requires development")
                            st.write(f"**Development Time:** {available_integrations[integration]['time']}")
                            if st.button(f"Start {integration} Development", key=f"{integration}_dev"):
                                st.info(f"Development started for {integration}")
    else:
        st.warning("No closed won deals to onboard. Close some deals first!")

# Feature Flags Page
elif page == "Feature Flags":
    st.title("🚦 Feature Flag Management")
    
    st.info("Control which features are visible during demos and for different customer tiers")
    
    # Global feature flags
    st.subheader("🌍 Global Feature Flags")
    
    col1, col2 = st.columns(2)
    
    with col1:
        for feature, enabled in list(st.session_state.feature_flags.items())[:4]:
            st.session_state.feature_flags[feature] = st.checkbox(
                feature.replace('_', ' ').title(),
                value=enabled,
                key=feature
            )
    
    with col2:
        for feature, enabled in list(st.session_state.feature_flags.items())[4:]:
            st.session_state.feature_flags[feature] = st.checkbox(
                feature.replace('_', ' ').title(),
                value=enabled,
                key=feature
            )
    
    # Plan-specific features
    st.subheader("📊 Plan-Specific Features")
    
    plan_features = {
        "Starter": ["basic_reporting", "email_support", "5_users"],
        "Professional": ["advanced_analytics", "api_access", "20_users", "priority_support"],
        "Enterprise": ["white_label", "custom_integrations", "unlimited_users", "sla", "dedicated_support"]
    }
    
    selected_plan = st.selectbox("Select Plan", list(plan_features.keys()))
    
    st.write(f"**{selected_plan} Plan Features:**")
    for feature in plan_features[selected_plan]:
        st.write(f"✅ {feature.replace('_', ' ').title()}")
    
    if st.button("💾 Save Feature Configuration", type="primary"):
        st.success("✅ Feature flags updated successfully!")
        
        # Show current configuration
        with st.expander("Current Configuration"):
            st.json(st.session_state.feature_flags)

# Sales Tools Page
elif page == "Sales Tools":
    st.title("🛠️ Sales Tools & Resources")
    
    tabs = st.tabs(["Email Templates", "Demo Scripts", "Objection Handling", "ROI Calculator"])
    
    with tabs[0]:
        st.subheader("📧 Email Templates")
        
        template_type = st.selectbox(
            "Select Template",
            ["Cold Outreach", "Demo Follow-up", "Proposal", "Contract", "Onboarding Welcome"]
        )
        
        if template_type == "Cold Outreach":
            template = """Subject: Save 20+ Hours Monthly on Commission Reconciliation

Hi {{contact_name}},

I noticed {{company_name}} has {{agent_count}} agents. Most agencies your size waste 20-40 hours monthly on manual commission reconciliation.

Commission Intelligence Platform automates this entire process by:
✓ Syncing with your AMS (Applied Epic, EZLynx, etc.)
✓ Automatically matching carrier statements
✓ Flagging missing commissions instantly

Would you be open to a 15-minute demo next week to see how we're saving agencies like yours ${{monthly_savings}}/month?

Best regards,
{{your_name}}
"""
        
        elif template_type == "Demo Follow-up":
            template = """Subject: Your Commission IQ Demo - Next Steps

Hi {{contact_name}},

Thank you for taking the time to see Commission Intelligence Platform today!

As we discussed, your custom implementation would include:
✓ {{integration_1}} integration
✓ {{integration_2}} integration
✓ Automated reconciliation saving {{hours_saved}} hours/month

Your investment:
- One-time setup: ${{setup_fee}}
- Monthly platform: ${{monthly_fee}}

I'm attaching:
1. ROI calculation showing {{payback_months}} month payback
2. Implementation timeline
3. Customer success stories

Are you available for a quick call this week to discuss getting started?

Best regards,
{{your_name}}
"""
        
        st.text_area("Template", value=template, height=400)
        
        # Variable replacements
        st.subheader("Variables")
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Contact Name", placeholder="John Smith")
            st.text_input("Company Name", placeholder="ABC Insurance")
            st.text_input("Agent Count", placeholder="25")
        
        with col2:
            st.text_input("Monthly Savings", placeholder="3,000")
            st.text_input("Your Name", placeholder="Sarah Johnson")
    
    with tabs[1]:
        st.subheader("📋 Demo Script")
        
        script = """# Commission Intelligence Platform Demo Script

## Introduction (2 minutes)
"Thank you for joining me today, {{contact_name}}. I know you're busy running {{company_name}}, so I'll keep this focused on how we can save you {{time_estimate}} hours per month on commission tracking and reconciliation."

## Pain Point Discovery (3 minutes)
1. "How are you currently tracking commissions?"
2. "Which systems do you use? (Applied Epic, EZLynx, etc.)"
3. "How much time does reconciliation take each month?"
4. "What's your biggest frustration with the current process?"

[LISTEN AND TAKE NOTES - Customize demo based on responses]

## Demo Flow (15 minutes)

### 1. Dashboard Overview (3 minutes)
"This is what your dashboard would look like. Notice we're showing {{company_name}}'s data here..."
- Show total premium and commission
- Highlight time savings metric
- Show agent leaderboard

### 2. Integration Demo (5 minutes)
"You mentioned you use {{their_system}}. Here's how our integration works..."
- Show real-time sync
- Demonstrate automatic reconciliation
- Show error detection

### 3. ROI Demonstration (5 minutes)
"Based on what you told me about {{specific_pain_point}}..."
- Calculate time savings
- Show cost savings
- Demonstrate accuracy improvements

### 4. Quick Win (2 minutes)
"Here's something you could implement on day one..."
- Show one specific feature that solves their biggest pain

## Pricing & Close (5 minutes)

"Based on your needs with {{agent_count}} agents and {{integrations}} integrations, I recommend our Professional package:"

- Setup: ${{setup_fee}} (one-time)
- Monthly: ${{monthly_fee}}

"The setup fee includes:"
- Custom configuration for {{company_name}}
- {{integration_list}} integrations
- Team training
- Dedicated support during onboarding

## Trial Close
"On a scale of 1-10, where would you say you are in terms of moving forward with Commission IQ?"

[If 7 or higher]: "Great! What would it take to get you to a 10?"
[If 6 or lower]: "I understand. What concerns do you have that I can address?"

## Next Steps
"Our next step would be to:"
1. Send you the agreement
2. Schedule implementation kickoff (Week of {{date}})
3. Begin {{first_integration}} integration
4. Have you live within {{timeline}}

"Does {{suggested_date}} work for our kickoff call?"
"""
        
        st.text_area("Demo Script", value=script, height=600)
    
    with tabs[2]:
        st.subheader("🎯 Objection Handling")
        
        objections = {
            "It's too expensive": {
                "response": "I understand price is a concern. Let's break down the ROI: You're currently spending {{hours}} hours at ${{hourly_rate}}/hour on reconciliation. That's ${{monthly_cost}}/month. Our solution at ${{our_price}}/month actually saves you ${{savings}}/month, paying for itself in {{payback}} months.",
                "follow_up": "Would it help if we could start with just one integration to prove the value?"
            },
            "We're happy with our current process": {
                "response": "That's great that you have a working process! Many of our customers felt the same way until they realized they were leaving money on the table. On average, we help agencies find ${{missing_commissions}}/month in missing commissions. Would finding an extra ${{annual_amount}}/year be valuable to {{company_name}}?",
                "follow_up": "What if I could show you exactly where you might have missing commissions right now?"
            },
            "We don't have time to implement": {
                "response": "I completely understand - you're busy running your agency. That's exactly why we handle the entire implementation. Our team does all the heavy lifting: setup, integration, data migration, and training. You'll spend less time on implementation than you currently spend on reconciliation in a single week.",
                "follow_up": "We can start with a pilot - just one carrier or one line of business. Would that be more manageable?"
            },
            "Need to think about it": {
                "response": "Of course, this is an important decision. To help with your evaluation, what specific concerns can I address right now? Is it the price, the implementation process, or something else?",
                "follow_up": "While you're evaluating, would it be helpful to connect you with {{similar_customer}} who was in a similar situation?"
            }
        }
        
        selected_objection = st.selectbox("Select Objection", list(objections.keys()))
        
        if selected_objection:
            st.write("**Response:**")
            st.info(objections[selected_objection]["response"])
            
            st.write("**Follow-up:**")
            st.success(objections[selected_objection]["follow_up"])
    
    with tabs[3]:
        st.subheader("💰 ROI Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            agents = st.number_input("Number of Agents", min_value=1, max_value=100, value=20)
            hours_per_month = st.number_input("Hours Spent on Reconciliation", min_value=10, max_value=100, value=40)
            hourly_rate = st.number_input("Hourly Rate ($)", min_value=20, max_value=100, value=50)
            missing_commission_pct = st.slider("Est. Missing Commissions (%)", 0.0, 5.0, 2.0, 0.5)
        
        with col2:
            total_premium = st.number_input("Monthly Premium ($)", min_value=100000, max_value=10000000, value=1000000, step=10000)
            avg_commission_rate = st.slider("Avg Commission Rate (%)", 5.0, 20.0, 12.0, 0.5)
            our_monthly_fee = st.number_input("Our Monthly Fee ($)", min_value=299, max_value=2999, value=599)
            setup_fee = st.number_input("Setup Fee ($)", min_value=2500, max_value=10000, value=5000, step=500)
        
        # Calculate ROI
        monthly_time_cost = hours_per_month * hourly_rate
        time_savings = monthly_time_cost * 0.8  # 80% time savings
        
        monthly_commission = total_premium * avg_commission_rate / 100
        missing_commission_recovery = monthly_commission * missing_commission_pct / 100
        
        total_monthly_savings = time_savings + missing_commission_recovery
        net_monthly_savings = total_monthly_savings - our_monthly_fee
        
        payback_months = setup_fee / net_monthly_savings if net_monthly_savings > 0 else 999
        annual_roi = (net_monthly_savings * 12 - setup_fee) / (setup_fee + our_monthly_fee * 12) * 100
        
        # Display results
        st.markdown("---")
        st.subheader("📊 ROI Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Monthly Time Savings", f"${time_savings:,.0f}", f"{hours_per_month * 0.8:.0f} hours")
        
        with col2:
            st.metric("Commission Recovery", f"${missing_commission_recovery:,.0f}/mo", f"${missing_commission_recovery * 12:,.0f}/yr")
        
        with col3:
            st.metric("Net Monthly Savings", f"${net_monthly_savings:,.0f}", f"${net_monthly_savings * 12:,.0f}/yr")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Payback Period", f"{payback_months:.1f} months", "")
        
        with col2:
            st.metric("Annual ROI", f"{annual_roi:.0f}%", "")
        
        # Summary box
        if net_monthly_savings > 0:
            st.success(f"""
            **Investment Summary for {agents} agents:**
            - You'll save ${total_monthly_savings:,.0f}/month
            - Net savings after our fee: ${net_monthly_savings:,.0f}/month
            - Break even in {payback_months:.1f} months
            - Year 1 net benefit: ${net_monthly_savings * 12 - setup_fee:,.0f}
            """)
        else:
            st.warning("Adjust the parameters to see positive ROI")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Commission IQ Admin Panel v1.0")
st.sidebar.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")