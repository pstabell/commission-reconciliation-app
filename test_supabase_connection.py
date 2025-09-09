"""Test script to verify Supabase connection and user creation"""
import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime

# Load environment variables
load_dotenv()

# Test connection
print("Testing Supabase connection...")
print(f"URL exists: {bool(os.getenv('PRODUCTION_SUPABASE_URL') or os.getenv('SUPABASE_URL'))}")
print(f"Key exists: {bool(os.getenv('PRODUCTION_SUPABASE_ANON_KEY') or os.getenv('SUPABASE_ANON_KEY'))}")

url = os.getenv("PRODUCTION_SUPABASE_URL", os.getenv("SUPABASE_URL"))
key = os.getenv("PRODUCTION_SUPABASE_ANON_KEY", os.getenv("SUPABASE_ANON_KEY"))

if not url or not key:
    print("❌ ERROR: Supabase credentials not found!")
    print("Make sure these are set in your .env file:")
    print("  - PRODUCTION_SUPABASE_URL or SUPABASE_URL")
    print("  - PRODUCTION_SUPABASE_ANON_KEY or SUPABASE_ANON_KEY")
    exit(1)

try:
    supabase = create_client(url, key)
    print("✅ Connected to Supabase!")
    
    # Test 1: Check existing users
    print("\nChecking users table...")
    result = supabase.table('users').select("email, subscription_status, created_at").execute()
    print(f"Found {len(result.data)} users")
    for user in result.data:
        print(f"  - {user['email']} | Status: {user['subscription_status']} | Created: {user.get('created_at', 'N/A')}")
    
    # Test 2: Try to insert a test user
    test_email = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"
    print(f"\nTesting user creation with: {test_email}")
    
    user_data = {
        'email': test_email,
        'stripe_customer_id': 'cus_test123',
        'subscription_id': 'sub_test123',
        'subscription_status': 'active',
        'subscription_tier': 'legacy',
        'created_at': datetime.now().isoformat()
    }
    
    insert_result = supabase.table('users').insert(user_data).execute()
    print("✅ Test user created successfully!")
    
    # Clean up test user
    supabase.table('users').delete().eq('email', test_email).execute()
    print("✅ Test user cleaned up")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print(f"Error type: {type(e).__name__}")