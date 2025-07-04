#!/usr/bin/env python3
"""
Final fixes for remaining database operations
"""

import re

# Read the file
with open('commission_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix pattern 1: with engine.begin() as conn: followed by conn.execute
pattern1 = r'with engine\.begin\(\) as conn:\s*\n\s*conn\.execute\(\(update_query\), update_values\)'
replacement1 = '''# Update via Supabase
                                            update_dict = {}
                                            for i, col in enumerate(columns_to_update if 'columns_to_update' in locals() else edited_data.columns):
                                                if col not in ['_id', 'Transaction ID', 'Transaction_ID']:
                                                    update_dict[col] = update_values[i] if i < len(update_values) else None
                                            
                                            transaction_id = row.get('Transaction ID', row.get('Transaction_ID'))
                                            if transaction_id:
                                                try:
                                                    supabase.table('policies').update(update_dict).eq('Transaction ID', transaction_id).execute()
                                                except Exception as update_error:
                                                    st.error(f"Error updating record: {update_error}")'''

content = re.sub(pattern1, replacement1, content, flags=re.MULTILINE)

# Fix pattern 2: conn.execute((''' for commission payments
pattern2 = r'conn\.execute\(\(\'\'\'\s*INSERT INTO commission_[^\']+\'\'\'\),[^)]+\)'
replacement2 = '''# Save to Supabase
                                payment_data = {
                                    "policy_number": policy_number if 'policy_number' in locals() else None,
                                    "customer": customer if 'customer' in locals() else None,
                                    "payment_amount": payment_amount if 'payment_amount' in locals() else None,
                                    "statement_date": statement_date if 'statement_date' in locals() else None,
                                    "payment_timestamp": datetime.datetime.now().isoformat()
                                }
                                supabase.table('commission_payments').insert(payment_data).execute()'''

content = re.sub(pattern2, replacement2, content, flags=re.MULTILINE | re.DOTALL)

# Fix pattern 3: conn.execute((update_sql), update_params)
pattern3 = r'conn\.execute\(\(update_sql\), update_params\)'
replacement3 = '''# Update via Supabase
                        if '_id' in selected_df.columns:
                            policy_id = selected_df.iloc[0]['_id']
                        else:
                            # Get the record ID first
                            search_key = 'Policy Number' if 'Policy Number' in update_params else 'Transaction ID'
                            search_value = update_params.get('policy_number', update_params.get('transaction_id'))
                            if search_value:
                                result = supabase.table('policies').select('_id').eq(search_key, search_value).execute()
                                if result.data:
                                    policy_id = result.data[0]['_id']
                                else:
                                    policy_id = None
                            else:
                                policy_id = None
                        
                        if policy_id:
                            # Remove ID fields from update
                            update_dict = {k: v for k, v in update_params.items() if k not in ['_id', 'policy_number', 'transaction_id']}
                            supabase.table('policies').update(update_dict).eq('_id', policy_id).execute()
                            clear_policies_cache()'''

content = re.sub(pattern3, replacement3, content)

# Write the updated file
with open('commission_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Applied final database fixes!")
print("📋 Fixed:")
print("  - Remaining UPDATE operations")
print("  - Commission payment INSERTs")
print("  - Policy update operations")