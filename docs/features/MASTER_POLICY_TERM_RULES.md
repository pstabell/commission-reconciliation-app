# MASTER POLICY TERM RULES 📋

**Created**: August 8, 2025  
**Last Updated**: August 8, 2025  
**Version**: 1.1  
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

**Principle**: Transactions on expiration dates become ORPHANS - NO EXCEPTIONS (Updated v1.1).

When a transaction's Effective Date equals the X-DATE (expiration date) of a policy term:
- Transaction becomes an ORPHAN requiring renewal term entry
- Appears at top of ledger with warning indicators
- Forces proper data entry for renewal terms

**Implementation**: Use strict `<` comparison (not `<=`) for X-DATE boundaries

### Rule 3: Standard Date Range Assignment 📊

For all other transactions (not on X-DATE):
- Assign to the term where: `term_eff_date ≤ transaction_eff_date < term_x_date`

## Examples

### Example 1: Any Transaction on X-DATE
```
Term 1: 06/14/2024 to 12/14/2024
Term 2: 12/14/2024 to 06/14/2025

ANY Transaction with Effective Date: 12/14/2024
→ Becomes ORPHAN (not assigned to any term)
→ Appears at top with warning indicators
→ Requires proper renewal term entry
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

### Why X-DATE transactions become orphans (Updated v1.1):
- Eliminates ambiguity about which term a boundary transaction belongs to
- Forces explicit renewal term creation with proper dates
- Prevents accidental assignment to wrong terms
- Ensures data integrity and accurate commission tracking
- Visual warnings make orphans impossible to miss

## Implementation Details

### Location in Code
- File: `commission_app.py`
- Individual Policy Revenue Ledger: Lines ~15711-15753 (uses < for X-DATE)
- Policy Revenue Ledger Reports: Lines 14688, 14694, 14698 (fixed in v1.1 to use <)

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