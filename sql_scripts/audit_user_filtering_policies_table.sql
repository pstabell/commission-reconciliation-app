-- Audit of policies table queries that need user filtering
-- Generated: 2025-01-22

-- Summary of findings from commission_app.py:

-- 1. QUERIES THAT NEED USER FILTERING:

-- Line 6271: Dashboard Quick Editor - UPDATE without user filter
-- supabase.table('policies').update(update_dict).eq('Transaction ID', transaction_id).execute()
-- ISSUE: Missing user_email/user_id filter - could update other users' data!

-- Line 8103: Edit Policy UPDATE - missing user filter  
-- response = supabase.table('policies').update(save_data).eq(get_mapped_column("Transaction ID"), transaction_id).execute()
-- ISSUE: No user filtering on update operation

-- Line 8450: Edit Transactions bulk update - missing user filter
-- supabase.table('policies').update(update_dict).eq(transaction_id_col, transaction_id).execute()
-- ISSUE: No user filtering - could update other users' transactions

-- Line 9660: Reconciliation update - missing user filter
-- supabase.table('policies').update({'reconciliation_status': 'reconciled', ...}).eq('_id', item['_id']).execute()
-- ISSUE: Updates based on _id without user verification

-- Line 11052: Reconciliation editor update - missing user filter
-- response = supabase.table('policies').update(update_data).eq('Transaction ID', selected_row['Transaction ID']).execute()
-- ISSUE: No user filtering

-- Line 11428: Void reconciliation update - missing user filter
-- supabase.table('policies').update({'reconciliation_status': 'unreconciled', ...}).eq('_id', orig['_id']).execute()
-- ISSUE: Updates based on _id without user verification

-- Line 12762: Merge policy types - NO USER FILTER NEEDED (admin operation)
-- update_response = supabase.table('policies').update({'Policy Type': merge_op['to']}).eq('"Policy Type"', merge_op['from']).execute()
-- NOTE: This appears to be an admin function that should affect all users

-- Line 13208: Merge transaction types - NO USER FILTER NEEDED (admin operation)
-- update_result = supabase.table('policies').update({'Transaction Type': merge["to"]}).eq('Transaction Type', merge["from"]).execute()
-- NOTE: Admin function that should affect all users

-- Line 14352: Commission rule update - missing user filter
-- supabase.table('policies').update({'Agent Estimated Comm $': new_agent_comm}).eq('_id', policy['_id']).execute()
-- ISSUE: Updates based on _id without user verification

-- Line 14875: Policy origination date update - missing user filter
-- supabase.table('policies').update({'Policy Origination Date': update['New Origination Date']}).eq('Transaction ID', update['Transaction ID']).execute()
-- ISSUE: No user filtering

-- Line 15440: CSV import update - missing user filter
-- response = supabase.table('policies').update(update_data).eq('"Transaction ID"', transaction_id).execute()
-- ISSUE: No user filtering on bulk updates

-- Line 8239: DELETE operation - missing user filter
-- supabase.table('policies').delete().eq(transaction_id_col, tid).execute()
-- ISSUE: Could delete other users' data!

-- Line 15729: Bulk delete - missing user filter
-- delete_response = supabase.table('policies').delete().in_('"Transaction ID"', batch_ids).execute()
-- ISSUE: Could delete other users' data in bulk!

-- 2. QUERIES THAT ALREADY HAVE USER FILTERING:
-- Lines 7474-7486: Has user_id/user_email filtering
-- Lines 7823-7834: Has user_id/user_email filtering

-- 3. SELECT QUERIES WITHOUT USER FILTERING (less critical but should be reviewed):
-- Line 1671: Getting all Client IDs (may need filtering)
-- Line 12672: Getting all Policy Types (admin function - OK)
-- Line 13015: Getting all Transaction Types (admin function - OK)