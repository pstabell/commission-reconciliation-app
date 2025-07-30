#!/usr/bin/env python3
"""
Script to analyze -IMPORT transactions and check for double entries
where both "Agent Estimated Comm $" and "Agent Paid Amount (STMT)" fields have values.
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os

# Database path
db_path = "commissions.db"

def analyze_import_transactions():
    """Analyze -IMPORT transactions for double entries."""
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    
    try:
        # Query to get all -IMPORT transactions
        query = """
        SELECT 
            transaction_id,
            Customer,
            agent_estimated_comm,
            agent_paid_amount_stmt,
            stmt_paid_date,
            x_date,
            created_at,
            last_modified
        FROM transactions
        WHERE transaction_id LIKE '%-IMPORT'
        ORDER BY Customer, stmt_paid_date
        """
        
        # Execute query and load into DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Convert numeric columns to float, handling None values
        df['agent_estimated_comm'] = pd.to_numeric(df['agent_estimated_comm'], errors='coerce').fillna(0)
        df['agent_paid_amount_stmt'] = pd.to_numeric(df['agent_paid_amount_stmt'], errors='coerce').fillna(0)
        
        # Total count of -IMPORT transactions
        total_import_count = len(df)
        
        # Count transactions with values in both fields (double entry)
        # Consider non-zero values only
        double_entry_mask = (df['agent_estimated_comm'] != 0) & (df['agent_paid_amount_stmt'] != 0)
        double_entry_count = double_entry_mask.sum()
        
        # Get examples of double entries
        double_entries = df[double_entry_mask].copy()
        
        # Print summary report
        print("=" * 80)
        print("IMPORT TRANSACTION ANALYSIS REPORT")
        print("=" * 80)
        print(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n1. SUMMARY COUNTS:")
        print(f"   - Total -IMPORT transactions: {total_import_count}")
        print(f"   - Transactions with double entry (both fields have values): {double_entry_count}")
        print(f"   - Percentage with double entry: {(double_entry_count/total_import_count*100):.1f}%")
        
        if double_entry_count > 0:
            print(f"\n2. PATTERN ANALYSIS:")
            
            # Check for date patterns
            print(f"\n   Statement Paid Dates:")
            date_counts = double_entries['stmt_paid_date'].value_counts()
            for date, count in date_counts.head(5).items():
                print(f"     - {date}: {count} transactions")
            
            # Check for customer patterns
            print(f"\n   Top Customers with Double Entries:")
            customer_counts = double_entries['Customer'].value_counts()
            for customer, count in customer_counts.head(5).items():
                print(f"     - {customer}: {count} transactions")
            
            # Show examples
            print(f"\n3. EXAMPLES OF DOUBLE ENTRIES (showing first 10):")
            print("-" * 80)
            
            for idx, (_, row) in enumerate(double_entries.head(10).iterrows(), 1):
                print(f"\n   Example {idx}:")
                print(f"     Transaction ID: {row['transaction_id']}")
                print(f"     Customer: {row['Customer']}")
                print(f"     Agent Estimated Comm $: ${row['agent_estimated_comm']:,.2f}")
                print(f"     Agent Paid Amount (STMT): ${row['agent_paid_amount_stmt']:,.2f}")
                print(f"     Statement Paid Date: {row['stmt_paid_date']}")
                print(f"     X Date: {row['x_date']}")
            
            # Check if the amounts are typically the same or different
            print(f"\n4. AMOUNT COMPARISON:")
            double_entries['amount_diff'] = abs(double_entries['agent_estimated_comm'] - double_entries['agent_paid_amount_stmt'])
            same_amount = (double_entries['amount_diff'] < 0.01).sum()
            print(f"   - Transactions where both amounts are the same: {same_amount}")
            print(f"   - Transactions where amounts differ: {double_entry_count - same_amount}")
            
            if double_entry_count - same_amount > 0:
                print(f"\n   Examples where amounts differ:")
                diff_examples = double_entries[double_entries['amount_diff'] >= 0.01].head(5)
                for _, row in diff_examples.iterrows():
                    print(f"     - {row['transaction_id']}: Est ${row['agent_estimated_comm']:,.2f} vs Paid ${row['agent_paid_amount_stmt']:,.2f} (Diff: ${row['amount_diff']:,.2f})")
        
        else:
            print("\n\nNo double entries found (no transactions with values in both fields).")
        
        # Additional analysis - breakdown by field
        print(f"\n5. FIELD USAGE BREAKDOWN:")
        est_only = ((df['agent_estimated_comm'] != 0) & (df['agent_paid_amount_stmt'] == 0)).sum()
        paid_only = ((df['agent_estimated_comm'] == 0) & (df['agent_paid_amount_stmt'] != 0)).sum()
        neither = ((df['agent_estimated_comm'] == 0) & (df['agent_paid_amount_stmt'] == 0)).sum()
        
        print(f"   - Only Agent Estimated Comm $ has value: {est_only}")
        print(f"   - Only Agent Paid Amount (STMT) has value: {paid_only}")
        print(f"   - Both fields have values (double entry): {double_entry_count}")
        print(f"   - Neither field has value: {neither}")
        
        # Export detailed results if there are double entries
        if double_entry_count > 0:
            output_file = f"import_double_entries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            double_entries.to_csv(output_file, index=False)
            print(f"\n\nDetailed results exported to: {output_file}")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"Error analyzing transactions: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()

if __name__ == "__main__":
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found!")
        print("Please ensure you're running this script from the correct directory.")
    else:
        analyze_import_transactions()