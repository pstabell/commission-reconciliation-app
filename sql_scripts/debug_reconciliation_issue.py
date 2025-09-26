"""
Debug script to understand why reconciliation shows 0 matches
when dashboard correctly shows $9,824.29 in Agent Commission Due
"""

import pandas as pd
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_supabase_client():
    """Initialize Supabase client"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)

def debug_reconciliation():
    """Debug why reconciliation can't find matches"""
    supabase = get_supabase_client()
    
    # Load all data (like the app does)
    response = supabase.table('policies').select("*").execute()
    if not response.data:
        print("No data found!")
        return
    
    all_data = pd.DataFrame(response.data)
    print(f"Total records loaded: {len(all_data)}")
    
    # Filter for original transactions (exclude STMT, VOID, ADJ)
    original_trans = all_data[
        ~all_data['Transaction ID'].str.contains('-STMT-|-VOID-|-ADJ-', na=False, regex=True)
    ].copy()
    print(f"Original transactions: {len(original_trans)}")
    
    # Calculate balances (simplified version)
    print("\n=== CALCULATING BALANCES ===")
    total_commission_due = 0
    transactions_with_balance = 0
    
    for idx, row in original_trans.iterrows():
        # Calculate credit (commission owed)
        credit = float(row.get('Total Agent Comm', 0) or 0)
        if credit == 0:
            # Fallback calculation
            agent_comm = float(row.get('Agent Estimated Comm $', 0) or 0)
            broker_comm = float(row.get('Broker Fee Agent Comm', 0) or 0)
            credit = agent_comm + broker_comm
        
        # Calculate debit (payments received)
        policy_num = row['Policy Number']
        effective_date = row['Effective Date']
        
        # Find matching STMT entries
        stmt_entries = all_data[
            (all_data['Policy Number'] == policy_num) &
            (all_data['Effective Date'] == effective_date) &
            (all_data['Transaction ID'].str.contains('-STMT-|-VOID-', na=False, regex=True))
        ]
        
        debit = 0
        if not stmt_entries.empty:
            debit = stmt_entries['Agent Paid Amount (STMT)'].fillna(0).sum()
        
        balance = credit - debit
        if balance > 0.01:
            transactions_with_balance += 1
            total_commission_due += balance
            if transactions_with_balance <= 5:  # Show first 5 examples
                print(f"\nExample {transactions_with_balance}:")
                print(f"  Customer: {row['Customer']}")
                print(f"  Policy: {row['Policy Number']}")
                print(f"  Effective Date: {row['Effective Date']}")
                print(f"  Commission Due: ${credit:.2f}")
                print(f"  Already Paid: ${debit:.2f}")
                print(f"  Outstanding: ${balance:.2f}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Transactions with outstanding balance: {transactions_with_balance}")
    print(f"Total Agent Commission Due: ${total_commission_due:.2f}")
    
    # Check what reconciliation looks for
    print("\n=== RECONCILIATION MATCHING KEYS ===")
    print("Reconciliation matches on:")
    print("1. Policy Number + Effective Date (exact match)")
    print("2. Customer + Policy + Amount (with 5% tolerance)")
    print("3. Customer + Policy")
    
    # Check data quality for matching
    print("\n=== DATA QUALITY FOR MATCHING ===")
    missing_policy = original_trans['Policy Number'].isna().sum()
    missing_customer = original_trans['Customer'].isna().sum()
    missing_date = original_trans['Effective Date'].isna().sum()
    
    print(f"Missing Policy Numbers: {missing_policy}")
    print(f"Missing Customer Names: {missing_customer}")
    print(f"Missing Effective Dates: {missing_date}")
    
    # Show unique values to check for formatting issues
    print("\n=== SAMPLE DATA FORMAT ===")
    print("Sample Policy Numbers:")
    print(original_trans['Policy Number'].dropna().head(5).tolist())
    print("\nSample Customer Names:")
    print(original_trans['Customer'].dropna().head(5).tolist())
    print("\nSample Effective Dates:")
    print(original_trans['Effective Date'].dropna().head(5).tolist())
    
    # Check if there are any STMT entries at all
    stmt_entries = all_data[all_data['Transaction ID'].str.contains('-STMT-', na=False)]
    print(f"\n=== RECONCILIATION HISTORY ===")
    print(f"Total STMT entries in database: {len(stmt_entries)}")
    
    if len(stmt_entries) > 0:
        print("Recent STMT entries:")
        print(stmt_entries[['Transaction ID', 'Policy Number', 'Effective Date', 'Agent Paid Amount (STMT)']].tail(5))

if __name__ == "__main__":
    debug_reconciliation()