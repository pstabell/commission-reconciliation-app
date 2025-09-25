"""
Simplified debug script to check policy types issue
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock streamlit session state
class MockSessionState:
    def __init__(self):
        self.data = {}
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __contains__(self, key):
        return key in self.data

# Create mock
import sys
sys.modules['streamlit'] = type(sys)('streamlit')
sys.modules['streamlit'].session_state = MockSessionState()

# Now import the actual code
from database_utils import get_supabase_client
import json

# Initialize Supabase client
supabase = get_supabase_client()

def debug_policy_types():
    print("\n=== DEBUGGING POLICY TYPES ISSUE ===\n")
    
    # 1. Check database directly for patrickstabell@outlook.com
    print("1. DIRECT DATABASE QUERY:")
    try:
        response = supabase.table('user_policy_types').select('*').eq('user_email', 'patrickstabell@outlook.com').execute()
        if response.data and len(response.data) > 0:
            types_data = response.data[0]
            print(f"Found data for patrickstabell@outlook.com")
            print(f"Full row keys: {list(types_data.keys())}")
            
            policy_types = types_data.get('policy_types', [])
            print(f"\nPolicy types field:")
            print(f"  - Type: {type(policy_types)}")
            print(f"  - Is None: {policy_types is None}")
            print(f"  - Length: {len(policy_types) if policy_types else 'N/A'}")
            
            # Print raw value to see what we're dealing with
            print(f"\nRaw policy_types value (first 200 chars):")
            print(f"{str(policy_types)[:200]}...")
            
            # Check if it's actually a list with data
            if isinstance(policy_types, list) and len(policy_types) > 0:
                print(f"\nFirst policy type item:")
                print(f"  Type: {type(policy_types[0])}")
                print(f"  Value: {policy_types[0]}")
                
                # Check structure of first item
                if isinstance(policy_types[0], dict):
                    print(f"  Keys: {list(policy_types[0].keys())}")
        else:
            print("No data found for patrickstabell@outlook.com")
    except Exception as e:
        print(f"Error querying database: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*50 + "\n")
    
    # 2. Test the class behavior
    print("2. TESTING UserPolicyTypes CLASS BEHAVIOR:")
    
    # Mock the session state
    sys.modules['streamlit'].session_state['user_email'] = 'patrickstabell@outlook.com'
    sys.modules['streamlit'].session_state['user_id'] = '89a3d8d1-bbe2-4cce-961e-e765c0598237'
    
    from user_policy_types_db import UserPolicyTypes
    
    upt = UserPolicyTypes()
    # Clear cache
    upt._types_cache = None
    upt._cache_user_id = None
    
    try:
        # Call the actual method
        result = upt.get_user_policy_types()
        print(f"Result from get_user_policy_types():")
        print(f"  Type: {type(result)}")
        print(f"  Keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
        
        if isinstance(result, dict):
            policy_types = result.get('policy_types', [])
            print(f"  policy_types count: {len(policy_types)}")
            if policy_types and len(policy_types) > 0:
                print(f"  First policy type: {policy_types[0]}")
    except Exception as e:
        print(f"Error calling get_user_policy_types: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_policy_types()