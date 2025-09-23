#!/usr/bin/env python3
"""
Debug script to investigate policy type addition failures.
This script simulates the policy type addition process to identify the issue.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_policy_types_db import UserPolicyTypes
import streamlit as st

# Simulate session state
st.session_state['user_email'] = 'test@example.com'
st.session_state['user_id'] = None

# Create instance
upt = UserPolicyTypes()

print("=== Policy Types Debug Script ===\n")

# Get current configuration
config = upt.get_user_policy_types()
print(f"Total policy types in config: {len(config['policy_types'])}")
print(f"Default type: {config['default']}")
print(f"Version: {config['version']}")

# Check if AUTOP exists
autop_exists = any(pt['code'] == 'AUTOP' for pt in config['policy_types'])
print(f"\nDoes AUTOP already exist? {autop_exists}")

if autop_exists:
    autop_entry = next(pt for pt in config['policy_types'] if pt['code'] == 'AUTOP')
    print(f"Existing AUTOP entry: {autop_entry}")

# Get the list of active policy types (what the UI shows)
active_types = upt.get_policy_types_list()
print(f"\nActive policy types shown in UI: {len(active_types)}")
print(f"First 10 active types: {active_types[:10]}")

# Try to add AUTOP
print("\n=== Attempting to add AUTOP ===")
result = upt.add_policy_type('AUTOP', 'Personal Auto')
print(f"Result of adding AUTOP: {result}")
print("Expected: False (because AUTOP already exists in defaults)")

# Try to add a truly new type
print("\n=== Attempting to add a new type TESTABC ===")
result = upt.add_policy_type('TESTABC', 'Test ABC Type')
print(f"Result of adding TESTABC: {result}")

# Check the configuration after adding
if result:
    config_after = upt.get_user_policy_types()
    testabc_exists = any(pt['code'] == 'TESTABC' for pt in config_after['policy_types'])
    print(f"TESTABC exists after adding: {testabc_exists}")
    print(f"Total types after adding: {len(config_after['policy_types'])}")

print("\n=== Summary ===")
print("1. The default configuration includes AUTOP")
print("2. Users cannot add a policy type that already exists")
print("3. The UI needs to show existing types more clearly")
print("4. The remove_policy_type method is missing and needs to be implemented")