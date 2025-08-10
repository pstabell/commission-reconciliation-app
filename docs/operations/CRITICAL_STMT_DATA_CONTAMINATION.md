# CRITICAL: STMT Data Contamination in -IMPORT Transactions

**Issue Date**: August 10, 2025  
**Severity**: CRITICAL  
**Affected Transactions**: -IMPORT transactions from July 2025 reconciliation

## Executive Summary

A critical data integrity issue has been discovered where -IMPORT transactions have been incorrectly populated with STMT column data. These columns should ONLY contain data in reconciliation entries (-STMT-, -VOID-, -ADJ- transactions), never in regular policy transactions or -IMPORT transactions.

## The Problem

### What Happened
During the July 2025 reconciliation process, -IMPORT transactions were incorrectly updated with payment data in the following columns:
- `Agent Paid Amount (STMT)`
- `Agency Comm Received (STMT)`
- `STMT DATE`

Additionally, matched policy transactions may have been incorrectly populated with data in:
- `Agency Estimated Comm/Revenue (CRM)` - This should NOT be updated during reconciliation

### Why This Is Wrong
1. **-IMPORT transactions** are policy transactions created from statement data when no match is found
2. **-STMT- transactions** are reconciliation entries that record actual payments
3. The STMT columns should ONLY have values in reconciliation entries, not in policy transactions
4. **Matched policy transactions** should NEVER be updated with ANY data during reconciliation - only NEW reconciliation entries should be created

### Example of Contaminated Data
```
Transaction ID: S140O3Z-IMPORT
Customer: Judith Concanon
Agent Paid Amount (STMT): $16.41  ❌ SHOULD BE NULL
```

## Root Cause Analysis

### Expected Reconciliation Flow
1. Statement imported with payment data
2. For unmatched items:
   - Create -IMPORT transaction (policy record) with commission data
   - Create -STMT- transaction (reconciliation entry) with payment data
3. Link them via reconciliation_id

### What Actually Happened
The reconciliation process appears to have:
1. Created -IMPORT transactions correctly
2. BUT populated STMT fields directly on the -IMPORT transactions
3. May or may not have created proper -STMT- entries

## Impact

### Data Integrity Issues
- Policy transactions incorrectly show as having received payments
- Balance calculations may be incorrect
- Reports showing both estimated and actual payments on same record
- Audit trail compromised

### Affected Features
- Policy Revenue Ledger balance calculations
- Reconciliation reports
- Outstanding balance tracking
- Commission payment audit trails

## Solution

### Immediate Fix
1. Run diagnostic script to identify all affected -IMPORT transactions
2. Clear STMT fields (set to NULL) on all -IMPORT transactions
3. Verify proper -STMT- entries exist for reconciliation tracking
4. Create backup before making changes

### Script Usage
```bash
cd diagnostic_scripts
python fix_import_stmt_contamination.py
```

The script will:
1. Analyze all -IMPORT transactions
2. Identify those with STMT data
3. Check for corresponding -STMT- entries
4. Create a backup CSV
5. Clear STMT fields (with confirmation)

## Prevention

### Code Review Needed
1. Review reconciliation import logic - it should ONLY:
   - Create NEW -STMT- transactions for matched items
   - Create NEW -IMPORT- and -STMT- transactions for unmatched items
   - NEVER update existing policy transactions
2. Ensure -IMPORT transactions NEVER receive STMT data
3. Add validation to prevent STMT data on non-reconciliation transactions
4. Ensure matched policy transactions are NEVER updated with any data
5. Use the enhanced matched transactions table to provide full transparency
6. Consider database constraints

### Key Principle
**The reconciliation process should be READ-ONLY for existing transactions and only CREATE new reconciliation entries**

### Proposed Validation
```python
def validate_stmt_data(transaction_id, data):
    """Ensure STMT fields only populated on reconciliation transactions."""
    if not any(suffix in transaction_id for suffix in ['-STMT-', '-VOID-', '-ADJ-']):
        # Remove any STMT fields if present
        stmt_fields = ['Agent Paid Amount (STMT)', 'Agency Comm Received (STMT)', 'STMT DATE']
        for field in stmt_fields:
            if field in data:
                del data[field]
    return data
```

## Verification Steps

After running the fix:

1. **Check -IMPORT Transactions**
   - View any -IMPORT transaction in Edit Policies
   - Verify STMT fields are empty/NULL
   - Confirm only commission fields have values

2. **Check -STMT- Transactions**
   - Go to Reconciliation → Reconciliation History
   - Verify -STMT- entries still have payment data
   - Confirm totals match original statement

3. **Check Balance Calculations**
   - View Policy Revenue Ledger for affected policies
   - Verify balances calculate correctly
   - Outstanding balance = Agent Comm - STMT payments

## Long-term Recommendations

1. **Add Database Constraints**
   - Consider check constraints to prevent STMT data on wrong transaction types
   - Add triggers to validate data integrity

2. **Enhance Reconciliation Logic**
   - Clear separation between policy and payment data
   - Explicit validation before database updates
   - Better error handling and logging

3. **Improve Testing**
   - Add test cases for reconciliation data separation
   - Verify STMT fields only on appropriate transactions
   - Test balance calculations with various scenarios

## Related Documentation
- [Reconciliation System Design](../features/RECONCILIATION_SYSTEM.md)
- [Known Issues and Fixes](KNOWN_ISSUES_AND_FIXES.md)
- [Database Protection Implementation](../archive/old_versions/DATABASE_PROTECTION_IMPLEMENTATION.md)

---

**IMPORTANT**: This is a critical data integrity issue that affects financial calculations. Handle with extreme care and always create backups before making corrections.