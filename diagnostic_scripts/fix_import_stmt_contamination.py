#!/usr/bin/env python3
"""
CRITICAL FIX: Remove STMT data from -IMPORT transactions

This script addresses a critical data integrity issue where -IMPORT transactions
have been incorrectly populated with STMT column data. These columns should ONLY
be populated on -STMT-, -VOID-, and -ADJ- transactions.

ISSUE: -IMPORT transactions from July 2025 reconciliation have values in:
- Agent Paid Amount (STMT)
- Agency Comm Received (STMT)  
- STMT DATE

These fields should be NULL/empty on -IMPORT transactions.

Author: Sales Commission App Team
Date: August 10, 2025
"""

import os
import sys
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Supabase credentials
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("ERROR: Missing SUPABASE_URL or SUPABASE_KEY in environment variables")
    sys.exit(1)

# Create Supabase client
supabase: Client = create_client(url, key)

def analyze_import_transactions():
    """Analyze -IMPORT transactions to find those with STMT data."""
    print("\n=== ANALYZING -IMPORT TRANSACTIONS ===\n")
    
    try:
        # Query all -IMPORT transactions
        response = supabase.table('policies').select('*').like('"Transaction ID"', '%-IMPORT%').execute()
        
        if not response.data:
            print("No -IMPORT transactions found in database.")
            return []
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(response.data)
        total_import = len(df)
        print(f"Total -IMPORT transactions found: {total_import}")
        
        # Check for STMT data contamination
        contaminated = df[
            (df['Agent Paid Amount (STMT)'].notna() & (df['Agent Paid Amount (STMT)'] != 0)) |
            (df['Agency Comm Received (STMT)'].notna() & (df['Agency Comm Received (STMT)'] != 0)) |
            (df['STMT DATE'].notna() & (df['STMT DATE'] != ''))
        ]
        
        if len(contaminated) == 0:
            print("\n✅ GOOD NEWS: No -IMPORT transactions have STMT data contamination!")
            return []
        
        print(f"\n⚠️  CRITICAL: Found {len(contaminated)} -IMPORT transactions with STMT data!")
        print("\nContaminated transactions:")
        print("-" * 100)
        
        # Display details of contaminated transactions
        for idx, row in contaminated.iterrows():
            print(f"\nTransaction ID: {row['Transaction ID']}")
            print(f"  Customer: {row['Customer']}")
            print(f"  Policy Number: {row['Policy Number']}")
            print(f"  Transaction Type: {row['Transaction Type']}")
            print(f"  Effective Date: {row['Effective Date']}")
            
            # Show contaminated fields
            print("  CONTAMINATED FIELDS:")
            if pd.notna(row['Agent Paid Amount (STMT)']) and row['Agent Paid Amount (STMT)'] != 0:
                print(f"    - Agent Paid Amount (STMT): ${row['Agent Paid Amount (STMT)']:.2f} ❌ SHOULD BE NULL")
            if pd.notna(row['Agency Comm Received (STMT)']) and row['Agency Comm Received (STMT)'] != 0:
                print(f"    - Agency Comm Received (STMT): ${row['Agency Comm Received (STMT)']:.2f} ❌ SHOULD BE NULL")
            if pd.notna(row['STMT DATE']) and row['STMT DATE'] != '':
                print(f"    - STMT DATE: {row['STMT DATE']} ❌ SHOULD BE NULL")
        
        return contaminated.to_dict('records')
        
    except Exception as e:
        print(f"ERROR analyzing transactions: {e}")
        return []

def check_for_stmt_entries(contaminated_imports):
    """Check if proper -STMT- entries exist for the contaminated imports."""
    print("\n=== CHECKING FOR PROPER -STMT- ENTRIES ===\n")
    
    if not contaminated_imports:
        return
    
    # Extract policy numbers from contaminated imports
    policy_numbers = [row['Policy Number'] for row in contaminated_imports]
    unique_policies = list(set(policy_numbers))
    
    print(f"Checking {len(unique_policies)} unique policy numbers for -STMT- entries...")
    
    try:
        # Query for -STMT- transactions with these policy numbers
        response = supabase.table('policies').select('*').in_('"Policy Number"', unique_policies).like('"Transaction ID"', '%-STMT-%').execute()
        
        if response.data:
            stmt_df = pd.DataFrame(response.data)
            print(f"\n✅ Found {len(stmt_df)} proper -STMT- transactions for these policies")
            
            # Group by policy number to show summary
            stmt_by_policy = stmt_df.groupby('Policy Number').agg({
                'Transaction ID': 'count',
                'Agent Paid Amount (STMT)': 'sum'
            }).rename(columns={
                'Transaction ID': 'STMT Count',
                'Agent Paid Amount (STMT)': 'Total STMT Amount'
            })
            
            print("\nSTMT transactions by policy:")
            print(stmt_by_policy.to_string())
        else:
            print("\n⚠️  WARNING: No -STMT- transactions found for these policies!")
            print("This suggests the reconciliation process may have incorrectly updated -IMPORT transactions")
            print("instead of creating proper -STMT- entries.")
            
    except Exception as e:
        print(f"ERROR checking STMT entries: {e}")

def create_backup(contaminated_imports):
    """Create a backup CSV of contaminated transactions before fixing."""
    if not contaminated_imports:
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"contaminated_imports_backup_{timestamp}.csv"
    
    try:
        df = pd.DataFrame(contaminated_imports)
        df.to_csv(backup_filename, index=False)
        print(f"\n📁 Backup created: {backup_filename}")
        return backup_filename
    except Exception as e:
        print(f"ERROR creating backup: {e}")
        return None

def fix_contaminated_imports(contaminated_imports, dry_run=True):
    """Remove STMT data from -IMPORT transactions."""
    if not contaminated_imports:
        return
    
    print(f"\n=== {'DRY RUN' if dry_run else 'FIXING'} CONTAMINATED IMPORTS ===\n")
    
    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made to the database")
    else:
        print("⚠️  LIVE MODE - Changes WILL be made to the database")
    
    success_count = 0
    error_count = 0
    
    for row in contaminated_imports:
        transaction_id = row['Transaction ID']
        
        # Prepare update to clear STMT fields
        update_data = {
            'Agent Paid Amount (STMT)': None,
            'Agency Comm Received (STMT)': None,
            'STMT DATE': None
        }
        
        if dry_run:
            print(f"\n[DRY RUN] Would update {transaction_id}:")
            print(f"  - Clear Agent Paid Amount (STMT): ${row.get('Agent Paid Amount (STMT)', 0):.2f} → NULL")
            print(f"  - Clear Agency Comm Received (STMT): ${row.get('Agency Comm Received (STMT)', 0):.2f} → NULL")
            print(f"  - Clear STMT DATE: {row.get('STMT DATE', '')} → NULL")
            success_count += 1
        else:
            try:
                # Execute the update
                response = supabase.table('policies').update(update_data).eq('"Transaction ID"', transaction_id).execute()
                
                if response.data:
                    print(f"✅ Fixed {transaction_id}")
                    success_count += 1
                else:
                    print(f"❌ Failed to update {transaction_id} - No data returned")
                    error_count += 1
                    
            except Exception as e:
                print(f"❌ ERROR updating {transaction_id}: {e}")
                error_count += 1
    
    print(f"\n{'DRY RUN' if dry_run else 'FIX'} SUMMARY:")
    print(f"  - Successfully {'would fix' if dry_run else 'fixed'}: {success_count}")
    if error_count > 0:
        print(f"  - Errors: {error_count}")

def main():
    """Main execution function."""
    print("=" * 100)
    print("CRITICAL DATA INTEGRITY FIX: Remove STMT data from -IMPORT transactions")
    print("=" * 100)
    
    # Step 1: Analyze the problem
    contaminated = analyze_import_transactions()
    
    if not contaminated:
        print("\n✅ No action needed - all -IMPORT transactions are clean!")
        return
    
    # Step 2: Check for proper STMT entries
    check_for_stmt_entries(contaminated)
    
    # Step 3: Create backup
    print("\n" + "=" * 50)
    backup_file = create_backup(contaminated)
    if not backup_file:
        print("⚠️  Failed to create backup - aborting for safety")
        return
    
    # Step 4: Confirm action
    print("\n" + "=" * 50)
    print(f"\n⚠️  READY TO FIX {len(contaminated)} CONTAMINATED -IMPORT TRANSACTIONS")
    print("\nThis will:")
    print("  1. Set 'Agent Paid Amount (STMT)' to NULL")
    print("  2. Set 'Agency Comm Received (STMT)' to NULL") 
    print("  3. Set 'STMT DATE' to NULL")
    print("\nThese fields should ONLY have values in -STMT-, -VOID-, and -ADJ- transactions.")
    
    # First do a dry run
    print("\n" + "-" * 50)
    fix_contaminated_imports(contaminated, dry_run=True)
    
    # Ask for confirmation
    print("\n" + "=" * 50)
    response = input("\nProceed with fixing the database? (type 'YES' to confirm): ")
    
    if response == 'YES':
        print("\n" + "-" * 50)
        fix_contaminated_imports(contaminated, dry_run=False)
        print("\n✅ FIX COMPLETE!")
        print(f"\n📁 Backup saved as: {backup_file}")
        print("\n⚠️  IMPORTANT: Please verify the fix by:")
        print("  1. Checking a few -IMPORT transactions in the app")
        print("  2. Running this script again to confirm all are clean")
        print("  3. Checking that -STMT- transactions still have their data")
    else:
        print("\n❌ Fix cancelled - no changes were made to the database")

if __name__ == "__main__":
    main()