"""Test webhook locally to debug issues."""
import os
from webhook_server import app, get_supabase_client

# Test Supabase connection
print("Testing Supabase connection...")
print(f"PRODUCTION_SUPABASE_URL: {os.getenv('PRODUCTION_SUPABASE_URL', 'Not set')}")
print(f"PRODUCTION_SUPABASE_ANON_KEY: {'Set' if os.getenv('PRODUCTION_SUPABASE_ANON_KEY') else 'Not set'}")

client = get_supabase_client()
if client:
    print("✓ Supabase client created successfully")
    try:
        # Try to query users table
        result = client.table('users').select("*").limit(1).execute()
        print(f"✓ Successfully queried users table")
    except Exception as e:
        print(f"✗ Error querying users table: {e}")
else:
    print("✗ Failed to create Supabase client")

# Test the webhook endpoint exists
with app.test_client() as c:
    response = c.get('/health')
    print(f"\nHealth check: {response.get_json()}")