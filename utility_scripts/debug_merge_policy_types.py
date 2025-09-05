#!/usr/bin/env python3
"""Debug script to check why DP1 and DFIRE policy types are not merging"""

import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Supabase credentials not found in environment variables")
    sys.exit(1)

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("=== Debugging Policy Type Merge Issue ===\n")

# 1. Check unique policy types in database
print("1. Checking unique policy types in database:")
try:
    response = supabase.table('policies').select('"Policy Type"').execute()
    
    if response.data:
        policy_types = {}
        for record in response.data:
            pt = record.get('Policy Type')
            if pt:
                policy_types[pt] = policy_types.get(pt, 0) + 1
        
        print(f"\nFound {len(policy_types)} unique policy types:")
        for pt, count in sorted(policy_types.items()):
            print(f"  - '{pt}': {count} transactions")
            
        # Check specifically for DP1 and DFIRE
        if 'DP1' in policy_types:
            print(f"\n✓ DP1 found with {policy_types['DP1']} transactions")
        else:
            print("\n✗ DP1 not found in database")
            
        if 'DFIRE' in policy_types:
            print(f"✓ DFIRE found with {policy_types['DFIRE']} transactions")
        else:
            print("\n✗ DFIRE not found in database")
    else:
        print("No data returned from policies table")
        
except Exception as e:
    print(f"Error querying database: {e}")

# 2. Try to simulate the merge operation
print("\n\n2. Testing merge operation (DP1 -> DFIRE):")
try:
    # First, let's check if there are any DP1 records
    dp1_check = supabase.table('policies').select('*').eq('"Policy Type"', 'DP1').limit(5).execute()
    
    if dp1_check.data:
        print(f"Found {len(dp1_check.data)} DP1 records (showing first 5)")
        for i, record in enumerate(dp1_check.data[:5]):
            print(f"  Record {i+1}: ID={record.get('_id')}, Customer={record.get('Customer')}, Policy#={record.get('Policy Number')}")
    else:
        print("No DP1 records found to merge")
        
    # Check DFIRE records too
    dfire_check = supabase.table('policies').select('*').eq('"Policy Type"', 'DFIRE').limit(5).execute()
    
    if dfire_check.data:
        print(f"\nFound {len(dfire_check.data)} DFIRE records (showing first 5)")
        for i, record in enumerate(dfire_check.data[:5]):
            print(f"  Record {i+1}: ID={record.get('_id')}, Customer={record.get('Customer')}, Policy#={record.get('Policy Number')}")
    else:
        print("\nNo DFIRE records found")
        
except Exception as e:
    print(f"Error checking records: {e}")

# 3. Check if column name requires special handling
print("\n\n3. Testing different column name formats:")
try:
    # Try without quotes
    test1 = supabase.table('policies').select('count', count='exact').eq('Policy Type', 'DP1').execute()
    print(f"Without quotes: {test1.count if hasattr(test1, 'count') else 'No count returned'}")
except Exception as e:
    print(f"Without quotes failed: {e}")

try:
    # Try with quotes
    test2 = supabase.table('policies').select('count', count='exact').eq('"Policy Type"', 'DP1').execute()
    print(f"With quotes: {test2.count if hasattr(test2, 'count') else 'No count returned'}")
except Exception as e:
    print(f"With quotes failed: {e}")

# 4. Check if we can perform a test update
print("\n\n4. Testing update capability:")
print("Would you like to try a test update? (This will update ONE DP1 record to DFIRE)")
print("Type 'yes' to proceed, anything else to skip: ")
user_input = input().strip().lower()

if user_input == 'yes':
    try:
        # Get one DP1 record
        test_record = supabase.table('policies').select('*').eq('"Policy Type"', 'DP1').limit(1).execute()
        
        if test_record.data:
            record_id = test_record.data[0]['_id']
            print(f"\nUpdating record ID {record_id} from DP1 to DFIRE...")
            
            # Try the update
            update_result = supabase.table('policies').update({'Policy Type': 'DFIRE'}).eq('_id', record_id).execute()
            
            if update_result.data:
                print("✓ Update successful!")
                # Verify the update
                verify = supabase.table('policies').select('*').eq('_id', record_id).execute()
                if verify.data:
                    print(f"Verified: Policy Type is now '{verify.data[0].get('Policy Type')}'")
            else:
                print("✗ Update returned no data")
        else:
            print("No DP1 record found to test with")
            
    except Exception as e:
        print(f"Update test failed: {e}")
else:
    print("Skipping test update")

print("\n\n=== End of Debug Report ===")