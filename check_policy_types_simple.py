#!/usr/bin/env python3
"""
Simplified script to check Policy Type values in Supabase database
"""

import os
from supabase import create_client

# Supabase credentials
SUPABASE_URL = "https://ddiahkzvmymacejqlnvc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkaWFoa3p2bXltYWNlanFsbnZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExNjU2MTUsImV4cCI6MjA2Njc0MTYxNX0.KgBeoRKsQO6WsQ0TzlC772fY8gAoXJonuS4M1Mi3BLs"

def main():
    try:
        # Create client
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Connected to Supabase successfully")
        
        # Query 1: Get sample policies with HOME or HO
        print("\n1. Sample policies with 'HOME' or 'HO' in Policy Type:")
        print("-" * 60)
        
        response = client.table('policies') \
            .select('policy_number, customer_name, policy_type') \
            .or_('policy_type.ilike.%HOME%,policy_type.ilike.%HO%') \
            .limit(5) \
            .execute()
        
        if response.data:
            for row in response.data:
                print(f"Policy #{row['policy_number']}: '{row['policy_type']}'")
        else:
            print("No policies found")
        
        # Query 2: Check for HO3 specifically
        print("\n2. Checking for 'HO3' policy type:")
        print("-" * 60)
        
        response2 = client.table('policies') \
            .select('policy_number, policy_type') \
            .eq('policy_type', 'HO3') \
            .limit(5) \
            .execute()
        
        if response2.data:
            print(f"Found {len(response2.data)} policies with 'HO3'")
            for row in response2.data:
                print(f"Policy #{row['policy_number']}")
        else:
            print("No policies found with exactly 'HO3'")
        
        # Query 3: Get unique policy types
        print("\n3. Unique policy types containing HOME or HO:")
        print("-" * 60)
        
        response3 = client.table('policies') \
            .select('policy_type') \
            .or_('policy_type.ilike.%HOME%,policy_type.ilike.%HO%') \
            .execute()
        
        if response3.data:
            unique_types = set(row['policy_type'] for row in response3.data if row['policy_type'])
            for pt in sorted(unique_types)[:10]:
                print(f"  - '{pt}'")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()