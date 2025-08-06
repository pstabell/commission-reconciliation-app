# Policy Term Filtering Examples - Visual Guide

## Overview
This document provides concrete examples of what transactions appear in the Policy Revenue Ledger Reports "Detailed Transactions" view for different month selections.

## Example: Adam Gomes Policy Timeline

### Policy Structure
**Policy Number**: 1AA338948
**Customer**: Adam Gomes

**Term 1 (Aug 2024 - Feb 2025)**:
- NEW transaction: 0POM131-IMPORT - Effective 08/28/2024
- Multiple END transactions throughout the term
- STMT reconciliation entries for payments
- Total: 14 transactions

**Term 2 (Feb 2025 - Aug 2025)**:
- RWL transaction: MBJD1AF - Effective 02/28/2025
- Additional transactions for this renewal term

---

## What You See in Each Month View

### When Viewing: August 2024 🗓️
**You WILL see** ✅:
```
Transaction ID      Type    Effective Date    Description
0POM131-IMPORT     NEW     08/28/2024        New policy issuance
JWD9KUQ            END     09/15/2024        Endorsement within term
KYT8MXN            END     10/22/2024        Another endorsement
L3RCX2S-STMT       STMT    09/30/2024        Payment reconciliation
M4YDZ3T-STMT       STMT    10/31/2024        Payment reconciliation
...
[Total: 14 transactions for Term 1]
```

**You WON'T see** ❌:
```
MBJD1AF            RWL     02/28/2025        ← Future renewal (Term 2)
N5ZEA4U-STMT       STMT    03/31/2025        ← Term 2 payment
```

**Why**: August 2024 view shows ONLY transactions for terms that START in August 2024.

---

### When Viewing: February 2025 🗓️
**You WILL see** ✅:
```
Transaction ID      Type    Effective Date    Description
MBJD1AF            RWL     02/28/2025        Renewal policy issuance
N5ZEA4U-STMT       STMT    03/31/2025        Payment reconciliation
P6AFB5V            END     04/15/2025        Endorsement within term
...
[All transactions for Term 2]
```

**You WON'T see** ❌:
```
0POM131-IMPORT     NEW     08/28/2024        ← Original policy (Term 1)
JWD9KUQ            END     09/15/2024        ← Term 1 endorsement
L3RCX2S-STMT       STMT    09/30/2024        ← Term 1 payment
```

**Why**: February 2025 view shows ONLY transactions for terms that START in February 2025.

---

### When Viewing: All Months 📅
**You WILL see** ✅:
```
Transaction ID      Type    Effective Date    Description
0POM131-IMPORT     NEW     08/28/2024        Term 1 start
JWD9KUQ            END     09/15/2024        Term 1 endorsement
L3RCX2S-STMT       STMT    09/30/2024        Term 1 payment
...
MBJD1AF            RWL     02/28/2025        Term 2 start
N5ZEA4U-STMT       STMT    03/31/2025        Term 2 payment
...
[All transactions for all terms]
```

**Why**: "All Months" view shows all transactions regardless of term.

---

## More Examples

### Example 2: Policy with Cancellation

**Policy**: ABC123
**Term**: January 2025 - January 2026

When viewing **January 2025**:
```
Transaction ID      Type    Effective Date    Description
Q7BGC6W            NEW     01/15/2025        New policy
R8CHD7X            CAN     03/20/2025        Cancellation
S9DIE8Y-STMT       STMT    02/28/2025        Payment before cancellation
T0EJF9Z-STMT       STMT    04/15/2025        Cancellation refund
```
All these appear because they belong to the term that STARTED in January 2025.

---

### Example 3: Policy with Multiple Endorsements

**Policy**: XYZ789
**Term**: June 2024 - June 2025

When viewing **June 2024**:
```
Transaction ID      Type    Effective Date    Description
U1FKG0A            NEW     06/01/2024        New policy
V2GLH1B            END     06/15/2024        Add vehicle
W3HMI2C            END     08/20/2024        Change coverage
X4INJ3D            END     11/10/2024        Add driver
Y5JOK4E-STMT       STMT    Monthly           Multiple payment entries
```

When viewing **June 2025** (if renewed):
```
Transaction ID      Type    Effective Date    Description
Z6KPL5F            RWL     06/01/2025        Renewal only
```
The renewal term starts fresh - previous term's endorsements don't carry over.

---

## Key Principles to Remember

1. **Term-Based, Not Policy-Based**: We show complete terms, not complete policies
2. **NEW/RWL Define Terms**: These transactions mark the beginning of a term
3. **Strict Month Matching**: NEW/RWL must occur in the selected month to appear
4. **Complete Term Data**: Once a term qualifies, ALL its transactions appear
5. **No Cross-Term Bleeding**: Terms are isolated from each other

## Common Misunderstandings

### ❌ Wrong: "I selected August 2024, so I should see all August 2024 transactions"
✅ Right: "I selected August 2024, so I see all transactions for terms that STARTED in August 2024"

### ❌ Wrong: "This policy renewed in February, why is it showing in August?"
✅ Right: "The August view shows the original term (Aug-Feb), the February view shows the renewal term (Feb-Aug)"

### ❌ Wrong: "Some transactions are missing from my month view"
✅ Right: "Those transactions belong to a term that started in a different month"

---

## Testing Your Understanding

**Question**: A policy starts on 12/15/2024 and renews on 06/15/2025. When viewing May 2025, what do you see?

**Answer**: Nothing for this policy. May 2025 only shows terms that START in May. The original term started in December 2024, and the renewal term starts in June 2025.

---

*This visual guide helps users understand exactly what to expect when filtering by month in the Policy Revenue Ledger Reports.*