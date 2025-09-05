"""
Test script to diagnose why I0Y68NM is still showing in Pending Renewals
"""

import os
from supabase import create_client, Client
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

print("=== Renewal Diagnosis for Transaction I0Y68NM ===\n")

# First, get the details of I0Y68NM
try:
    result = supabase.table('policies').select('*').eq('"Transaction ID"', 'I0Y68NM').execute()
    if result.data:
        original = result.data[0]
        print(f"Found Transaction I0Y68NM:")
        print(f"  Customer: {original.get('Customer')}")
        print(f"  Policy Number: {original.get('Policy Number')}")
        print(f"  Transaction Type: {original.get('Transaction Type')}")
        print(f"  Effective Date: {original.get('Effective Date')}")
        print(f"  X-DATE: {original.get('X-DATE')}")
        print(f"  Prior Policy Number: {original.get('Prior Policy Number')}")
        print()
        
        # Check if this policy number appears in any Prior Policy Number field
        policy_num = original.get('Policy Number')
        if policy_num:
            print(f"Checking for renewals with Prior Policy Number = '{policy_num}'...")
            renewal_result = supabase.table('policies').select('*').eq('"Prior Policy Number"', policy_num).execute()
            
            if renewal_result.data:
                print(f"\n✅ Found {len(renewal_result.data)} renewal(s) for this policy:")
                for renewal in renewal_result.data:
                    print(f"\n  Renewal Transaction ID: {renewal.get('Transaction ID')}")
                    print(f"  Customer: {renewal.get('Customer')}")
                    print(f"  Policy Number: {renewal.get('Policy Number')}")
                    print(f"  Transaction Type: {renewal.get('Transaction Type')}")
                    print(f"  Prior Policy Number: {renewal.get('Prior Policy Number')}")
                    print(f"  Effective Date: {renewal.get('Effective Date')}")
                    print(f"  X-DATE: {renewal.get('X-DATE')}")
            else:
                print("❌ No renewals found with this policy number in Prior Policy Number field")
                
                # Let's check if there's a renewal with same customer but didn't set Prior Policy Number
                customer = original.get('Customer')
                print(f"\nChecking for other policies for customer '{customer}'...")
                
                customer_policies = supabase.table('policies').select('*').eq('"Customer"', customer).order('"Effective Date"', desc=True).execute()
                
                if customer_policies.data:
                    print(f"\nFound {len(customer_policies.data)} total policies for this customer:")
                    for idx, policy in enumerate(customer_policies.data[:5]):  # Show max 5
                        print(f"\n  [{idx+1}] Transaction ID: {policy.get('Transaction ID')}")
                        print(f"      Policy Number: {policy.get('Policy Number')}")
                        print(f"      Transaction Type: {policy.get('Transaction Type')}")
                        print(f"      Prior Policy Number: {policy.get('Prior Policy Number')}")
                        print(f"      Effective Date: {policy.get('Effective Date')}")
                        print(f"      X-DATE: {policy.get('X-DATE')}")
        else:
            print("⚠️ Original transaction has no Policy Number!")
    else:
        print("❌ Transaction I0Y68NM not found in database")
        
except Exception as e:
    print(f"Error: {e}")

print("\n=== Checking Transaction 4W014EN ===\n")

# Also check 4W014EN to see if it's related
try:
    result = supabase.table('policies').select('*').eq('"Transaction ID"', '4W014EN').execute()
    if result.data:
        policy = result.data[0]
        print(f"Found Transaction 4W014EN:")
        print(f"  Customer: {policy.get('Customer')}")
        print(f"  Policy Number: {policy.get('Policy Number')}")
        print(f"  Transaction Type: {policy.get('Transaction Type')}")
        print(f"  Prior Policy Number: {policy.get('Prior Policy Number')}")
        print(f"  Effective Date: {policy.get('Effective Date')}")
        print(f"  X-DATE: {policy.get('X-DATE')}")
        
        # Check if this has a Prior Policy Number set
        prior_policy = policy.get('Prior Policy Number')
        if prior_policy:
            print(f"\n✅ This transaction has Prior Policy Number: {prior_policy}")
            print("   This should exclude the prior policy from Pending Renewals")
        else:
            print("\n⚠️ This transaction has NO Prior Policy Number set")
            print("   The original policy may still appear in Pending Renewals")
            
except Exception as e:
    print(f"Error: {e}")

print("\n=== Summary ===")
print("If I0Y68NM is still showing in Pending Renewals, it's likely because:")
print("1. No renewal transaction has I0Y68NM's Policy Number in its Prior Policy Number field")
print("2. The renewal transaction exists but Prior Policy Number wasn't set")
print("3. The Policy Numbers don't match between original and renewal")