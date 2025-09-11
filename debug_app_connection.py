"""
Debug script to test why carriers/MGAs aren't showing in the Streamlit app
This mimics exactly what the app does when loading carriers
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def get_supabase_client():
    """Get Supabase client - exactly as the app does it."""
    app_mode = os.getenv("APP_ENVIRONMENT")
    
    if app_mode == "PRODUCTION":
        # Use production database credentials
        url = os.getenv("PRODUCTION_SUPABASE_URL", os.getenv("SUPABASE_URL"))
        key = os.getenv("PRODUCTION_SUPABASE_ANON_KEY", os.getenv("SUPABASE_ANON_KEY"))
        print("🔵 Using PRODUCTION credentials")
    else:
        # Use personal database credentials (default)
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        print("🟢 Using PERSONAL database credentials")
    
    print(f"URL: {url[:30]}..." if url else "❌ No URL found")
    print(f"Key type: {'ANON_KEY' if 'anon' in str(key).lower() else 'SERVICE_KEY' if key else '❌ No key'}")
    
    if not url or not key:
        raise Exception("Missing Supabase credentials")
    
    return create_client(url, key)

def test_carriers_load():
    """Test loading carriers exactly as commission_app.py does it"""
    
    print("\n=== Testing Carrier Load (App Method) ===\n")
    
    try:
        supabase = get_supabase_client()
        print("✅ Supabase client created\n")
        
        # Line 12838-12839 from commission_app.py
        print("Running: supabase.table('carriers').select('*').execute()")
        response = supabase.table('carriers').select("*").execute()
        carriers_data = response.data if response.data else []
        
        print(f"\nResult: Found {len(carriers_data)} carriers")
        
        if carriers_data:
            print("\nFirst 5 carriers:")
            for carrier in carriers_data[:5]:
                print(f"  - {carrier['carrier_name']} (ID: {carrier['carrier_id']}, Status: {carrier.get('status', 'Active')})")
            
            # Check what load_carriers_for_dropdown would return
            print("\n\nTesting load_carriers_for_dropdown() logic:")
            active_carriers = [c for c in carriers_data if c.get('status', 'Active') == 'Active']
            print(f"Active carriers for dropdown: {len(active_carriers)}")
        else:
            print("\n❌ No carriers found!")
            print("\nPossible issues:")
            print("1. Wrong database (check APP_ENVIRONMENT)")
            print("2. RLS blocking access (if using ANON key)")
            print("3. Empty table in this environment")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")

def test_direct_query():
    """Test with both ANON and SERVICE keys if available"""
    print("\n\n=== Testing Different Key Types ===\n")
    
    # Test with ANON key
    url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    
    if url and anon_key:
        try:
            print("1. Testing with ANON key:")
            client = create_client(url, anon_key)
            response = client.table('carriers').select("carrier_id, carrier_name").execute()
            print(f"   ✅ ANON key can see {len(response.data)} carriers")
        except Exception as e:
            print(f"   ❌ ANON key error: {str(e)}")
    
    # Test with SERVICE key if available
    service_key = os.getenv("SUPABASE_KEY")
    if url and service_key and service_key != anon_key:
        try:
            print("\n2. Testing with SERVICE key:")
            client = create_client(url, service_key)
            response = client.table('carriers').select("carrier_id, carrier_name").execute()
            print(f"   ✅ SERVICE key can see {len(response.data)} carriers")
        except Exception as e:
            print(f"   ❌ SERVICE key error: {str(e)}")

if __name__ == "__main__":
    print("APP_ENVIRONMENT:", os.getenv("APP_ENVIRONMENT", "Not set (defaults to PERSONAL)"))
    test_carriers_load()
    test_direct_query()