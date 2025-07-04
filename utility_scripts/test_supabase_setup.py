import os
import sys
from datetime import datetime

# Try to import supabase, install if not available
try:
    from supabase import create_client, Client
except ImportError:
    print("Installing supabase-py...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "supabase"])
    from supabase import create_client, Client

# Try to import python-dotenv, install if not available
try:
    from dotenv import load_dotenv
except ImportError:
    print("Installing python-dotenv...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase credentials
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_ANON_KEY not found in .env file")
    sys.exit(1)

print("Testing Supabase connection...")
print(f"URL: {url}")
print(f"Key: {key[:20]}...")

try:
    # Create Supabase client
    supabase: Client = create_client(url, key)
    print("Successfully connected to Supabase\!")
    
    print("\\nChecking database schema...")
    
    # Test 1: Check if policies table exists
    print("\\n1. Testing policies table:")
    try:
        result = supabase.table("policies").select("*").limit(1).execute()
        print("   Table policies exists")
        print("   - Columns available for query")
    except Exception as e:
        print(f"   Error accessing policies table: {str(e)}")
    
    # Test 2: Check other tables
    tables_to_check = ["commission_payments", "manual_commission_entries", "renewal_history"]
    
    for table in tables_to_check:
        print(f"\\n2. Testing {table} table:")
        try:
            result = supabase.table(table).select("*").limit(1).execute()
            print(f"   Table {table} exists")
        except Exception as e:
            print(f"   Error accessing {table} table: {str(e)}")
    
    print("\\nSupabase connection test completed\!")
    
except Exception as e:
    print(f"\\nFailed to connect to Supabase: {str(e)}")
