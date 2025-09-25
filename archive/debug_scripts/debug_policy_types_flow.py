"""
Debug script to trace the policy types data flow issue
"""

import streamlit as st
from database_utils import get_supabase_client
import json

# Initialize Supabase client
supabase = get_supabase_client()

def debug_policy_types():
    print("\n=== DEBUGGING POLICY TYPES DATA FLOW ===\n")
    
    # 1. Check database directly
    print("1. CHECKING DATABASE DIRECTLY:")
    try:
        response = supabase.table('user_policy_types').select('*').execute()
        if response.data:
            for row in response.data:
                print(f"\nUser: {row.get('user_email')}")
                print(f"User ID: {row.get('user_id')}")
                policy_types = row.get('policy_types', [])
                print(f"Policy Types Count: {len(policy_types)}")
                if policy_types and len(policy_types) > 0:
                    print("First few policy types:")
                    for i, pt in enumerate(policy_types[:5]):
                        print(f"  - {pt}")
                        if i >= 4:
                            print(f"  ... and {len(policy_types) - 5} more")
                            break
                print(f"Raw policy_types data type: {type(policy_types)}")
                print(f"Is list: {isinstance(policy_types, list)}")
                print(f"Is empty: {not policy_types}")
        else:
            print("No data found in user_policy_types table")
    except Exception as e:
        print(f"Error querying database: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. Test the UserPolicyTypes class directly
    print("2. TESTING UserPolicyTypes CLASS:")
    from user_policy_types_db import UserPolicyTypes
    
    upt = UserPolicyTypes()
    
    # Mock session state
    st.session_state['user_email'] = 'patrickstabell@outlook.com'
    st.session_state['user_id'] = '89a3d8d1-bbe2-4cce-961e-e765c0598237'
    
    print(f"Session state user_email: {st.session_state.get('user_email')}")
    print(f"Session state user_id: {st.session_state.get('user_id')}")
    
    try:
        # Clear cache to force fresh load
        upt._types_cache = None
        upt._cache_user_id = None
        
        result = upt.get_user_policy_types()
        print(f"\nResult from get_user_policy_types():")
        print(f"Type: {type(result)}")
        print(f"Keys: {list(result.keys())}")
        policy_types = result.get('policy_types', [])
        print(f"Policy types count: {len(policy_types)}")
        print(f"Policy types type: {type(policy_types)}")
        if policy_types:
            print("First few policy types:")
            for i, pt in enumerate(policy_types[:3]):
                print(f"  - {pt}")
    except Exception as e:
        print(f"Error calling get_user_policy_types: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*50 + "\n")
    
    # 3. Test with specific email query
    print("3. TESTING SPECIFIC EMAIL QUERY:")
    try:
        response = supabase.table('user_policy_types').select('*').eq('user_email', 'patrickstabell@outlook.com').execute()
        if response.data and len(response.data) > 0:
            types_data = response.data[0]
            print(f"Found data for patrickstabell@outlook.com")
            print(f"Full row keys: {list(types_data.keys())}")
            policy_types = types_data.get('policy_types', [])
            print(f"Policy types from database: {len(policy_types)} items")
            print(f"Type of policy_types field: {type(policy_types)}")
            
            # Check if it might be a JSON string
            if isinstance(policy_types, str):
                print("Policy types is a string, attempting to parse as JSON...")
                try:
                    parsed = json.loads(policy_types)
                    print(f"Successfully parsed JSON, got {len(parsed)} items")
                except:
                    print("Failed to parse as JSON")
        else:
            print("No data found for patrickstabell@outlook.com")
    except Exception as e:
        print(f"Error querying specific email: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_policy_types()