# Import Transaction ID Pattern Plan

**Created**: July 14, 2025  
**Status**: DRAFT  
**Purpose**: Fix transaction ID patterns for import-created transactions to prevent accidental deletion

## Problem Statement

Currently, transactions created during reconciliation import have standard transaction IDs (like 0POM131), making them indistinguishable from regular transactions. This creates risk because:

1. These transactions can be accidentally deleted, breaking reconciliation links
2. No visual or systematic way to identify them as import-created
3. They should have restricted editing (only premium/commission fields)
4. Current protection only covers -STMT, -VOID, -ADJ patterns

## Solution Design

### Transaction Categories (Revised)

1. **Regular Transactions**
   - Pattern: Standard format (MNL-XXXXXX, 0POM131, etc.)
   - Permissions: Fully editable and deletable
   - Examples: Manual entries, normal policy events

2. **Import-Created Transactions** 
   - Current Pattern: Standard format (PROBLEM!)
   - New Pattern: **XXXXXX-IMPORT**
   - Permissions: Partially editable (see field list below), NOT deletable
   - Identifier: Description contains "Created from statement import"

3. **Reconciliation Records**
   - Pattern: XXXXXX-STMT, XXXXXX-VOID, XXXXXX-ADJ
   - Permissions: Hidden from Edit Policy Transactions page
   - Purpose: Immutable payment history

### Editable Fields for Import-Created Transactions

**Editable** (to complete commission calculations):
- Premium Sold
- Commissionable Premium  
- Policy Taxes & Fees
- Policy Gross Comm %
- Agent Comm Rate fields
- Broker Fee (if applicable)
- Policy details (Policy Number, Effective Date, etc.)
- Notes

**Read-Only** (preserve payment integrity):
- Transaction ID
- Agent Paid Amount (STMT)
- Agency Comm Received (STMT)
- STMT DATE
- Customer/Client information
- Reconciliation fields

**Auto-Calculated** (based on editable fields):
- Agency Estimated Comm/Revenue (CRM)
- Agent Estimated Comm $

## Implementation Steps

### IMPORTANT NOTE FOR MIGRATIONS:
When running database migrations, use Supabase SQL Editor directly instead of Python scripts. The SQL approach is simpler and more direct for one-time data updates.

## Implementation Steps

### Phase 1: Update Transaction Generation
1. Modify `generate_transaction_id()` to accept a suffix parameter
2. Update reconciliation import logic to use `-IMPORT` suffix for new transactions
3. Test with new imports to verify pattern

### Phase 2: Migration Script
```python
# Pseudocode for migration
def migrate_import_transaction_ids():
    # 1. Query all transactions with description containing "Created from statement import"
    import_transactions = supabase.table('policies')\
        .select('*')\
        .like('NOTES', '%Created from statement import%')\
        .execute()
    
    # 2. For each transaction, update the ID
    for transaction in import_transactions.data:
        old_id = transaction['Transaction ID']
        new_id = f"{old_id}-IMPORT"
        
        # Check new ID doesn't already exist
        # Update the transaction ID
        # Update any references in reconciliation tables
        
    # 3. Return migration summary
```

### Phase 3: Update Protection Logic
1. Add `-IMPORT` pattern to `is_reconciliation_transaction()` function
2. Create new function `is_import_transaction()` for specific handling
3. Update Edit Policy Transactions page:
   - Prevent deletion of -IMPORT transactions
   - Implement field-level edit restrictions
   - Add visual indicator (icon or color)

### Phase 4: UI Updates
1. Add info icon next to -IMPORT transactions explaining restrictions
2. Disable delete checkbox for -IMPORT transactions
3. Update help text to explain the three transaction categories
4. Consider adding filter: "Show Import-Created Transactions"

## Testing Checklist

- [ ] New imports create XXXXXX-IMPORT pattern IDs
- [ ] Migration script successfully updates existing import transactions
- [ ] -IMPORT transactions cannot be deleted
- [ ] Only allowed fields are editable in -IMPORT transactions  
- [ ] Formulas calculate correctly with partial data
- [ ] Reconciliation still works with new ID pattern
- [ ] No duplicate IDs created during migration
- [ ] Visual indicators display correctly
- [ ] Help documentation is clear

## Rollback Plan

If issues arise:
1. Backup database before migration
2. Keep mapping of old ID -> new ID changes
3. Prepare reverse migration script
4. Test rollback in development first

## Success Criteria

1. Zero import-created transactions can be accidentally deleted
2. Users can complete commission data for import transactions
3. Clear visual distinction between transaction types
4. No disruption to existing reconciliation processes
5. All historical import transactions properly protected

## Notes

- Consider adding `transaction_type` field to database for easier querying
- May want to add audit log for ID migrations
- Future enhancement: Bulk edit tool for completing import transaction data

---

*This plan will be merged into existing documentation after successful implementation and deleted.*