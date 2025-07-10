# Policy Term Months - Edit Form Placement Guide

## Current Edit Form Layout
In the Edit Policy Transactions modal, the Policy Information section currently has:

**Top Row (Explicitly placed):**
- Left: Carrier Name
- Right: MGA Name

**Remaining fields (auto-arranged in 2 columns):**
- Policy Type (with dropdown)
- Transaction Type (with dropdown)
- Policy Number
- NEW BIZ CHECKLIST COMPLETE (checkbox)
- FULL OR MONTHLY PMTS (dropdown)
- NOTES
- And other policy fields...

## Recommended Placement for Policy Term Months

### Option 1: Next to Transaction Type (Preferred)
Since Transaction Type is already a dropdown in the policy_fields list, place Policy Term Months immediately after it in the field counter logic. This would typically put them side by side:

```
Row 1: [Carrier Name]         [MGA Name]
Row 2: [Policy Type]          [Policy Number]  
Row 3: [Transaction Type]     [Policy Term Months]  ← Add here
Row 4: [Other fields...]      [Other fields...]
```

### Implementation Location
File: `commission_app.py`
Section: Edit modal → Policy Information (around line 3145)

Add a new condition after the Transaction Type handling:
```python
elif field == 'Transaction Type':
    # Existing Transaction Type dropdown code...
    
elif field == 'Policy Term Months':
    # Policy Term dropdown
    policy_terms = [3, 6, 9, 12]
    current_term = modal_data.get(field, None)
    updated_data[field] = st.selectbox(
        field,
        options=[None] + policy_terms,
        format_func=lambda x: "" if x is None else f"{x} months",
        index=0 if current_term is None else (policy_terms.index(current_term) + 1),
        key=f"modal_{field}",
        help="Select policy duration in months"
    )
```

### Update policy_fields List
In the policy_fields list (line 3074), add 'Policy Term Months' after 'Transaction Type':
```python
policy_fields = ['Writing Code', 'Policy #', 'Product', 'Carrier', 
                 'Policy Type', 'Carrier Name', 'MGA Name', 'Policy Number', 
                 'Transaction Type', 'Policy Term Months', 'NEW BIZ CHECKLIST COMPLETE', 
                 'FULL OR MONTHLY PMTS', 'NOTES']
```

## Why This Placement?
1. **Logical grouping** - Transaction Type and Policy Term are related
2. **Consistent with Add form** - Same side-by-side layout as Add New Policy Transaction
3. **Natural flow** - Users select transaction type, then specify term length
4. **Space efficient** - Both are dropdowns of similar size

## Visual Result
The edit form will have Policy Term Months as a dropdown showing:
- (empty/blank option)
- 3 months
- 6 months  
- 9 months
- 12 months

This matches the Add New Policy Transaction page layout for consistency.