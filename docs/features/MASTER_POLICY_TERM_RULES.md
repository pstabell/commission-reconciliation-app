# MASTER POLICY TERM RULES 📋

**Created**: August 8, 2025  
**Last Updated**: August 17, 2025  
**Version**: 1.2  
**Purpose**: Define the unbreakable rules for assigning transactions to policy terms

## Overview

The MASTER POLICY TERM RULES ensure that transactions are correctly assigned to policy terms without duplication or confusion. These rules are implemented in the Policy Revenue Ledger Reports to maintain data integrity and accurate reporting.

## The Rules

### Rule 1: One Transaction = One Term ☝️

**Principle**: A transaction is like a person - it can only exist in one place at a time.

- Each transaction belongs to exactly ONE policy term
- No transaction can appear in multiple terms
- Once assigned to a term, a transaction cannot be duplicated

### Rule 2: X-DATE Boundary Rule 📅

**Principle**: Transactions on expiration dates become ORPHANS - EXCEPT CANCELLATIONS (Updated v1.2).

When a transaction's Effective Date equals the X-DATE (expiration date) of a policy term:
- Most transactions become ORPHANS requiring renewal term entry
- **EXCEPTION**: CAN (cancellation) transactions on X-DATE are assigned to the expiring term
- Orphaned transactions appear at top of ledger with warning indicators
- Forces proper data entry for renewal terms

**Implementation**: 
- Use strict `<` comparison for most transaction types
- Use `<=` comparison for CAN transactions only

### Rule 3: Standard Date Range Assignment 📊

For all other transactions (not on X-DATE):
- Assign to the term where: `term_eff_date ≤ transaction_eff_date < term_x_date`

## Examples

### Example 1: Non-CAN Transaction on X-DATE
```
Term 1: 06/14/2024 to 12/14/2024
Term 2: 12/14/2024 to 06/14/2025

END/STMT/etc Transaction with Effective Date: 12/14/2024
→ Becomes ORPHAN (not assigned to any term)
→ Appears at top with warning indicators
→ Requires proper renewal term entry
```

### Example 1a: CAN Transaction on X-DATE (Exception)
```
Term 1: 06/14/2024 to 12/14/2024
Term 2: 12/14/2024 to 06/14/2025

CAN Transaction with Effective Date: 12/14/2024
→ Assigned to Term 1 (expiring term)
→ Uses <= comparison for CAN transactions
→ Prevents orphaned cancellations
```

### Example 2: Transaction Before X-DATE
```
Term 1: 06/14/2024 to 12/14/2024

END Transaction with Effective Date: 12/13/2024
→ Assigned to Term 1 (within term boundaries)
```

### Example 3: Transaction After X-DATE
```
Term 2: 12/14/2024 to 06/14/2025

END Transaction with Effective Date: 12/15/2024
→ Assigned to Term 2 (within new term boundaries)
```

## Business Logic Rationale

### Why X-DATE transactions become orphans (Updated v1.2):
- Eliminates ambiguity about which term a boundary transaction belongs to
- Forces explicit renewal term creation with proper dates
- Prevents accidental assignment to wrong terms
- Ensures data integrity and accurate commission tracking
- Visual warnings make orphans impossible to miss

### CAN Transaction Exception Rationale:
- Cancellations on X-DATE logically belong to the expiring term
- Prevents orphaned CAN transactions that can't be reconciled
- Reflects business logic: a policy canceled on expiration date cancels the expiring term

## Implementation Details

### Location in Code
- File: `commission_app.py`
- Individual Policy Revenue Ledger: Lines ~15711-15753 (uses < for X-DATE)
- Policy Revenue Ledger Reports: Lines 16165-16171 (v1.2 added CAN exception with <=)

### Key Variables
- `term_eff_date`: Start date of the policy term
- `term_x_date`: Expiration date of the policy term
- `trans_eff_date`: Effective date of the transaction
- `trans_type`: Transaction type (NEW, RWL, END, CAN, etc.)

### Algorithm
1. For each policy term (defined by NEW/RWL transactions):
   - Check if a next term exists
   - For each transaction:
     - Skip if already assigned (Rule 1)
     - Check if on X-DATE boundary (Rule 2)
     - Otherwise use standard date range (Rule 3)

## Testing Scenarios

1. **Multiple Terms**: Verify transactions are split correctly between terms
2. **X-DATE Transactions**: Confirm proper assignment based on type
3. **No Duplicates**: Ensure each transaction appears only once
4. **Edge Cases**: Test policies with no renewals
5. **STMT Transactions**: Verify reconciliation entries follow the rules

## Future Considerations

- These rules apply to ALL transaction types (NEW, RWL, END, CAN, STMT, VOID, etc.)
- The rules are designed to be simple and unbreakable
- Any exceptions must be explicitly documented and approved

---

*These MASTER POLICY TERM RULES ensure consistent, logical assignment of transactions to policy terms throughout the application.*