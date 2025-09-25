#!/usr/bin/env python3
"""
Debug script to check why user_policy_types data isn't being retrieved.
"""

import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_utils import get_supabase_client

# Test data
test_user_id = "89a3d8d1-bbe2-4cce-961e-e765c0598237"
test_email = "patrickstabell@outlook.com"

print("=== Debugging User Policy Types Retrieval ===")
print(f"\nTest user_id: {test_user_id}")
print(f"Test email: {test_email}")

# Initialize Supabase client
supabase = get_supabase_client()

print("\n1. Checking database directly...")

# Test 1: Query by user_id
print("\n   a) Query by user_id:")
try:
    response = supabase.table('user_policy_types').select('*').eq('user_id', test_user_id).execute()
    if response.data:
        print(f"   ✓ Found {len(response.data)} records by user_id")
        for idx, record in enumerate(response.data):
            print(f"\n   Record {idx + 1}:")
            print(f"   - id: {record.get('id')}")
            print(f"   - user_id: {record.get('user_id')}")
            print(f"   - user_email: {record.get('user_email')}")
            print(f"   - created_at: {record.get('created_at')}")
            policy_types = record.get('policy_types', [])
            print(f"   - policy_types type: {type(policy_types)}")
            print(f"   - policy_types count: {len(policy_types) if isinstance(policy_types, list) else 'N/A'}")
            if isinstance(policy_types, list) and len(policy_types) > 0:
                print(f"   - First policy type: {policy_types[0]}")
    else:
        print("   ✗ No records found by user_id")
except Exception as e:
    print(f"   ✗ Error querying by user_id: {e}")

# Test 2: Query by user_email
print("\n   b) Query by user_email (lowercase):")
try:
    response = supabase.table('user_policy_types').select('*').eq('user_email', test_email.lower()).execute()
    if response.data:
        print(f"   ✓ Found {len(response.data)} records by user_email")
    else:
        print("   ✗ No records found by user_email")
except Exception as e:
    print(f"   ✗ Error querying by user_email: {e}")

# Test 3: Query by case-insensitive email
print("\n   c) Query by user_email (case-insensitive):")
try:
    response = supabase.table('user_policy_types').select('*').ilike('user_email', test_email).execute()
    if response.data:
        print(f"   ✓ Found {len(response.data)} records by ilike user_email")
    else:
        print("   ✗ No records found by ilike user_email")
except Exception as e:
    print(f"   ✗ Error querying by ilike user_email: {e}")

# Test 4: Test the actual retrieval logic
print("\n2. Testing UserPolicyTypes class logic...")

# Import the class
from user_policy_types_db import UserPolicyTypes

# Create instance
upt = UserPolicyTypes()

# Simulate session state
import streamlit as st
if 'user_id' not in st.session_state:
    st.session_state.user_id = test_user_id
if 'user_email' not in st.session_state:
    st.session_state.user_email = test_email

print(f"\n   Session state set:")
print(f"   - user_id: {st.session_state.get('user_id')}")
print(f"   - user_email: {st.session_state.get('user_email')}")

# Test get_user_policy_types
print("\n   Testing get_user_policy_types()...")
try:
    result = upt.get_user_policy_types()
    print(f"\n   Result type: {type(result)}")
    print(f"   Result keys: {list(result.keys())}")
    
    policy_types = result.get('policy_types', [])
    print(f"\n   policy_types type: {type(policy_types)}")
    print(f"   policy_types count: {len(policy_types)}")
    
    if policy_types:
        print(f"   First 3 policy types: {policy_types[:3]}")
    else:
        print("   ✗ policy_types is empty!")
        
    # Check cache
    print(f"\n   Cache status:")
    print(f"   - _types_cache: {'Set' if upt._types_cache else 'Not set'}")
    print(f"   - _cache_user_id: {upt._cache_user_id}")
    
except Exception as e:
    print(f"   ✗ Error in get_user_policy_types(): {e}")
    import traceback
    traceback.print_exc()

# Test 5: Check what happens in the Admin Panel display logic
print("\n3. Testing Admin Panel display logic...")
full_config = result if 'result' in locals() else {}
all_policy_types = full_config.get('policy_types', [])

print(f"\n   all_policy_types = {type(all_policy_types)}")
print(f"   len(all_policy_types) = {len(all_policy_types)}")
print(f"   bool(all_policy_types) = {bool(all_policy_types)}")

if all_policy_types:
    print("   -> Would show policy types table")
else:
    print("   -> Would show 'No policy types found' warning")

print("\n=== Debug Summary ===")
print("\nThe issue is likely one of:")
print("1. Empty policy_types array in database")
print("2. Session state not properly set")
print("3. Cache returning stale data")
print("4. Query not finding the user record")
print("\nCheck the output above to identify the specific issue.")