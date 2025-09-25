#!/usr/bin/env python3
"""
Debug script to investigate why policy types aren't displaying in Admin Panel.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_utils import get_supabase_client

def debug_policy_types():
    """Debug policy types display issue."""
    print("=== Policy Types Display Debug ===\n")
    
    try:
        supabase = get_supabase_client()
        
        # Get all policy types from database
        print("1. Fetching all user_policy_types records...")
        response = supabase.table('user_policy_types').select('*').execute()
        
        if response.data:
            print(f"   Found {len(response.data)} records in user_policy_types table\n")
            
            for i, record in enumerate(response.data[:3]):  # Show first 3 records
                print(f"   Record {i+1}:")
                print(f"   - user_email: {record.get('user_email', 'N/A')}")
                print(f"   - user_id: {record.get('user_id', 'N/A')}")
                
                # Check the policy_types field
                policy_types_data = record.get('policy_types', None)
                if policy_types_data is None:
                    print("   - policy_types: NULL/None")
                elif isinstance(policy_types_data, str):
                    print(f"   - policy_types: STRING (length {len(policy_types_data)})")
                    try:
                        parsed = json.loads(policy_types_data)
                        if isinstance(parsed, list):
                            print(f"     -> Parses to list with {len(parsed)} items")
                            if parsed:
                                print(f"     -> First item: {parsed[0]}")
                        else:
                            print(f"     -> Parses to: {type(parsed)}")
                    except json.JSONDecodeError as e:
                        print(f"     -> JSON parse error: {e}")
                        print(f"     -> First 100 chars: {policy_types_data[:100]}")
                elif isinstance(policy_types_data, list):
                    print(f"   - policy_types: LIST with {len(policy_types_data)} items")
                    if policy_types_data:
                        print(f"     -> First item: {policy_types_data[0]}")
                else:
                    print(f"   - policy_types: {type(policy_types_data)}")
                
                # Check other fields
                for field in ['default_type', 'categories', 'version']:
                    if field in record:
                        print(f"   - {field}: {record[field]}")
                
                print()
        else:
            print("   No records found in user_policy_types table")
        
        # Check table schema
        print("\n2. Checking table schema (via a test query)...")
        try:
            # Try to insert a minimal test record and then delete it
            test_data = {
                'user_email': 'schema_test_temp@example.com',
                'policy_types': []
            }
            test_response = supabase.table('user_policy_types').insert(test_data).execute()
            print("   Successfully inserted with minimal fields (user_email, policy_types)")
            
            # Delete the test record
            supabase.table('user_policy_types').delete().eq('user_email', 'schema_test_temp@example.com').execute()
            print("   Test record deleted")
            
            # Try with more fields
            test_data['default_type'] = 'HO3'
            test_data['categories'] = ['Test']
            test_data['version'] = '1.0.0'
            test_response = supabase.table('user_policy_types').insert(test_data).execute()
            print("   Successfully inserted with all fields")
            
            # Delete again
            supabase.table('user_policy_types').delete().eq('user_email', 'schema_test_temp@example.com').execute()
            print("   Test record deleted")
            
        except Exception as e:
            print(f"   Schema test failed: {e}")
            error_msg = str(e)
            if 'column' in error_msg.lower():
                print("   -> This suggests a column doesn't exist in the table")
        
        print("\n3. Testing data retrieval like the app does...")
        # Simulate how the app retrieves data
        test_email = 'patrickstabell@outlook.com'  # Replace with actual email
        response = supabase.table('user_policy_types').select('*').eq('user_email', test_email).execute()
        
        if response.data:
            print(f"   Found data for {test_email}")
            data = response.data[0]
            policy_types_field = data.get('policy_types', [])
            
            print(f"   Type of policy_types field: {type(policy_types_field)}")
            
            if isinstance(policy_types_field, str):
                try:
                    policy_types_list = json.loads(policy_types_field)
                    print(f"   Parsed to: {type(policy_types_list)} with {len(policy_types_list)} items")
                except:
                    print("   Failed to parse JSON")
            elif isinstance(policy_types_field, list):
                print(f"   Already a list with {len(policy_types_field)} items")
                policy_types_list = policy_types_field
            else:
                print(f"   Unexpected type: {type(policy_types_field)}")
                policy_types_list = []
            
            # Check if empty
            if not policy_types_list:
                print("   -> policy_types list is EMPTY! This is why 'No policy types found' appears")
            else:
                print(f"   -> policy_types has {len(policy_types_list)} items")
                print(f"   -> First few items: {policy_types_list[:3]}")
        else:
            print(f"   No data found for {test_email}")
            
    except Exception as e:
        print(f"\nError during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_policy_types()