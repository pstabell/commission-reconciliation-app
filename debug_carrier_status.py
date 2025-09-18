#!/usr/bin/env python3

import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def check_carrier_status():
    # Get all carriers for demo user
    print("Fetching carriers for Demo@AgentCommissionTracker.com...")
    
    response = supabase.table('carriers').select("*").eq('user_email', 'Demo@AgentCommissionTracker.com').execute()
    carriers = response.data if response.data else []
    
    print(f"\nTotal carriers found: {len(carriers)}")
    
    # Count by status
    status_counts = {}
    for carrier in carriers:
        status = carrier.get('status', 'None')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\nCarriers by status:")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")
    
    # Show sample carriers
    print("\nSample carriers:")
    for carrier in carriers[:5]:
        print(f"  ID: {carrier.get('carrier_id')}, Name: {carrier.get('carrier_name')}, Status: {carrier.get('status')}")
    
    # Check for Active carriers specifically
    active_carriers = [c for c in carriers if c.get('status') == 'Active']
    print(f"\nActive carriers (status == 'Active'): {len(active_carriers)}")
    
    # Check for case variations
    active_lower = [c for c in carriers if c.get('status', '').lower() == 'active']
    print(f"Active carriers (case-insensitive): {len(active_lower)}")
    
    # If no Active carriers, update them
    if len(active_carriers) == 0 and len(carriers) > 0:
        print("\nNo Active carriers found. Would you like to update all carriers to Active status? (y/n): ", end='')
        if input().lower() == 'y':
            for carrier in carriers:
                if carrier.get('status') != 'Active':
                    try:
                        supabase.table('carriers').update({'status': 'Active'}).eq('carrier_id', carrier['carrier_id']).execute()
                        print(f"Updated carrier {carrier['carrier_name']} to Active")
                    except Exception as e:
                        print(f"Error updating carrier {carrier['carrier_name']}: {e}")
            print("\nDone! All carriers should now be Active.")

if __name__ == "__main__":
    check_carrier_status()