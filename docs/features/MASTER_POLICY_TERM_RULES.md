# MASTER POLICY TERM RULES 📋

**Created**: August 8, 2025  
**Version**: 1.0  
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

**Principle**: Transactions on expiration dates belong to the renewal (with one exception).

When a transaction's Effective Date equals the X-DATE (expiration date) of a policy term:

1. **IF** a renewal term exists:
   - **AND** transaction type ≠ CAN → Assign to RENEWAL term
   - **AND** transaction type = CAN → Assign to EXPIRING term
   
2. **IF** no renewal term exists:
   - → Assign to current/expiring term

### Rule 3: Standard Date Range Assignment 📊

For all other transactions (not on X-DATE):
- Assign to the term where: `term_eff_date ≤ transaction_eff_date < term_x_date`

## Examples

### Example 1: Renewal on X-DATE
```
Term 1: 06/14/2024 to 12/14/2024
Term 2: 12/14/2024 to 06/14/2025

RWL Transaction with Effective Date: 12/14/2024
→ Assigned to Term 2 (renewal term)
```

### Example 2: Cancellation on X-DATE
```
Term 1: 06/14/2024 to 12/14/2024
Term 2: 12/14/2024 to 06/14/2025

CAN Transaction with Effective Date: 12/14/2024
→ Assigned to Term 1 (expiring term)
```

### Example 3: No Renewal Exists
```
Term 1: 06/14/2024 to 12/14/2024
No Term 2

END Transaction with Effective Date: 12/14/2024
→ Assigned to Term 1 (only available term)
```

## Business Logic Rationale

### Why X-DATE transactions go to renewal:
- Insurance coverage technically renews at 12:01 AM on the X-DATE
- The old policy expires at 11:59 PM the day before
- Therefore, transactions on X-DATE logically belong to the new term

### Why CAN is the exception:
- Cancellations terminate the existing policy
- They must be associated with the policy being cancelled
- A cancellation cannot belong to a policy that hasn't started yet

## Implementation Details

### Location in Code
- File: `commission_app.py`
- Section: Policy Revenue Ledger Reports
- Lines: ~15664-15702

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