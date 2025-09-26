# Dashboard Commission Due Calculation Documentation
**Date**: September 26, 2025
**Author**: Claude

## Summary
The Dashboard correctly shows **$9,824.29** in Agent Commission Due by calculating outstanding balances (what's still owed after reconciliations). The SQL script incorrectly shows **$49,378.71** because it sums ALL commission amounts without considering payments already made.

## Dashboard Calculation Method (CORRECT)

The dashboard uses a **balance-based approach** that follows these steps:

1. **Calculate Credits (Commission Earned)**
   - Takes each original transaction (excludes -STMT-, -VOID-, -ADJ- entries)
   - Uses `Total Agent Comm` field as the credit amount
   - Falls back to `Agent Estimated Comm $` + `Broker Fee Agent Comm` if Total Agent Comm is missing

2. **Calculate Debits (Payments Received)**
   - For each original transaction, finds all matching reconciliation entries
   - Matches by Policy Number AND Effective Date
   - Sums all `Agent Paid Amount (STMT)` from -STMT- and -VOID- entries
   - -VOID- entries have negative amounts that reduce the total paid

3. **Calculate Balance**
   - Balance = Credits - Debits
   - Only positive balances are included in Agent Commission Due
   - This represents what's actually still owed to the agent

## Code Implementation

From `commission_app.py` lines 817-825:

```python
# Calculate total commission due using balance approach
try:
    # Get all transactions with their balances
    trans_with_balance = calculate_transaction_balances(df)
    
    # Sum all positive balances (what's still owed)
    if '_balance' in trans_with_balance.columns:
        unpaid_balances = trans_with_balance[trans_with_balance['_balance'] > 0]
        metrics['agent_comm_due_total'] = unpaid_balances['_balance'].sum()
```

The `calculate_transaction_balances` function (lines 2618-2739):
- Filters to original transactions only
- For each transaction, calculates: credit - debit = balance
- Returns all transactions with their `_balance` column

## Why SQL Shows $49,378.71 (INCORRECT)

The SQL script likely:
1. Sums ALL `Total Agent Comm` amounts
2. Doesn't exclude already-reconciled transactions
3. Doesn't account for payments made (-STMT- entries)
4. Includes transactions with zero or negative balances

## Example

Consider a transaction:
- Policy ABC123, Effective Date 01/01/2025
- Total Agent Comm: $500 (credit)
- Agent Paid Amount (STMT): $500 from reconciliation entry
- Balance: $500 - $500 = $0

**Dashboard**: Correctly excludes this (balance = 0)
**SQL**: Incorrectly includes the $500 in commission due

## Verification

To verify the dashboard calculation:
1. Look at the Unreconciled Transactions tab
2. Sum the Balance column for all transactions with Balance > 0
3. This should match the dashboard's Agent Commission Due figure

## Key Insight

The dashboard implements true **double-entry accounting**:
- Credits = Commission earned
- Debits = Payments received  
- Balance = What's still owed

This is why it correctly shows $9,824.29 - it only counts commissions that haven't been paid yet.

## Related Documentation
- [RECONCILIATION_SYSTEM.md](../features/RECONCILIATION_SYSTEM.md) - Full reconciliation system details
- [2025-09-20-unlock-button-rename-and-commission-fix.md](../changelogs/2025-09-20-unlock-button-rename-and-commission-fix.md) - Recent fix for commission calculations