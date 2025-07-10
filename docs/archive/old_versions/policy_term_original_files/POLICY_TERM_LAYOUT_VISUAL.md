# Policy Term Field Layout - Visual Guide

## Current Layout Issue
Transaction Type currently stretches across both columns:

```
Row 2: [Carrier Name]        [MGA Name]
Row 2.5: [---------- Transaction Type ----------]  ← Stretches across both columns
Row 3: [Effective Date]      [Policy Origination Date]
```

## Proposed Layout with Policy Term
Transaction Type and Policy Term side by side:

```
Row 2: [Carrier Name]        [MGA Name]
Row 2.5: [Transaction Type]  [Policy Term Months]  ← Better use of space
Row 3: [Effective Date]      [Policy Origination Date]
```

## Benefits
1. **Better space utilization** - No more stretched fields
2. **Logical grouping** - Transaction type and term are related
3. **Clean layout** - Maintains two-column structure throughout

## Code Location
- File: `commission_app.py`
- Line: ~3989-3990
- Section: Add New Policy Transaction → Policy Information

## Implementation
Instead of:
```python
# Row 2.5: Transaction Type
transaction_type = st.selectbox("Transaction Type", ["NEW", "RWL", ...])
```

Use:
```python
# Row 2.5: Transaction Type and Policy Term
col1, col2 = st.columns(2)
with col1:
    transaction_type = st.selectbox("Transaction Type", ["NEW", "RWL", ...])
with col2:
    policy_term = st.selectbox("Policy Term Months", [None, 3, 6, 9, 12], ...)
```