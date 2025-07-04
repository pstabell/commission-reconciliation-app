#!/usr/bin/env python3
"""
Test script to verify the reconciliation logic works correctly.
This script will simulate the reconciliation process and check if new transactions
are properly inserted into the main policies table.
"""

import pandas as pd
import sqlalchemy
import datetime
import json

# Create engine (same as in the main app)
engine = sqlalchemy.create_engine('sqlite:///commissions.db')

# Read current policies data
print("🔍 Reading current policies data...")
all_data = pd.read_sql('SELECT * FROM policies', engine)
print(f"Current policies count: {len(all_data)}")
print(f"Current columns: {list(all_data.columns)}")

# Simulate manual commission rows (what would be in session state)
test_manual_commission_rows = [
    {
        "Customer": "TEST CUSTOMER A",
        "Policy Type": "AUTO",
        "Policy Number": "TEST-001-RECONCILE",
        "Effective Date": "12/20/2024",
        "Transaction Type": "RWL",
        "Amount Paid": 150.00,
        "Agency Comm Received (STMT)": 300.00,
        "Client ID": "CLI-TEST-001",
        "Transaction ID": "TXN-TEST-001"
    },
    {
        "Customer": "TEST CUSTOMER B", 
        "Policy Type": "HOME",
        "Policy Number": "TEST-002-RECONCILE",
        "Effective Date": "12/21/2024",
        "Transaction Type": "NEW",
        "Amount Paid": 250.00,
        "Agency Comm Received (STMT)": 500.00,
        "Client ID": "CLI-TEST-002",
        "Transaction ID": "TXN-TEST-002"
    }
]

statement_date = datetime.date.today()
statement_description = "TEST RECONCILIATION"

print("\n📝 Simulating reconciliation process...")

try:
    # Prepare statement details for JSON storage
    statement_details = []
    for row in test_manual_commission_rows:
        statement_details.append({
            "Customer": row.get("Customer", ""),
            "Policy Type": row.get("Policy Type", ""),
            "Policy Number": row.get("Policy Number", ""),
            "Effective Date": row.get("Effective Date", ""),
            "Transaction Type": row.get("Transaction Type", ""),
            "Commission Paid": row.get("Amount Paid", 0),
            "Agency Comm Received (STMT)": row.get("Agency Comm Received (STMT)", 0),
            "Client ID": row.get("Client ID", ""),
            "Transaction ID": row.get("Transaction ID", "")
        })
    
    total_agency_received = sum(float(row.get("Agency Comm Received (STMT)", 0)) for row in test_manual_commission_rows)
    
    # Save to commission_payments table
    with engine.begin() as conn:
        conn.execute(sqlalchemy.text('''
            INSERT INTO commission_payments 
            (policy_number, customer, payment_amount, statement_date, payment_timestamp, statement_details)
            VALUES (:policy_number, :customer, :payment_amount, :statement_date, :payment_timestamp, :statement_details)
        '''), {
            "policy_number": f"BULK_STATEMENT_{statement_date.strftime('%Y%m%d')}",
            "customer": statement_description if statement_description else f"Commission Statement - {statement_date.strftime('%m/%d/%Y')}",
            "payment_amount": total_agency_received,
            "statement_date": statement_date.strftime('%Y-%m-%d'),
            "payment_timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "statement_details": json.dumps(statement_details)
        })
    
    print("✅ Saved to commission_payments table")
    
    # Save individual entries to manual_commission_entries table as well
    for row in test_manual_commission_rows:
        with engine.begin() as conn:
            conn.execute(sqlalchemy.text('''
                INSERT OR REPLACE INTO manual_commission_entries 
                (client_id, transaction_id, customer, policy_type, policy_number, effective_date, transaction_type, commission_paid, agency_commission_received, statement_date)
                VALUES (:client_id, :transaction_id, :customer, :policy_type, :policy_number, :effective_date, :transaction_type, :commission_paid, :agency_commission_received, :statement_date)
            '''), {
                "client_id": row.get("Client ID", ""),
                "transaction_id": row.get("Transaction ID", ""),
                "customer": row.get("Customer", ""),
                "policy_type": row.get("Policy Type", ""),
                "policy_number": row.get("Policy Number", ""),
                "effective_date": row.get("Effective Date", ""),
                "transaction_type": row.get("Transaction Type", ""),
                "commission_paid": float(row.get("Amount Paid", 0)),
                "agency_commission_received": float(row.get("Agency Comm Received (STMT)", 0)),
                "statement_date": statement_date.strftime('%Y-%m-%d')
            })
    
    print("✅ Saved to manual_commission_entries table")
    
    # --- NEW: Insert reconciled transactions into main policies table ---
    # This makes them appear in "All Policies" page
    db_columns = all_data.columns.tolist()
    
    for row in test_manual_commission_rows:
        # Create a new policy record with proper field mapping
        new_policy = {}
          # Map the reconciled fields to the policies table structure
        for col in db_columns:
            if col == "Customer":
                new_policy[col] = row.get("Customer", "")
            elif col == "Policy Type":
                new_policy[col] = row.get("Policy Type", "")
            elif col == "Policy Number":
                new_policy[col] = row.get("Policy Number", "")
            elif col == "Effective Date":
                new_policy[col] = row.get("Effective Date", "")
            elif col == "Client ID":
                new_policy[col] = row.get("Client ID", "")
            elif col == "Transaction ID":
                new_policy[col] = row.get("Transaction ID", "")
            elif col == "Transaction Type":
                # Map Transaction Type to Transaction Type
                transaction_type = row.get("Transaction Type", "")
                if transaction_type.upper() in ["NEW", "NBS", "STL", "BOR", "END", "PCH", "RWL", "REWRITE", "CAN", "XCL"]:
                    new_policy[col] = transaction_type.upper()
                else:
                    new_policy[col] = "RWL"  # Default
            elif col == "Agent Paid Amount (STMT)":
                new_policy[col] = float(row.get("Amount Paid", 0))
            elif col == "Statement Date" or col == "STMT DATE":
                new_policy[col] = statement_date.strftime('%m/%d/%Y')
            elif col == "Policy Origination Date":
                # Use effective date if available, otherwise statement date
                eff_date = row.get("Effective Date", "")
                new_policy[col] = eff_date if eff_date else statement_date.strftime('%m/%d/%Y')
            elif col == "Paid":
                # Mark as paid since we're reconciling a payment
                new_policy[col] = "Yes"
            elif col in ["Premium Sold", "Agency Estimated Comm/Revenue (CRM)", "Calculated Commission", "Agent Estimated Comm $"]:
                # Set monetary fields to 0 or use agency commission received if applicable
                if col == "Agency Estimated Comm/Revenue (CRM)" and "Agency Comm Received (STMT)" in row:
                    new_policy[col] = float(row.get("Agency Comm Received (STMT)", 0))
                else:
                    new_policy[col] = 0.0
            elif col in ["Policy Gross Comm %", "Agent Comm (New 50% RWL 25%)", "Gross Agency Comm %"]:
                # Set percentage fields to default values
                new_policy[col] = 0.0
            else:
                # Set all other fields to empty string
                new_policy[col] = ""
        
        print(f"\n🔄 Creating new policy record for: {new_policy['Customer']} - {new_policy['Policy Number']}")
        print(f"   Mapped fields: {len([k for k, v in new_policy.items() if v])}/{len(new_policy)}")
        
        # Insert into policies table
        new_policy_df = pd.DataFrame([new_policy])
        new_policy_df.to_sql('policies', engine, if_exists='append', index=False)
    
    print(f"\n✅ Successfully added {len(test_manual_commission_rows)} new transactions to main policies table!")
    
    # Verify the new records were added
    updated_data = pd.read_sql('SELECT * FROM policies', engine)
    print(f"✅ Policies count after reconciliation: {len(updated_data)} (was {len(all_data)})")
    
    # Show the new records
    new_records = updated_data[updated_data['Policy Number'].str.contains('TEST-.*-RECONCILE', na=False)]
    print(f"\n📋 New reconciled records found: {len(new_records)}")
    if len(new_records) > 0:
        print("New records:")
        for idx, record in new_records.iterrows():
            print(f"  - {record['Customer']}: {record['Policy Number']} ({record['Policy Type']}) - Paid: ${record.get('Agent Paid Amount (STMT)', 0)}")
    
    print("\n🎉 Reconciliation test completed successfully!")
    print("✅ New transactions will now appear in the 'All Policies' page")

except Exception as e:
    print(f"❌ Error during reconciliation test: {str(e)}")
    import traceback
    traceback.print_exc()
