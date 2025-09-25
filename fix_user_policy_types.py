#!/usr/bin/env python3
"""
Quick fix to populate empty policy_types for specific user.
"""

import os
import json

# Direct database query using psql
user_id = "89a3d8d1-bbe2-4cce-961e-e765c0598237"
user_email = "patrickstabell@outlook.com"

# Default policy types
default_policy_types = [
    {'code': 'AUTOP', 'name': 'AUTOP', 'active': True, 'category': 'Other'},
    {'code': 'HOME', 'name': 'HOME', 'active': True, 'category': 'Personal Property'},
    {'code': 'DFIRE', 'name': 'DFIRE', 'active': True, 'category': 'Personal Property'},
    {'code': 'WC', 'name': 'WC', 'active': True, 'category': 'Other'},
    {'code': 'AUTOB', 'name': 'AUTOB', 'active': True, 'category': 'Other'},
    {'code': 'GL', 'name': 'GL', 'active': True, 'category': 'Other'},
    {'code': 'FLOOD', 'name': 'FLOOD', 'active': True, 'category': 'Specialty'},
    {'code': 'BOAT', 'name': 'BOAT', 'active': True, 'category': 'Specialty'},
    {'code': 'CONDO', 'name': 'CONDO', 'active': True, 'category': 'Personal Property'},
    {'code': 'PROP-C', 'name': 'PROP-C', 'active': True, 'category': 'Other'},
    {'code': 'PACKAGE-P', 'name': 'PACKAGE-P', 'active': True, 'category': 'Other'},
    {'code': 'UMB-P', 'name': 'UMB-P', 'active': True, 'category': 'Other'},
    {'code': 'IM-C', 'name': 'IM-C', 'active': True, 'category': 'Other'},
    {'code': 'GARAGE', 'name': 'GARAGE', 'active': True, 'category': 'Other'},
    {'code': 'UMB-C', 'name': 'UMB-C', 'active': True, 'category': 'Other'},
    {'code': 'OCEAN MARINE', 'name': 'OCEAN MARINE', 'active': True, 'category': 'Other'},
    {'code': 'WIND-P', 'name': 'WIND-P', 'active': True, 'category': 'Other'},
    {'code': 'PL', 'name': 'PL', 'active': True, 'category': 'Other'},
    {'code': 'COLLECTOR', 'name': 'COLLECTOR', 'active': True, 'category': 'Other'},
    {'code': 'PACKAGE-C', 'name': 'PACKAGE-C', 'active': True, 'category': 'Commercial'},
    {'code': 'FLOOD-C', 'name': 'FLOOD-C', 'active': True, 'category': 'Other'},
    {'code': 'BOP', 'name': 'BOP', 'active': True, 'category': 'Commercial'},
    {'code': 'BPP', 'name': 'BPP', 'active': True, 'category': 'Other'},
    {'code': 'EXCESS', 'name': 'EXCESS', 'active': True, 'category': 'Other'},
    {'code': 'CYBER', 'name': 'CYBER', 'active': True, 'category': 'Commercial'},
    {'code': 'D&O', 'name': 'D&O', 'active': True, 'category': 'Other'},
    {'code': 'CYCLE', 'name': 'CYCLE', 'active': True, 'category': 'Personal Auto'},
    {'code': 'AUTO', 'name': 'AUTO', 'active': True, 'category': 'Personal Auto'},
    {'code': 'RV', 'name': 'RV', 'active': True, 'category': 'Personal Auto'},
    {'code': 'RENTERS', 'name': 'RENTERS', 'active': True, 'category': 'Personal Property'},
    {'code': 'UMBRELLA', 'name': 'UMBRELLA-C', 'active': True, 'category': 'Commercial'},
    {'code': 'MOBILE', 'name': 'MOBILE', 'active': True, 'category': 'Personal Property'},
    {'code': 'WIND', 'name': 'WIND', 'active': True, 'category': 'Specialty'},
    {'code': 'UMBRELLA-P', 'name': 'UMBRELLA-P', 'active': True, 'category': 'Personal'}
]

# Convert to JSON string
policy_types_json = json.dumps(default_policy_types)

# SQL update query
sql_query = f"""
UPDATE user_policy_types 
SET policy_types = '{policy_types_json}'::jsonb
WHERE user_id = '{user_id}' 
  AND (policy_types IS NULL OR policy_types = '[]'::jsonb OR jsonb_array_length(policy_types) = 0);
"""

print("=== Fix User Policy Types ===")
print(f"\nUser ID: {user_id}")
print(f"User Email: {user_email}")
print("\nSQL Query to run:")
print(sql_query)

print("\n\nTo fix the issue, run this query in your database.")
print("\nAlternatively, you can:")
print("1. Log into the app as this user")
print("2. Go to Admin Panel > Policy Types Management")
print("3. Click 'Initialize Default Policy Types' button")