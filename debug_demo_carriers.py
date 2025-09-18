"""Debug script to check demo user's carriers and their status values."""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# Load environment variables
load_dotenv()

def get_supabase_client() -> Client:
    """Create Supabase client using environment variables."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")
    
    return create_client(url, key)

def debug_demo_carriers():
    """Debug carriers for demo user."""
    try:
        supabase = get_supabase_client()
        demo_email = "Demo@AgentCommissionTracker.com"
        
        print(f"\n{'='*60}")
        print(f"Debugging carriers for: {demo_email}")
        print(f"{'='*60}\n")
        
        # 1. Get all carriers for demo user
        response = supabase.table('carriers').select("*").eq('user_email', demo_email).execute()
        carriers = response.data if response.data else []
        
        print(f"Total carriers found: {len(carriers)}")
        
        if not carriers:
            print("❌ No carriers found for demo user!")
            return
        
        # 2. Analyze status values
        status_counts = {}
        for carrier in carriers:
            status = carrier.get('status', 'None')
            if status not in status_counts:
                status_counts[status] = 0
            status_counts[status] += 1
        
        print(f"\nStatus distribution:")
        for status, count in sorted(status_counts.items()):
            print(f"  - '{status}': {count} carriers")
        
        # 3. Count active carriers
        active_carriers = [c for c in carriers if c.get('status') == 'Active']
        print(f"\nActive carriers: {len(active_carriers)}")
        
        # 4. Show sample carriers
        print(f"\nFirst 5 carriers (showing key fields):")
        for i, carrier in enumerate(carriers[:5]):
            print(f"\n  Carrier {i+1}:")
            print(f"    - ID: {carrier.get('carrier_id')}")
            print(f"    - Name: {carrier.get('carrier_name')}")
            print(f"    - Status: '{carrier.get('status')}' (type: {type(carrier.get('status'))})")
            print(f"    - Updated: {carrier.get('updated_at')}")
        
        # 5. Check for NULL or missing status
        problem_carriers = [c for c in carriers if not c.get('status') or c.get('status') == '']
        if problem_carriers:
            print(f"\n⚠️  Found {len(problem_carriers)} carriers with NULL/empty status!")
            print("First 3 problem carriers:")
            for carrier in problem_carriers[:3]:
                print(f"  - {carrier.get('carrier_name')} (ID: {carrier.get('carrier_id')})")
        
        # 6. Fix suggestion
        if len(active_carriers) == 0 and len(carriers) > 0:
            print(f"\n🔧 FIX NEEDED: No carriers have 'Active' status!")
            print("Run this SQL to fix:")
            print(f"""
UPDATE carriers 
SET status = 'Active' 
WHERE user_email = '{demo_email}' 
  AND (status IS NULL OR status = '' OR status != 'Active');
            """)
            
        # 7. Check updated_at values for sorting
        print(f"\n📅 Checking updated_at values for sorting:")
        carriers_with_dates = [c for c in carriers if c.get('updated_at')]
        carriers_without_dates = [c for c in carriers if not c.get('updated_at')]
        
        print(f"  - Carriers with updated_at: {len(carriers_with_dates)}")
        print(f"  - Carriers without updated_at: {len(carriers_without_dates)}")
        
        if carriers_without_dates:
            print(f"\n⚠️  Found {len(carriers_without_dates)} carriers without updated_at!")
            print("This will affect sorting in Recent Carriers view.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_demo_carriers()