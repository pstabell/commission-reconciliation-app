"""
Quick test to verify commission rules are loading correctly
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Check environment
print(f"APP_ENVIRONMENT: {os.getenv('APP_ENVIRONMENT', 'Not set (defaults to personal)')}")

# Create client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

if not url or not key:
    print("Missing Supabase credentials!")
    exit(1)

supabase = create_client(url, key)

print("\n=== Testing Commission Rules Loading ===\n")

# Test 1: Load all rules (what should happen in personal mode)
try:
    response = supabase.table('commission_rules').select("*").execute()
    rules = response.data if response.data else []
    print(f"✅ Unfiltered query: Found {len(rules)} commission rules")
    
    if rules:
        print("\nFirst rule sample:")
        print(f"  Rule ID: {rules[0].get('rule_id')}")
        print(f"  Carrier ID: {rules[0].get('carrier_id')}")
        print(f"  Policy Type: {rules[0].get('policy_type', 'Default')}")
        print(f"  New Rate: {rules[0].get('new_rate')}%")
        print(f"  Renewal Rate: {rules[0].get('renewal_rate')}%")
except Exception as e:
    print(f"❌ Error loading rules: {e}")

# Test 2: Check if filtering by non-existent column causes issues
print("\n\nTesting filtered query (simulating production mode):")
try:
    response = supabase.table('commission_rules').select("*").eq('user_email', 'test@example.com').execute()
    print(f"❌ This should have failed! The user_email column doesn't exist.")
except Exception as e:
    print(f"✅ Expected error: {e}")
    print("   The app is trying to filter by a column that doesn't exist!")

print("\n\n=== SOLUTION ===")
print("The app should NOT filter commission rules in personal mode.")
print("Since APP_ENVIRONMENT is not set to 'PRODUCTION', it should load all rules.")
print("\nIf rules aren't showing, the issue might be:")
print("1. The commission_rules table is empty")
print("2. RLS is enabled on commission_rules")
print("3. There's an error being silently caught (line 12866-12867 in commission_app.py)")