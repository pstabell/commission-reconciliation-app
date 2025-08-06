# Policy Term-Based Transaction Filtering - FINAL WORKING VERSION

## Overview
The Policy Revenue Ledger Reports "Detailed Transactions" view uses sophisticated term-aware filtering to show transactions for policy terms that START in the selected month, while excluding transactions from other terms even if they're for the same policy.

## Date Implemented
- Initial Implementation: August 5, 2025 (Version 3.9.32)
- **FINAL FIX**: August 6, 2025 - Correct term-aware filtering

## The Core Design Principle
**Show ALL transactions for policy TERMS that start in the selected month** - not all transactions for policies, but specifically for the terms that begin in that month.

### Critical Understanding
A single policy can have multiple terms:
- Term 1: NEW transaction on 08/28/2024 (Aug 2024 - Feb 2025)
- Term 2: RWL transaction on 02/28/2025 (Feb 2025 - Aug 2025)

When viewing August 2024, we should see ALL transactions for Term 1, but NO transactions for Term 2.

## The FINAL Working Implementation

### Key Components

#### 1. Month Selection Creates Year-Month Filter
```python
# Convert selected month to YYYY-MM format
selected_date = pd.to_datetime(selected_month)
selected_ym = selected_date.strftime('%Y-%m')

# Ensure Year-Month column exists
if 'Year-Month' not in working_data.columns:
    working_data['Year-Month'] = pd.to_datetime(working_data['Effective Date'], errors='coerce').dt.strftime('%Y-%m')
```

#### 2. Find NEW/RWL Transactions in Selected Month
```python
# Find all NEW/RWL transactions effective in the selected month
new_rwl_in_month = working_data[
    (working_data['Transaction Type'].isin(['NEW', 'RWL'])) & 
    (working_data['Year-Month'] == selected_ym)
]
```

#### 3. Process Each Term Individually
For each NEW/RWL found in the selected month:
```python
# Process each NEW/RWL transaction to find its term boundaries
for _, term_defining_row in new_rwl_in_month.iterrows():
    policy_num = term_defining_row['Policy Number']
    term_eff_date = pd.to_datetime(term_defining_row['Effective Date'])
    term_x_date = pd.to_datetime(term_defining_row['X-DATE']) if pd.notna(term_defining_row.get('X-DATE')) else None
```

#### 4. The Critical Filtering Logic
```python
# For NEW/RWL transactions, be very strict - only include if in selected month
if trans_type in ['NEW', 'RWL']:
    trans_year_month = trans_eff_date.strftime('%Y-%m') if pd.notna(trans_eff_date) else ''
    # Only include if this NEW/RWL is in our selected month
    if trans_year_month == selected_ym:
        include_transaction = True

# Include END transactions within the term dates
elif trans_type == 'END' and pd.notna(trans_eff_date) and term_x_date:
    if term_eff_date <= trans_eff_date <= term_x_date:
        include_transaction = True

# Include STMT/VOID transactions within term
elif '-STMT-' in trans_id or '-VOID-' in trans_id:
    stmt_date = pd.to_datetime(trans_row.get('STMT DATE'), errors='coerce')
    if pd.notna(stmt_date) and term_x_date and term_eff_date <= stmt_date <= term_x_date:
        include_transaction = True
    # Also check if they reference the same term based on effective date
    elif trans_eff_date == term_eff_date:
        include_transaction = True

# Include other transactions (CAN, PMT, etc.) within the term dates
elif pd.notna(trans_eff_date) and term_x_date:
    if term_eff_date <= trans_eff_date <= term_x_date:
        include_transaction = True
```

### The Key Insight: NEW/RWL Must Match Selected Month
The breakthrough fix was making NEW/RWL filtering extremely strict:
- **OLD LOGIC**: Include NEW/RWL if it matches the term's effective date
- **NEW LOGIC**: Include NEW/RWL ONLY if its Year-Month matches the selected month

This prevents future renewals from appearing in past month views.

## Real-World Example: Adam Gomes Policy

### Policy Timeline
- **Term 1**: NEW on 08/28/2024, expires 02/28/2025
- **Term 2**: RWL on 02/28/2025, expires 08/28/2025

### When Viewing August 2024
✅ **WILL SHOW** (Term 1 - started in August 2024):
- NEW transaction (0POM131-IMPORT) - Effective 08/28/2024
- END transactions - Effective dates within term
- STMT transactions - For payments within Term 1
- **Result**: 14 transactions total for Term 1

❌ **WILL NOT SHOW** (Term 2 - starts in February 2025):
- RWL transaction (MBJD1AF) - Effective 02/28/2025
- STMT transactions for Term 2 payments
- **Why**: The RWL Year-Month (2025-02) ≠ Selected Month (2024-08)

### When Viewing February 2025
✅ **WILL SHOW** (Term 2 - started in February 2025):
- RWL transaction (MBJD1AF) - Effective 02/28/2025
- Any END/STMT/VOID transactions for Term 2

❌ **WILL NOT SHOW** (Term 1 - started in August 2024):
- NEW transaction from August 2024
- Any transactions from Term 1

## Common Pitfalls to Avoid

### 1. Don't Filter All Transactions by Date
**WRONG**:
```python
# This would exclude ENDs and STMTs with different dates
month_data = working_data[working_data['Year-Month'] == selected_ym]
```

### 2. Don't Show All Terms for a Policy
**WRONG**:
```python
# This would include all terms, even future renewals
policy_transactions = working_data[working_data['Policy Number'] == policy_num]
```

### 3. Don't Trust Transaction IDs Alone
**WRONG**:
```python
# Transaction IDs can be misleading for matching
if trans_row['Transaction ID'] == term_defining_row['Transaction ID']
```

## The Working Logic Flow

1. **User selects a month** (e.g., August 2024)
2. **Find NEW/RWL transactions** effective in that month
3. **For each NEW/RWL found**:
   - Get the term boundaries (Effective Date to X-DATE)
   - Find all transactions for that policy
   - Filter to include ONLY:
     - NEW/RWL transactions in the selected month
     - END transactions within the term dates
     - STMT/VOID transactions within term or matching term effective date
     - Other transactions within the term dates
4. **Result**: Complete view of terms that started in the selected month

## Benefits of This Approach

1. **Accurate Monthly Views**: Only see terms that actually started in the selected month
2. **Complete Term Information**: See all transactions for those terms, not just partial data
3. **No Future Bleeding**: Future renewals don't appear in past month views
4. **Logical Grouping**: Transactions stay with their proper terms

## Testing Checklist

- [ ] August 2024 view shows only Term 1 for policies that renewed in 2025
- [ ] February 2025 view shows only Term 2 for those same policies
- [ ] All Months view shows both terms properly grouped
- [ ] END transactions appear with their correct terms
- [ ] STMT transactions appear based on term boundaries
- [ ] No duplicate transactions across terms

## Related Features

### Policy Revenue Ledger Page Enhancement (v3.9.35)
The individual Policy Revenue Ledger page now also filters the Effective Date dropdown to show only NEW/RWL dates:
- **Before**: Showed all transaction dates (END, STMT, etc.), causing confusion
- **After**: Shows only policy term start dates (NEW/RWL transactions)
- **Benefit**: Clear policy instance selection, no more selecting endorsement dates by mistake
- **Workflow**: Select policy by its start date → Then optionally filter by X-DATE for specific terms

## Related Documentation
- [Policy Revenue Ledger Reports.md](Policy Revenue Ledger Reports.md) - Full feature documentation
- [RECONCILIATION_SYSTEM.md](RECONCILIATION_SYSTEM.md) - How STMT transactions work
- [CHANGELOG.md](../core/CHANGELOG.md) - Version history

## Summary
**REMEMBER**: The filter finds policy TERMS that start in the selected month, then shows ALL transactions for those specific terms. It does NOT show all transactions for policies - it's term-specific!