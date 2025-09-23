"""
Fix for MGA Policy Type Commission Initialization

This script provides a solution for the "column policy_types does not exist" error
by working with the existing commission_rules table structure.
"""

import streamlit as st
from supabase import Client
import os

def initialize_mga_commission_rules(supabase: Client, mga_id: str, user_email: str, user_id: str = None):
    """
    Initialize commission rules for all policy types for a specific MGA
    using the existing commission_rules table structure.
    """
    # Default policy types and their commission rates
    default_policy_types = [
        {"code": "GL", "name": "General Liability", "new_rate": 10, "renewal_rate": 10},
        {"code": "WC", "name": "Workers Compensation", "new_rate": 10, "renewal_rate": 10},
        {"code": "BOP", "name": "Business Owners Policy", "new_rate": 12, "renewal_rate": 12},
        {"code": "AUTO", "name": "Auto", "new_rate": 12, "renewal_rate": 12},
        {"code": "HOME", "name": "Homeowners", "new_rate": 12, "renewal_rate": 12},
        {"code": "FLOOD", "name": "Flood", "new_rate": 15, "renewal_rate": 15},
        {"code": "WIND", "name": "Wind/Hurricane", "new_rate": 15, "renewal_rate": 15},
        {"code": "UMBR", "name": "Umbrella", "new_rate": 15, "renewal_rate": 15},
        {"code": "OTHER", "name": "Other", "new_rate": 10, "renewal_rate": 10},
    ]
    
    created_count = 0
    errors = []
    
    for policy_type in default_policy_types:
        try:
            # Create commission rule for this policy type
            rule_data = {
                "mga_id": mga_id,
                "policy_type": policy_type["name"],  # Use full name instead of code
                "new_rate": policy_type["new_rate"],
                "renewal_rate": policy_type["renewal_rate"],
                "state": "FL",  # Default to Florida
                "rule_description": f"Default rate for {policy_type['name']}",
                "is_active": True,
                "user_email": user_email
            }
            
            if user_id:
                rule_data["user_id"] = user_id
            
            # Check if rule already exists
            existing = supabase.table('commission_rules').select("*").eq('mga_id', mga_id).eq('policy_type', policy_type["name"]).eq('user_email', user_email).execute()
            
            if not existing.data:
                # Insert new rule
                supabase.table('commission_rules').insert(rule_data).execute()
                created_count += 1
                
        except Exception as e:
            errors.append(f"Error creating rule for {policy_type['name']}: {str(e)}")
    
    return created_count, errors


def add_mga_commission_initialization_button(mga_id: str, mga_name: str):
    """
    Add this to your Streamlit app where you need the initialization button.
    """
    st.subheader(f"Commission Rules for {mga_name}")
    
    # Check if MGA has any commission rules
    supabase = st.session_state.get('supabase_client')
    if not supabase:
        st.error("Database connection not available")
        return
    
    user_email = st.session_state.get('user_email', '').lower()
    user_id = st.session_state.get('user_id')
    
    # Get existing rules
    existing_rules = supabase.table('commission_rules').select("*").eq('mga_id', mga_id).eq('user_email', user_email).execute()
    
    if not existing_rules.data:
        st.warning(f"No commission rules found for {mga_name}")
        
        if st.button("🚀 Initialize All Policy Types", type="primary", key=f"init_mga_{mga_id}"):
            with st.spinner("Creating commission rules..."):
                created_count, errors = initialize_mga_commission_rules(
                    supabase, 
                    mga_id, 
                    user_email, 
                    user_id
                )
                
                if created_count > 0:
                    st.success(f"✅ Created {created_count} commission rules for {mga_name}")
                    st.rerun()
                
                if errors:
                    st.error("Some errors occurred:")
                    for error in errors:
                        st.error(f"• {error}")
    else:
        # Show existing rules
        st.info(f"Found {len(existing_rules.data)} commission rules")
        
        # Display rules in a table
        rules_data = []
        for rule in existing_rules.data:
            rules_data.append({
                "Policy Type": rule.get('policy_type', 'All'),
                "New Rate": f"{rule.get('new_rate', 0)}%",
                "Renewal Rate": f"{rule.get('renewal_rate', 0)}%",
                "State": rule.get('state', 'FL'),
                "Active": "✅" if rule.get('is_active', True) else "❌"
            })
        
        if rules_data:
            st.dataframe(rules_data, use_container_width=True)


# Alternative: Fix for the existing button that's causing the error
def fix_existing_initialization_button():
    """
    Replace the problematic initialization code with this working version.
    """
    # This would replace the code that's trying to access mga_policy_type_commissions
    # Look for something like:
    # supabase.table('mga_policy_type_commissions').select('policy_types')
    
    # Replace with:
    # Get policy types from user_policy_types table instead
    user_email = st.session_state.get('user_email', '').lower()
    response = supabase.table('user_policy_types').select("*").eq('user_email', user_email).execute()
    
    if response.data and len(response.data) > 0:
        policy_types = response.data[0].get('policy_types', [])
        # Process policy types...
    else:
        st.warning("No policy types found. Please initialize policy types first.")