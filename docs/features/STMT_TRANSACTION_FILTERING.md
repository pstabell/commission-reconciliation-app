# STMT Transaction Filtering in Policy Terms

## Overview
STMT (statement/payment) transactions represent commission payments received from carriers. These transactions must be properly associated with their policy terms to ensure accurate revenue tracking and balance calculations.

## Date Implemented
August 5, 2025 (Version 3.9.32)

## The Problem
STMT transactions were not appearing in the Policy Revenue Ledger when filtering by policy term, even though they had Effective Dates within the term period. This was because the system was incorrectly filtering STMT transactions by their STMT DATE (payment/reconciliation date) instead of their Effective Date (when they apply to the policy).

## The Solution

### Consistent Date Filtering
All transactions are now filtered by their **Effective Date** when viewing a policy term:
- **NEW/RWL**: Continue to match by X-DATE (policy expiration)
- **END**: Filter by Effective Date within term
- **STMT/VOID/ADJ**: Filter by Effective Date within term (changed from STMT DATE)

### Why This Matters
1. **Logical Consistency**: A STMT transaction with Effective Date 08/28/2024 belongs to the policy term starting 08/28/2024, regardless of when the payment was actually received
2. **Complete Picture**: Users can see all financial activity affecting a policy term in one view
3. **Accurate Balances**: Term-specific balance calculations include all relevant payments

## Implementation Details

### Policy Revenue Ledger Page
The term filtering logic was updated to use Effective Date for all transaction types:
```python
# All transactions now filtered consistently by Effective Date
if pd.notna(trans_eff_date) and term_eff_date <= trans_eff_date <= term_x_date:
    filtered_rows.append(idx)
```

### Policy Revenue Ledger Reports Page
Enhanced to match the Policy Revenue Ledger logic:
1. Added policy number trimming to handle whitespace
2. Added special STMT transaction handling for missing Client IDs
3. Already uses Effective Date for month filtering (correct behavior)

## Example Scenario
- Policy Term: 08/28/2024 to 02/28/2025
- STMT Transaction: Effective Date 08/28/2024, STMT DATE (reconciled) 10/31/2024

**Before Fix**: STMT transaction would only appear if viewing October 2024 data
**After Fix**: STMT transaction correctly appears in the August 2024 - February 2025 term

## Additional Discovery (v3.9.32 Update)

### The Order of Operations Problem
During testing, we discovered that STMT transactions created during reconciliation inherit the Transaction Type from the original transaction (NEW, END, etc.) rather than having "STMT" as their type. This caused an issue where:

1. STMT transactions with Transaction Type = "END" were being evaluated as regular END transactions
2. The `elif` chain in the filtering logic meant they never reached the STMT checking logic
3. Only STMT transactions with non-standard transaction types were being included

### The Solution
We reordered the filtering logic to check for "-STMT-" in the Transaction ID **FIRST**, before evaluating transaction types. This ensures that:
- All STMT transactions are properly identified by their Transaction ID pattern
- They are filtered by Effective Date regardless of their Transaction Type
- The filtering logic is more robust and handles all reconciliation scenarios

### Code Example
```python
# Check for STMT/VOID transactions FIRST (they might have various transaction types)
if "-STMT-" in str(row.get("Transaction ID", "")) or "-VOID-" in str(row.get("Transaction ID", "")):
    # Include if Effective Date falls within term
    if pd.notna(trans_eff_date) and term_eff_date <= trans_eff_date <= term_x_date:
        filtered_rows.append(idx)
# Then check other transaction types...
```

## Benefits
1. **Data Integrity**: All transactions affecting a policy term are visible together
2. **Consistency**: Both Policy Revenue Ledger pages show identical data
3. **User Experience**: No more confusion about "missing" STMT transactions
4. **Accurate Reporting**: Balance calculations include all relevant payments

## Related Documentation
- [RECONCILIATION_SYSTEM.md](RECONCILIATION_SYSTEM.md) - How reconciliation creates STMT transactions
- [CLAUDE.md](../operations/CLAUDE.md) - Known Issues #31 for technical details