import os

file_path = r"C:\Users\Patri\OneDrive\STABELL DOCUMENTS\STABELL FILES\TECHNOLOGY\PROGRAMMING\SALES COMMISSIONS APP\commission_app.py"
with open(file_path, "r") as f:
    content = f.read()

old_block = """                # Get the statement_id of the rows to delete
                to_delete_ids = payment_history_df.loc[to_delete_indices, 'statement_id'].tolist()

                if to_delete_ids:
                    try:
                        with engine.begin() as conn:
                            # Use statement_id which is the correct unique key for this table
                            delete_query = sqlalchemy.text("DELETE FROM commission_payments WHERE statement_id IN :ids")
                            conn.execute(delete_query, {"ids": to_delete_ids})
                        
                        st.success(f"✅ Deleted {len(to_delete_ids)} selected payment history records.")
                        # Refresh data by re-running the script
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting records: {e}")
                else:
                    st.warning("No records were selected for deletion.")"""

new_block = """                # Get the actual database ID to delete
                to_delete_id = payment_history_df.loc[to_delete_indices, 'id'].tolist()

                if to_delete_id:
                    try:
                        with engine.begin() as conn:
                            # Use the correct primary key 'id' for deletion
                            delete_query = sqlalchemy.text("DELETE FROM commission_payments WHERE id IN :ids")
                            conn.execute(delete_query, {"ids": to_delete_id})
                        
                        st.success(f"✅ Deleted {len(to_delete_id)} selected payment history records.")
                        # Refresh data by re-running the script
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting records: {e}")
                else:
                    st.warning("No records were selected for deletion.")"""

new_content = content.replace(old_block, new_block)

with open(file_path, "w") as f:
    f.write(new_content)

print("File updated successfully.")