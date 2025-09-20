# Edit Policy Transactions Duplicate Bug Fix
**Date**: 2025-01-20
**Fixed**: Transaction duplication when saving edits

## Problem
When editing transactions in the Edit Policy Transactions page, the save function was creating duplicate transactions instead of updating existing ones. This caused transaction counts to jump (e.g., from 425 to 537).

## Root Cause
The bug was in the save logic at line 7641 of commission_app.py. The code used `edit_results` (the filtered dataset) to determine which transactions already existed. When editing a filtered view, transactions outside the current filter were incorrectly identified as "new" and duplicates were created.

```python
# BROKEN CODE:
original_transaction_ids = set(edit_results[transaction_id_col].dropna().astype(str))
```

## Solution
Changed the code to check against ALL transactions in the database, not just the filtered view:

```python
# FIXED CODE:
all_transactions = load_policies_data()
if not all_transactions.empty and transaction_id_col in all_transactions.columns:
    original_transaction_ids = set(all_transactions[transaction_id_col].dropna().astype(str))
```

Also added user_id filtering to the update query for better security in multi-tenant scenarios.

## Impact
- Prevented creation of duplicate transactions when editing
- Fixed transaction count inflation issue
- Improved security with proper user isolation on updates

## Testing
1. Filter transactions to show subset
2. Edit some names and save
3. Transaction count should remain stable
4. No duplicates should be created

## Related Files
- commission_app.py (lines 7638-7645, 7712-7726)
- SQL cleanup script: remove_exact_id_duplicates.sql