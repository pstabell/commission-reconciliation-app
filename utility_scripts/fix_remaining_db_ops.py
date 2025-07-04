#!/usr/bin/env python3
"""
Fix remaining database operations in commission_app.py
"""

import re

# Read the file
with open('commission_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove SQLAlchemy version display
content = content.replace(
    'st.write(f"• SQLAlchemy version: {sqlalchemy.__version__}")',
    'st.write(f"• Database: Supabase Cloud")'
)

# 2. Fix UPDATE operations for dashboard
# First UPDATE operation around line 760
old_update1 = """                                for idx, row in edited_data.iterrows():
                                    update_query = f"UPDATE policies SET "
                                    update_values = []
                                    for col in edited_data.columns:
                                        if col != 'Transaction_ID':  # Don't update primary key
                                            update_query += f"{col} = ?, "
                                            update_values.append(row[col])
                                    
                                    update_query = update_query.rstrip(', ') + " WHERE Transaction_ID = ?"
                                    update_values.append(row['Transaction_ID'])
                                    
                                    with engine.begin() as conn:
                                        conn.execute(sqlalchemy.text(update_query), update_values)"""

new_update1 = """                                for idx, row in edited_data.iterrows():
                                    # Update via Supabase
                                    update_dict = {}
                                    for col in edited_data.columns:
                                        if col not in ['_id', 'Transaction ID']:  # Don't update ID fields
                                            update_dict[col] = row[col]
                                    
                                    # Find the record by Transaction ID
                                    transaction_id = row.get('Transaction ID', row.get('Transaction_ID'))
                                    if transaction_id:
                                        try:
                                            supabase.table('policies').update(update_dict).eq('Transaction ID', transaction_id).execute()
                                        except Exception as update_error:
                                            st.error(f"Error updating record {transaction_id}: {update_error}")"""

content = content.replace(old_update1, new_update1)

# 3. Fix INSERT operation for new policies
old_insert = """                        insert_query = \"\"\"
                        INSERT INTO policies (
                            Client_ID, Transaction_ID, Customer, Policy_Number, Policy_Type,
                            Effective_Date, Transaction_Type, Commission_Paid, Agency_Commission_Received,
                            Premium, Commission_Rate, Balance_Due, Notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        \"\"\"
                        
                        with engine.begin() as conn:
                            conn.execute(sqlalchemy.text(insert_query), [
                                client_id, transaction_id, customer, policy_number, policy_type,
                                effective_date.strftime('%m/%d/%Y'), transaction_type, commission_paid,
                                agency_commission_received, premium, commission_rate, balance_due, notes
                            ])"""

new_insert = """                        # Insert via Supabase
                        new_policy = {
                            "Client ID": client_id,
                            "Transaction ID": transaction_id,
                            "Customer": customer,
                            "Policy Number": policy_number,
                            "Policy Type": policy_type,
                            "Effective Date": effective_date.strftime('%m/%d/%Y'),
                            "Transaction Type": transaction_type,
                            "Agent Estimated Comm $": commission_paid,
                            "Agency Gross Comm Received": agency_commission_received,
                            "Premium Sold": f"${premium:,.2f}" if premium else None,
                            "Policy Gross Comm %": f"{commission_rate}%" if commission_rate else None,
                            "BALANCE DUE": balance_due,
                            "NOTES": notes
                        }
                        
                        supabase.table('policies').insert(new_policy).execute()
                        clear_policies_cache()"""

content = content.replace(old_insert, new_insert)

# 4. Fix to_sql operations for file uploads
# Around line 2118
content = re.sub(
    r'new_df\.to_sql\("policies", engine, if_exists="append", index=False\)',
    '''# Insert via Supabase in batches
                                for _, row in new_df.iterrows():
                                    policy_data = row.to_dict()
                                    # Handle NaN values
                                    for key, value in policy_data.items():
                                        if pd.isna(value):
                                            policy_data[key] = None
                                    try:
                                        supabase.table('policies').insert(policy_data).execute()
                                    except Exception as e:
                                        st.error(f"Error inserting policy: {e}")
                                clear_policies_cache()''',
    content
)

# 5. Fix renewal to_sql operation
content = re.sub(
    r"renewed_rows\.to_sql\('policies', conn, if_exists='append', index=False\)",
    '''# Insert renewed policies via Supabase
                            for _, row in renewed_rows.iterrows():
                                renewal_data = row.to_dict()
                                # Handle NaN values
                                for key, value in renewal_data.items():
                                    if pd.isna(value):
                                        renewal_data[key] = None
                                try:
                                    supabase.table('policies').insert(renewal_data).execute()
                                except Exception as e:
                                    st.error(f"Error inserting renewal: {e}")
                            clear_policies_cache()''',
    content
)

# 6. Fix commission INSERT operations
content = re.sub(
    r'conn\.execute\(sqlalchemy\.text\(\'\'\'\s*INSERT INTO commission_[^\']+\'\'\'\),[^)]+\)',
    '''# Save commission payment to Supabase
                                payment_data = {
                                    "policy_number": policy_number,
                                    "customer": customer,
                                    "payment_amount": payment_amount,
                                    "statement_date": statement_date,
                                    "payment_timestamp": datetime.datetime.now().isoformat(),
                                    "statement_details": json.dumps(statement_details) if statement_details else None
                                }
                                supabase.table('commission_payments').insert(payment_data).execute()''',
    content
)

# 7. Fix renewal history INSERT
content = re.sub(
    r'conn\.execute\(sqlalchemy\.text\("""\s*INSERT INTO renewal_history[^"]+"""\),[^)]+\)',
    '''# Save renewal history to Supabase
                                    renewal_history_data = {
                                        "renewal_timestamp": datetime.datetime.now().isoformat(),
                                        "renewed_by": "User",
                                        "original_transaction_id": original_id,
                                        "new_transaction_id": new_id,
                                        "details": json.dumps({"count": len(renewed_ids), "ids": renewed_ids})
                                    }
                                    supabase.table('renewal_history').insert(renewal_history_data).execute()''',
    content
)

# 8. Remove any remaining sqlalchemy.text() calls
content = content.replace('sqlalchemy.text(', '(')
content = content.replace('from sqlalchemy import text', '')

# 9. Add missing import for json if needed
if 'import json' not in content.split('\n')[:30]:
    lines = content.split('\n')
    for i, line in enumerate(lines[:30]):
        if line.startswith('import'):
            lines.insert(i+1, 'import json')
            break
    content = '\n'.join(lines)

# Write the updated file
with open('commission_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed remaining database operations!")
print("📋 Changes made:")
print("  - Removed SQLAlchemy version display")
print("  - Fixed UPDATE operations for policies")
print("  - Fixed INSERT operations for new policies")
print("  - Fixed to_sql operations for file uploads and renewals")
print("  - Fixed commission payment inserts")
print("  - Fixed renewal history inserts")
print("  - Removed remaining sqlalchemy.text() calls")