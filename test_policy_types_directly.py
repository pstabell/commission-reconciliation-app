"""
Direct test to see the policy types issue
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# First, let's check what's in the database directly using SQL
print("=== DIRECT DATABASE CHECK ===\n")

# We'll use the database credentials directly
from dotenv import load_dotenv
load_dotenv()

import requests
import json

# Get Supabase URL and key from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Missing SUPABASE_URL or SUPABASE_KEY in environment variables")
    sys.exit(1)

# Make a direct REST API call to Supabase
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Query for the specific user
url = f"{SUPABASE_URL}/rest/v1/user_policy_types?user_email=eq.patrickstabell@outlook.com"
response = requests.get(url, headers=headers)

print(f"Response status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Number of records: {len(data)}")
    
    if data:
        record = data[0]
        print(f"\nRecord found:")
        print(f"  user_email: {record.get('user_email')}")
        print(f"  user_id: {record.get('user_id')}")
        
        policy_types = record.get('policy_types')
        print(f"\nPolicy types field:")
        print(f"  Type: {type(policy_types)}")
        print(f"  Raw value (first 500 chars): {str(policy_types)[:500]}")
        
        # Try to understand the structure
        if isinstance(policy_types, list):
            print(f"  List length: {len(policy_types)}")
            if policy_types:
                print(f"  First item type: {type(policy_types[0])}")
                print(f"  First item: {policy_types[0]}")
        elif isinstance(policy_types, str):
            print("  It's a string, trying to parse as JSON...")
            try:
                parsed = json.loads(policy_types)
                print(f"  Parsed type: {type(parsed)}")
                print(f"  Parsed length: {len(parsed) if hasattr(parsed, '__len__') else 'N/A'}")
            except Exception as e:
                print(f"  JSON parse error: {e}")
else:
    print(f"Error response: {response.text}")

print("\n" + "="*50 + "\n")

# Now test the actual class behavior by inspecting it
print("=== TESTING CLASS BEHAVIOR ===\n")

try:
    # Import and examine the UserPolicyTypes class
    from user_policy_types_db import UserPolicyTypes
    import inspect
    
    # Check the get_user_policy_types method
    print("Examining get_user_policy_types method...")
    method_source = inspect.getsource(UserPolicyTypes.get_user_policy_types)
    
    # Look for the specific lines that handle empty policy_types
    if "if not result['policy_types']:" in method_source:
        print("Found check for empty policy_types in the code")
        print("This might be triggering if the list is being evaluated as falsy")
    
    # Check what happens with an empty list
    print("\nTesting empty list behavior:")
    test_list = []
    print(f"  Empty list: {test_list}")
    print(f"  not test_list: {not test_list}")
    print(f"  bool(test_list): {bool(test_list)}")
    
except Exception as e:
    print(f"Error examining class: {e}")
    import traceback
    traceback.print_exc()