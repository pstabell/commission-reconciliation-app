"""
Debug script to test commission rules loading
Run this to see what error is being hidden
"""

import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Simulate the app's logic
print("=== Debugging Commission Rules Loading ===\n")

# Check environment
app_env = os.getenv("APP_ENVIRONMENT")
print(f"1. APP_ENVIRONMENT: '{app_env}' (empty means personal mode)")

# Create Supabase client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

if not url or not key:
    print("❌ Missing Supabase credentials!")
    exit(1)

supabase = create_client(url, key)
print(f"2. Supabase client created")

# Test the exact logic from commission_app.py lines 12861-12865
print("\n3. Testing commission rules query...")

try:
    # This is what should run in personal mode
    if app_env == "PRODUCTION":
        print("   - Would run PRODUCTION mode query (filtered by user_email)")
        print("   - But APP_ENVIRONMENT is not 'PRODUCTION', so skipping...")
    else:
        print("   - Running PERSONAL mode query (unfiltered)...")
        response = supabase.table('commission_rules').select("*").execute()
        commission_rules = response.data if response.data else []
        print(f"   ✅ Success! Found {len(commission_rules)} commission rules")
        
        if commission_rules:
            print(f"\n4. Sample rule:")
            rule = commission_rules[0]
            print(f"   - Rule ID: {rule.get('rule_id')}")
            print(f"   - Carrier ID: {rule.get('carrier_id')}")
            print(f"   - New Rate: {rule.get('new_rate')}%")
            print(f"   - Renewal Rate: {rule.get('renewal_rate')}%")
        
except Exception as e:
    print(f"   ❌ ERROR: {type(e).__name__}: {str(e)}")
    print(f"\n   This error is being silently caught in the app!")
    print(f"   That's why you can't see your commission rules.")
    
    # Check if it's an RLS issue
    if "permission denied" in str(e).lower():
        print("\n   🔒 This looks like an RLS issue on commission_rules table.")
        print("   Run: ALTER TABLE commission_rules DISABLE ROW LEVEL SECURITY;")

print("\n=== Summary ===")
print("The app should show all your commission rules in personal mode.")
print("If they're not showing, check for errors above.")