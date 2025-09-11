"""
Test script to debug why carriers/MGAs aren't showing in the Streamlit app
Run this as a standalone Python script to test the connection
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def test_supabase_connection():
    """Test the connection and data retrieval"""
    
    print("=== Testing Supabase Connection ===\n")
    
    # Get credentials
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    print(f"1. Supabase URL: {url[:30]}..." if url else "❌ No SUPABASE_URL found")
    print(f"2. Supabase Key: {'✅ Found' if key else '❌ No SUPABASE_KEY found'}")
    
    if not url or not key:
        print("\n❌ Missing credentials. Check your .env file")
        return
    
    try:
        # Create client
        supabase: Client = create_client(url, key)
        print("\n3. ✅ Supabase client created successfully")
        
        # Test carriers query
        print("\n=== Testing Carriers Table ===")
        try:
            carriers_response = supabase.table('carriers').select("*").execute()
            print(f"✅ Carriers query successful")
            print(f"   - Found {len(carriers_response.data)} carriers")
            if carriers_response.data:
                print(f"   - First carrier: {carriers_response.data[0]['carrier_name']}")
                print(f"   - Sample carriers: {', '.join([c['carrier_name'] for c in carriers_response.data[:5]])}")
        except Exception as e:
            print(f"❌ Error querying carriers: {str(e)}")
        
        # Test MGAs query
        print("\n=== Testing MGAs Table ===")
        try:
            mgas_response = supabase.table('mgas').select("*").execute()
            print(f"✅ MGAs query successful")
            print(f"   - Found {len(mgas_response.data)} MGAs")
            if mgas_response.data:
                print(f"   - First MGA: {mgas_response.data[0]['mga_name']}")
                print(f"   - Sample MGAs: {', '.join([m['mga_name'] for m in mgas_response.data[:5]])}")
        except Exception as e:
            print(f"❌ Error querying MGAs: {str(e)}")
        
        # Test commission rules query
        print("\n=== Testing Commission Rules Table ===")
        try:
            rules_response = supabase.table('commission_rules').select("*").execute()
            print(f"✅ Commission rules query successful")
            print(f"   - Found {len(rules_response.data)} rules")
        except Exception as e:
            print(f"❌ Error querying commission rules: {str(e)}")
        
        # Test with explicit RLS bypass (if using service role key)
        print("\n=== Testing RLS Impact ===")
        print("If using service role key, RLS should be bypassed")
        print("If using anon key, RLS policies apply")
        
    except Exception as e:
        print(f"\n❌ Failed to create Supabase client: {str(e)}")
        print("\nPossible issues:")
        print("1. Wrong credentials in .env file")
        print("2. Network/firewall blocking connection")
        print("3. Supabase project is paused or deleted")

if __name__ == "__main__":
    test_supabase_connection()