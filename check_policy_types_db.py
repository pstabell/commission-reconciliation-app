#!/usr/bin/env python3
"""
Script to check Policy Type values in Supabase database
This will help determine if policy types are stored as codes (HO3) or names (HOME)
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd

# Load environment variables
load_dotenv()

def connect_to_supabase():
    """Connect to Supabase database"""
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_ANON_KEY')
    
    if not url or not key:
        print("Error: Supabase credentials not found in environment variables")
        sys.exit(1)
    
    try:
        client = create_client(url, key)
        print("Successfully connected to Supabase")
        return client
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        sys.exit(1)

def check_policy_types(client: Client):
    """Query and analyze policy types in the database"""
    print("\n" + "="*60)
    print("CHECKING POLICY TYPES IN DATABASE")
    print("="*60)
    
    try:
        # 1. Get a sample of policies with HOME or HO in the Policy Type
        print("\n1. Sample of policies with 'HOME' or 'HO' in Policy Type:")
        print("-" * 60)
        
        # Query for policies containing HOME or HO
        response = client.table('policies') \
            .select('id', 'policy_number', 'customer_name', 'policy_type', 'carrier', 'mga') \
            .or_('policy_type.ilike.%HOME%,policy_type.ilike.%HO%') \
            .limit(10) \
            .execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            print(f"Found {len(df)} policies:")
            for idx, row in df.iterrows():
                print(f"  - Policy #{row['policy_number']}: '{row['policy_type']}' "
                      f"(Customer: {row['customer_name']}, Carrier: {row['carrier']})")
        else:
            print("No policies found with 'HOME' or 'HO' in Policy Type")
        
        # 2. Check specifically for HO3 policy type
        print("\n2. Checking for policies with exactly 'HO3' as Policy Type:")
        print("-" * 60)
        
        response_ho3 = client.table('policies') \
            .select('id', 'policy_number', 'customer_name', 'policy_type', 'carrier', 'mga') \
            .eq('policy_type', 'HO3') \
            .limit(5) \
            .execute()
        
        if response_ho3.data:
            df_ho3 = pd.DataFrame(response_ho3.data)
            print(f"Found {len(df_ho3)} policies with 'HO3':")
            for idx, row in df_ho3.iterrows():
                print(f"  - Policy #{row['policy_number']}: '{row['policy_type']}'")
        else:
            print("No policies found with exactly 'HO3' as Policy Type")
        
        # 3. Get all unique policy types that contain HOME or HO
        print("\n3. All unique Policy Types containing 'HOME' or 'HO':")
        print("-" * 60)
        
        response_all = client.table('policies') \
            .select('policy_type') \
            .or_('policy_type.ilike.%HOME%,policy_type.ilike.%HO%') \
            .execute()
        
        if response_all.data:
            policy_types = set(row['policy_type'] for row in response_all.data if row['policy_type'])
            sorted_types = sorted(policy_types)
            print(f"Found {len(sorted_types)} unique policy types:")
            for pt in sorted_types:
                # Count how many policies have this type
                count_response = client.table('policies') \
                    .select('id', count='exact') \
                    .eq('policy_type', pt) \
                    .execute()
                count = count_response.count if hasattr(count_response, 'count') else 0
                print(f"  - '{pt}' ({count} policies)")
        
        # 4. Sample of all unique policy types in the database
        print("\n4. Sample of ALL unique Policy Types in database:")
        print("-" * 60)
        
        response_unique = client.table('policies') \
            .select('policy_type') \
            .execute()
        
        if response_unique.data:
            all_types = set(row['policy_type'] for row in response_unique.data if row['policy_type'])
            sorted_all_types = sorted(all_types)[:20]  # Show first 20
            print(f"Showing first 20 of {len(all_types)} unique policy types:")
            for pt in sorted_all_types:
                print(f"  - '{pt}'")
            
            if len(all_types) > 20:
                print(f"  ... and {len(all_types) - 20} more")
        
    except Exception as e:
        print(f"Error querying database: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function"""
    # Connect to Supabase
    client = connect_to_supabase()
    
    # Check policy types
    check_policy_types(client)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()