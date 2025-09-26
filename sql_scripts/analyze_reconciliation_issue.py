#!/usr/bin/env python3
"""
Analyze reconciliation balance discrepancy.
Dashboard shows $9,824 due but reconciliation shows tiny amounts.
"""

import pandas as pd
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables  
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def run_analysis():
    print("="*80)
    print("RECONCILIATION BALANCE ANALYSIS")
    print("="*80)
    
    # 1. Get all transactions and calculate balances like the app does
    print("\n1. Fetching all transactions...")
    
    # Get all data
    all_data_response = supabase.table('policies') \
        .select('*') \
        .eq('user_email', 'patric@bellwethercm.com') \
        .execute()
    
    all_data = pd.DataFrame(all_data_response.data)
    print(f"   Total records: {len(all_data)}")
    
    # Filter original transactions (exclude -STMT-, -VOID-, -ADJ-)
    original_mask = ~all_data['Transaction ID'].str.contains('-STMT-|-VOID-|-ADJ-', na=False, regex=True)
    original_trans = all_data[original_mask].copy()
    print(f"   Original transactions: {len(original_trans)}")
    
    # 2. Check Total Agent Comm values
    print("\n2. Total Agent Comm Analysis:")
    print(f"   - Records with Total Agent Comm: {original_trans['Total Agent Comm'].notna().sum()}")
    print(f"   - Records with NULL Total Agent Comm: {original_trans['Total Agent Comm'].isna().sum()}")
    print(f"   - Records with Total Agent Comm = 0: {(original_trans['Total Agent Comm'] == 0).sum()}")
    print(f"   - Records with Total Agent Comm > 0: {(original_trans['Total Agent Comm'] > 0).sum()}")
    
    # 3. Calculate balances manually
    print("\n3. Calculating balances for each transaction...")
    
    balances = []
    for idx, row in original_trans.iterrows():
        # Get commission amount
        total_agent_comm = row.get('Total Agent Comm', 0)
        if pd.isna(total_agent_comm) or total_agent_comm == 0:
            # Fallback calculation
            agent_est = row.get('Agent Estimated Comm $', 0)
            broker_fee = row.get('Broker Fee Agent Comm', 0)
            total_agent_comm = float(agent_est or 0) + float(broker_fee or 0)
        
        credit = float(total_agent_comm or 0)
        
        # Get payments for this policy
        policy_num = row['Policy Number']
        eff_date = row['Effective Date']
        
        # Find STMT entries
        stmt_entries = all_data[
            (all_data['Policy Number'] == policy_num) &
            (all_data['Effective Date'] == eff_date) &
            (all_data['Transaction ID'].str.contains('-STMT-', na=False))
        ]
        
        debit = 0
        if not stmt_entries.empty:
            debit = stmt_entries['Agent Paid Amount (STMT)'].fillna(0).sum()
        
        balance = credit - debit
        
        if balance > 0.01:  # Only track positive balances
            balances.append({
                'Transaction ID': row['Transaction ID'],
                'Customer': row['Customer'],
                'Policy Number': policy_num,
                'Effective Date': eff_date,
                'Total Agent Comm': row.get('Total Agent Comm', 0),
                'Credit': credit,
                'Debit': debit,
                'Balance': balance
            })
    
    balance_df = pd.DataFrame(balances)
    
    print(f"\n   Transactions with positive balance: {len(balance_df)}")
    if len(balance_df) > 0:
        print(f"   Total balance outstanding: ${balance_df['Balance'].sum():,.2f}")
        
        # Show top 10 by balance
        print("\n4. Top 10 Transactions by Outstanding Balance:")
        print("-" * 80)
        top_10 = balance_df.nlargest(10, 'Balance')
        for _, row in top_10.iterrows():
            print(f"   {row['Transaction ID']}: {row['Customer'][:30]:<30} "
                  f"Balance: ${row['Balance']:>10,.2f} "
                  f"(Credit: ${row['Credit']:,.2f}, Debit: ${row['Debit']:,.2f})")
    
    # 5. Check date filtering
    print("\n5. Date Range Analysis:")
    original_trans['Effective Date'] = pd.to_datetime(original_trans['Effective Date'], errors='coerce')
    
    # Past 18 months
    from datetime import datetime, timedelta
    cutoff_18m = datetime.now() - timedelta(days=548)  # ~18 months
    recent_trans = original_trans[original_trans['Effective Date'] >= cutoff_18m]
    
    print(f"   Transactions in past 18 months: {len(recent_trans)}")
    print(f"   Transactions older than 18 months: {len(original_trans) - len(recent_trans)}")
    
    # 6. Dashboard calculation replication
    print("\n6. Dashboard Calculation Replication:")
    
    # Calculate total earned from original transactions
    total_earned = original_trans['Total Agent Comm'].fillna(0).sum()
    
    # Calculate total paid from STMT entries
    stmt_mask = all_data['Transaction ID'].str.contains('-STMT-', na=False)
    total_paid = all_data[stmt_mask]['Agent Paid Amount (STMT)'].fillna(0).sum()
    
    print(f"   Total Agent Comm (earned): ${total_earned:,.2f}")
    print(f"   Total Agent Paid (STMT): ${total_paid:,.2f}")
    print(f"   Simple calculation (earned - paid): ${total_earned - total_paid:,.2f}")
    
    # 7. Check for specific high-value unpaid transactions
    print("\n7. High-Value Unpaid Transactions:")
    print("-" * 80)
    
    # Get transactions with Total Agent Comm > $100
    high_value = original_trans[original_trans['Total Agent Comm'] > 100].copy()
    print(f"   Found {len(high_value)} transactions with Total Agent Comm > $100")
    
    # Check if they have been paid
    unpaid_count = 0
    for _, trans in high_value.iterrows():
        # Check for STMT entries
        stmt_check = all_data[
            (all_data['Policy Number'] == trans['Policy Number']) &
            (all_data['Effective Date'] == trans['Effective Date']) &
            (all_data['Transaction ID'].str.contains('-STMT-', na=False))
        ]
        
        if stmt_check.empty:
            unpaid_count += 1
            if unpaid_count <= 5:  # Show first 5
                print(f"   UNPAID: {trans['Transaction ID']} - {trans['Customer'][:30]} - ${trans['Total Agent Comm']:,.2f}")
    
    print(f"\n   Total unpaid high-value transactions: {unpaid_count}")
    
    return balance_df

if __name__ == "__main__":
    try:
        balance_df = run_analysis()
        
        # Save detailed results
        if not balance_df.empty:
            output_file = "reconciliation_balance_analysis.csv"
            balance_df.to_csv(output_file, index=False)
            print(f"\n8. Detailed results saved to: {output_file}")
            
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()