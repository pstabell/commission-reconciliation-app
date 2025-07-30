#!/usr/bin/env python3
"""
Simple script to analyze -IMPORT transactions without external dependencies.
"""

import sqlite3
from datetime import datetime
import os
from collections import defaultdict

# Database path
db_path = "commissions.db"

def analyze_import_transactions():
    """Analyze -IMPORT transactions for double entries."""
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
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
        
        # Execute query
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Process results
        total_import_count = len(rows)
        double_entry_count = 0
        double_entries = []
        
        # Stats for analysis
        est_only = 0
        paid_only = 0
        neither = 0
        date_counts = defaultdict(int)
        customer_counts = defaultdict(int)
        
        for row in rows:
            transaction_id = row[0]
            customer = row[1]
            agent_estimated = float(row[2]) if row[2] else 0.0
            agent_paid = float(row[3]) if row[3] else 0.0
            stmt_date = row[4]
            x_date = row[5]
            
            # Check for double entry
            if agent_estimated != 0 and agent_paid != 0:
                double_entry_count += 1
                double_entries.append({
                    'transaction_id': transaction_id,
                    'customer': customer,
                    'agent_estimated': agent_estimated,
                    'agent_paid': agent_paid,
                    'stmt_date': stmt_date,
                    'x_date': x_date,
                    'amount_diff': abs(agent_estimated - agent_paid)
                })
                date_counts[stmt_date] += 1
                customer_counts[customer] += 1
            elif agent_estimated != 0 and agent_paid == 0:
                est_only += 1
            elif agent_estimated == 0 and agent_paid != 0:
                paid_only += 1
            else:
                neither += 1
        
        # Print summary report
        print("=" * 80)
        print("IMPORT TRANSACTION ANALYSIS REPORT")
        print("=" * 80)
        print(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n1. SUMMARY COUNTS:")
        print(f"   - Total -IMPORT transactions: {total_import_count}")
        print(f"   - Transactions with double entry (both fields have values): {double_entry_count}")
        if total_import_count > 0:
            print(f"   - Percentage with double entry: {(double_entry_count/total_import_count*100):.1f}%")
        
        if double_entry_count > 0:
            print(f"\n2. PATTERN ANALYSIS:")
            
            # Check for date patterns
            print(f"\n   Statement Paid Dates (top 5):")
            sorted_dates = sorted(date_counts.items(), key=lambda x: x[1], reverse=True)
            for date, count in sorted_dates[:5]:
                print(f"     - {date}: {count} transactions")
            
            # Check for customer patterns
            print(f"\n   Top Customers with Double Entries (top 5):")
            sorted_customers = sorted(customer_counts.items(), key=lambda x: x[1], reverse=True)
            for customer, count in sorted_customers[:5]:
                print(f"     - {customer}: {count} transactions")
            
            # Show examples
            print(f"\n3. EXAMPLES OF DOUBLE ENTRIES (showing first 10):")
            print("-" * 80)
            
            for idx, entry in enumerate(double_entries[:10], 1):
                print(f"\n   Example {idx}:")
                print(f"     Transaction ID: {entry['transaction_id']}")
                print(f"     Customer: {entry['customer']}")
                print(f"     Agent Estimated Comm $: ${entry['agent_estimated']:,.2f}")
                print(f"     Agent Paid Amount (STMT): ${entry['agent_paid']:,.2f}")
                print(f"     Statement Paid Date: {entry['stmt_date']}")
                print(f"     X Date: {entry['x_date']}")
            
            # Check if the amounts are typically the same or different
            print(f"\n4. AMOUNT COMPARISON:")
            same_amount = sum(1 for e in double_entries if e['amount_diff'] < 0.01)
            print(f"   - Transactions where both amounts are the same: {same_amount}")
            print(f"   - Transactions where amounts differ: {double_entry_count - same_amount}")
            
            if double_entry_count - same_amount > 0:
                print(f"\n   Examples where amounts differ:")
                diff_examples = [e for e in double_entries if e['amount_diff'] >= 0.01][:5]
                for entry in diff_examples:
                    print(f"     - {entry['transaction_id']}: Est ${entry['agent_estimated']:,.2f} vs Paid ${entry['agent_paid']:,.2f} (Diff: ${entry['amount_diff']:,.2f})")
        
        else:
            print("\n\nNo double entries found (no transactions with values in both fields).")
        
        # Additional analysis - breakdown by field
        print(f"\n5. FIELD USAGE BREAKDOWN:")
        print(f"   - Only Agent Estimated Comm $ has value: {est_only}")
        print(f"   - Only Agent Paid Amount (STMT) has value: {paid_only}")
        print(f"   - Both fields have values (double entry): {double_entry_count}")
        print(f"   - Neither field has value: {neither}")
        
        # Export detailed results if there are double entries
        if double_entry_count > 0:
            output_file = f"import_double_entries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(output_file, 'w') as f:
                # Write header
                f.write("transaction_id,customer,agent_estimated_comm,agent_paid_amount_stmt,stmt_date,x_date,amount_diff\n")
                # Write data
                for entry in double_entries:
                    f.write(f"{entry['transaction_id']},{entry['customer']},{entry['agent_estimated']:.2f},{entry['agent_paid']:.2f},{entry['stmt_date']},{entry['x_date']},{entry['amount_diff']:.2f}\n")
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