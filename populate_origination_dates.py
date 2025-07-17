#!/usr/bin/env python3
"""
Script to populate missing Policy Origination Dates in the database
using the same logic as the Edit Transaction form.
"""

import pandas as pd
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

def get_supabase_client():
    """Get Supabase client."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        raise Exception("Missing Supabase credentials. Please check your .env file.")
    return create_client(url, key)

def load_all_policies():
    """Load all policies from database."""
    supabase = get_supabase_client()
    response = supabase.table('policies').select("*").execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame()

def find_origination_date(policy_num, all_data, visited=None):
    """
    Recursively find the origination date by tracing back to the original NEW transaction.
    """
    if visited is None:
        visited = set()
    
    if policy_num in visited:
        return None, None, "Circular reference detected"
    visited.add(policy_num)
    
    # Find transactions for this policy number
    policy_transactions = all_data[all_data['Policy Number'] == policy_num].copy()
    
    if not policy_transactions.empty:
        # Sort by effective date to get earliest
        if 'Effective Date' in policy_transactions.columns:
            policy_transactions = policy_transactions.sort_values('Effective Date')
        
        # Check for NEW transaction
        new_transactions = policy_transactions[policy_transactions['Transaction Type'] == 'NEW']
        if len(new_transactions) > 1:
            # Multiple NEW transactions warning
            return None, None, "Multiple NEW transactions found"
        elif len(new_transactions) == 1:
            # Found the NEW transaction
            orig_date = new_transactions.iloc[0].get('Policy Origination Date')
            if orig_date and pd.notna(orig_date):
                return orig_date, new_transactions.iloc[0].get('Transaction ID'), "Found from NEW transaction"
            # If NEW transaction has no origination date, use its effective date
            eff_date = new_transactions.iloc[0].get('Effective Date')
            if eff_date and pd.notna(eff_date):
                return eff_date, new_transactions.iloc[0].get('Transaction ID'), "Found from NEW transaction's Effective Date"
        
        # No NEW transaction, check for Prior Policy Number
        for _, trans in policy_transactions.iterrows():
            prior_policy = trans.get('Prior Policy Number')
            if prior_policy and pd.notna(prior_policy) and str(prior_policy).strip():
                # Recursively follow the chain
                result_date, source_trans_id, result_msg = find_origination_date(prior_policy, all_data, visited)
                if result_date:
                    return result_date, source_trans_id, f"{result_msg} (via Prior Policy: {prior_policy})"
    
    return None, None, "No NEW transaction found in chain"

def main():
    print("Policy Origination Date Population Script")
    print("=" * 50)
    
    # Load all policies
    print("\nLoading all policies from database...")
    all_data = load_all_policies()
    print(f"Loaded {len(all_data)} total transactions")
    
    # Find transactions missing Policy Origination Date
    missing_origination = all_data[
        (all_data['Policy Origination Date'].isna()) | 
        (all_data['Policy Origination Date'] == '') |
        (all_data['Policy Origination Date'].isna())
    ].copy()
    
    print(f"\nFound {len(missing_origination)} transactions missing Policy Origination Date")
    
    if len(missing_origination) == 0:
        print("All transactions already have Policy Origination Date populated!")
        return
    
    # Process each missing transaction
    updates = []
    errors = []
    
    print("\nProcessing transactions...")
    for idx, row in missing_origination.iterrows():
        transaction_id = row.get('Transaction ID')
        transaction_type = row.get('Transaction Type')
        policy_number = row.get('Policy Number')
        effective_date = row.get('Effective Date')
        
        print(f"\n[{idx+1}/{len(missing_origination)}] Processing {transaction_id} - Type: {transaction_type}")
        
        auto_populated_date = None
        reason = ""
        
        # Apply the same logic as the form
        if transaction_type == 'NEW':
            # For NEW transactions, use Effective Date
            if effective_date and pd.notna(effective_date):
                auto_populated_date = effective_date
                reason = "NEW transaction - using Effective Date"
        
        elif transaction_type == 'BoR':
            # For BoR, use Effective Date (new relationship)
            if effective_date and pd.notna(effective_date):
                auto_populated_date = effective_date
                reason = "BoR transaction - using Effective Date (new relationship)"
        
        elif transaction_type in ['RWL', 'END', 'PCH', 'CAN', 'XCL', 'REWRITE', 'NBS', 'STL'] and policy_number:
            # For these types, look up the original NEW transaction
            found_date, source_trans_id, message = find_origination_date(policy_number, all_data)
            if found_date:
                auto_populated_date = found_date
                reason = f"{transaction_type} transaction - {message}"
        
        # If we found a date to populate
        if auto_populated_date:
            updates.append({
                'transaction_id': transaction_id,
                'policy_number': policy_number,
                'transaction_type': transaction_type,
                'origination_date': auto_populated_date,
                'reason': reason
            })
            print(f"  ✓ Will update with: {auto_populated_date} ({reason})")
        else:
            errors.append({
                'transaction_id': transaction_id,
                'policy_number': policy_number,
                'transaction_type': transaction_type,
                'reason': 'No origination date could be determined'
            })
            print(f"  ✗ Skipping - no origination date found")
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total transactions missing origination date: {len(missing_origination)}")
    print(f"Can be updated: {len(updates)}")
    print(f"Cannot be updated: {len(errors)}")
    
    if updates:
        print("\nTransactions to update:")
        update_df = pd.DataFrame(updates)
        print(update_df.to_string(index=False))
    
    if errors:
        print("\nTransactions that cannot be updated:")
        error_df = pd.DataFrame(errors)
        print(error_df.to_string(index=False))
    
    # Ask for confirmation before updating
    if updates:
        print("\n" + "=" * 50)
        response = input(f"Do you want to update {len(updates)} transactions? (yes/no): ")
        
        if response.lower() == 'yes':
            print("\nUpdating database...")
            supabase = get_supabase_client()
            success_count = 0
            
            for update in updates:
                try:
                    # Update the record
                    supabase.table('policies').update({
                        'Policy Origination Date': update['origination_date']
                    }).eq('Transaction ID', update['transaction_id']).execute()
                    
                    success_count += 1
                    print(f"✓ Updated {update['transaction_id']}")
                except Exception as e:
                    print(f"✗ Error updating {update['transaction_id']}: {str(e)}")
            
            print(f"\nSuccessfully updated {success_count} out of {len(updates)} transactions")
        else:
            print("\nUpdate cancelled")
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"origination_date_population_report_{timestamp}.csv"
    
    # Combine updates and errors for report
    all_results = []
    for update in updates:
        all_results.append({
            'Transaction ID': update['transaction_id'],
            'Policy Number': update['policy_number'],
            'Transaction Type': update['transaction_type'],
            'Status': 'Can Update',
            'Origination Date': update['origination_date'],
            'Reason': update['reason']
        })
    for error in errors:
        all_results.append({
            'Transaction ID': error['transaction_id'],
            'Policy Number': error['policy_number'],
            'Transaction Type': error['transaction_type'],
            'Status': 'Cannot Update',
            'Origination Date': '',
            'Reason': error['reason']
        })
    
    if all_results:
        report_df = pd.DataFrame(all_results)
        report_df.to_csv(report_filename, index=False)
        print(f"\nReport saved to: {report_filename}")

if __name__ == "__main__":
    main()