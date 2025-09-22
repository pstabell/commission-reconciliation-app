# Admin Panel Transaction Count Fix

## Date: 2025-01-22

## Issue
The Admin Panel's "Transaction Types & Mapping" tab was showing an incorrect total transaction count of 824 instead of the correct 425 shown in the dashboard. The discrepancy was due to the Admin Panel counting reconciliation transactions (-STMT-, -VOID-, -ADJ-) along with regular policy transactions.

## Root Cause
The Admin Panel was using a simple query to count all transactions:
```python
trans_type_data = supabase.table('policies').select('"Transaction Type"').execute()
```

This included reconciliation transactions that should be excluded from the count.

## Solution
Updated the query to also fetch the Transaction ID and filter out reconciliation entries:
```python
trans_type_data = supabase.table('policies').select('"Transaction Type", "Transaction ID"').execute()

if trans_type_data.data:
    # Filter out reconciliation transactions (-STMT-, -VOID-, -ADJ-)
    # to match the dashboard's calculation
    filtered_data = []
    for row in trans_type_data.data:
        trans_id = row.get('Transaction ID', '')
        trans_type = row.get('Transaction Type')
        # Exclude reconciliation entries
        if trans_id and not any(suffix in str(trans_id) for suffix in ['-STMT-', '-VOID-', '-ADJ-']):
            if trans_type:
                filtered_data.append(trans_type)
    
    trans_type_counts = pd.Series(filtered_data).value_counts().to_dict() if filtered_data else {}
```

## Files Modified
- `/commission_app.py` - Updated the transaction count logic in the Admin Panel (tab10)

## Impact
- The Admin Panel now shows the correct transaction count (425) matching the dashboard
- Transaction type counts are now accurate, excluding reconciliation entries
- No impact on other functionality

## Testing
1. Navigate to Admin Panel > Transaction Types & Mapping
2. Verify the "Total Transactions" metric shows 425 (not 824)
3. Verify individual transaction type counts are correct
4. Confirm dashboard still shows 425 transactions

## Prevention
- Always filter out reconciliation transactions (-STMT-, -VOID-, -ADJ-) when counting policy transactions
- Use the same filtering logic across all pages for consistency
- The dashboard's `calculate_transaction_balances` function already does this correctly