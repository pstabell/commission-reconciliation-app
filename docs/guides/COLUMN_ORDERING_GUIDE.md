# Column Ordering Guide

## Overview

This guide explains how to reorder columns in different parts of the Sales Commission App. Column ordering is implemented differently across various pages, and understanding these implementations is crucial for making successful modifications.

## Table of Contents

1. [Edit Policy Transactions Page](#edit-policy-transactions-page)
2. [Policy Revenue Ledger Reports](#policy-revenue-ledger-reports)
3. [All Policy Transactions Page](#all-policy-transactions-page)
4. [Session State Considerations](#session-state-considerations)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## Edit Policy Transactions Page

### Implementation Details

The Edit Policy Transactions page uses a programmatic column ordering system that builds the column order dynamically.

#### Key Code Locations

**File**: `commission_app.py`
**Lines**: ~4900-4960

#### Column Ordering Process

1. **Priority Columns Array**: The system builds a `priority_cols` array that defines the order:
   ```python
   priority_cols = ['Select']  # Always first
   
   # Add ID columns
   if transaction_id_col and transaction_id_col in all_cols:
       priority_cols.append(transaction_id_col)
   if client_id_col and client_id_col in all_cols:
       priority_cols.append(client_id_col)
   
   # Add core columns
   if 'Customer' in all_cols:
       priority_cols.append('Customer')
   if 'Policy Number' in all_cols:
       priority_cols.append('Policy Number')
   
   # Add date columns in specific order
   date_cols_ordered = ['Policy Origination Date', 'Effective Date', 'X-DATE', 'Policy Term']
   for col in date_cols_ordered:
       if col in all_cols:
           priority_cols.append(col)
   ```

2. **Remaining Columns**: Any columns not in the priority list are added at the end:
   ```python
   remaining_cols = [col for col in all_cols if col not in priority_cols]
   final_col_order = priority_cols + remaining_cols
   ```

3. **Apply Ordering**: The dataframe is reordered:
   ```python
   edit_results_with_selection = edit_results_with_selection[final_col_order]
   ```

### How to Change Column Order

1. **Locate the column ordering section** (around line 4940)
2. **Modify the appropriate array**:
   - For date-related columns: Update `date_cols_ordered`
   - For other priority columns: Add them to the priority building logic
3. **Update the session state version** to force a refresh (CRITICAL!):
   ```python
   current_search_state = f"{edit_search_term}_{show_attention_filter}_v3"  # Increment version
   ```

### Example: Moving Policy Term After X-DATE

```python
# Before
date_cols_ordered = ['Policy Origination Date', 'Effective Date', 'Policy Term', 'X-DATE']

# After
date_cols_ordered = ['Policy Origination Date', 'Effective Date', 'X-DATE', 'Policy Term']
```

## Policy Revenue Ledger Reports

The Policy Revenue Ledger Reports page uses a template-based system with drag-and-drop functionality.

### Features

- User-configurable column selection
- Drag-and-drop reordering
- Save/load templates
- Default template setting

### Configuration Location

Templates are stored in: `config_files/prl_templates.json`

### How to Change Default Column Order

1. **Via UI**:
   - Navigate to Policy Revenue Ledger Reports
   - Use the column selector to choose and order columns
   - Save as template
   - Click the star button to set as default

2. **Via Code**:
   - Modify the default column order in the template initialization code
   - Update `prl_templates.json` directly

## All Policy Transactions Page

### Implementation Details

**File**: `commission_app.py`  
**Lines**: ~4600-4620

The All Policy Transactions page uses a `preferred_order` array:

```python
preferred_order = [
    '_id', 'Transaction ID', 'Client ID', 'Customer', 
    'Policy Number', 'Prior Policy Number',
    'Carrier Name', 'MGA Name',
    'Policy Type', 'Transaction Type',
    'Policy Origination Date', 'Effective Date', 'X-DATE', 'Policy Term',
    'Premium Sold', 'Policy Taxes & Fees', 'Commissionable Premium',
    # ... more columns
]
```

### How to Change Column Order

1. Locate the `preferred_order` array (around line 4602)
2. Rearrange the column names in the desired order
3. Save and refresh the application

## Session State Considerations

### Why Session State Matters

Streamlit caches data in session state for performance. When changing column orders, you must ensure the cached data is refreshed.

### Key Session State Variables

- `edit_policies_editor`: Stores the current dataframe for editing
- `last_search_{editor_key}`: Tracks the last search criteria
- Template selections in Policy Revenue Ledger
- Widget-specific keys like `modal_X-DATE`, `modal_Policy Term`

### Forcing a Session State Refresh

When modifying column orders in code:

1. **Increment version numbers**:
   ```python
   current_search_state = f"{edit_search_term}_{show_attention_filter}_v{n+1}"
   ```

2. **Clear specific session state keys**:
   ```python
   if 'edit_policies_editor' in st.session_state:
       del st.session_state['edit_policies_editor']
   ```

3. **Use different cache keys**:
   ```python
   cache_key = f"data_cache_{datetime.now().strftime('%Y%m%d%H%M%S')}"
   ```

### Widget Session State Limitations

**Important**: Streamlit widgets create immutable session state keys that cannot be modified after the widget is rendered.

**Problem Example**:
```python
# This will cause an error:
st.date_input("Date", key="my_date")
st.session_state["my_date"] = new_date  # ERROR!
```

**Solution Pattern - Pending State**:
```python
# Store pending changes in a different key
st.session_state['pending_date'] = calculated_date

# Apply in a form submit or button click
if st.button("Apply"):
    # Use the pending value to update data
    data['date'] = st.session_state['pending_date']
```

This pattern was successfully used to fix the Policy Term X-DATE calculation issue.

## Best Practices

### 1. Document Your Changes

Always add comments when modifying column orders:
```python
# Reordered to put Policy Term after X-DATE per user request
date_cols_ordered = ['Policy Origination Date', 'Effective Date', 'X-DATE', 'Policy Term']
```

### 2. Test Thoroughly

- Test with existing data
- Test with new searches
- Test after page refresh
- Test with different user sessions

### 3. Consider User Preferences

- Some pages allow user-configurable ordering (Policy Revenue Ledger)
- Others have fixed ordering (Edit Policy Transactions)
- Consider implementing template functionality for fixed-order pages

### 4. Maintain Consistency

- Similar data should appear in similar order across pages
- Date columns should follow a logical progression
- Financial columns should be grouped together

## Troubleshooting

### Column Order Not Updating

**Problem**: Changed column order in code but UI shows old order

**Solutions**:
1. Increment the version in `current_search_state`
2. Clear browser cache and cookies
3. Start a new Streamlit session
4. Check for multiple column ordering locations

### Columns Missing After Reorder

**Problem**: Some columns disappear after reordering

**Causes**:
1. Typo in column name
2. Column not present in data
3. Column filtered out by logic

**Debug Steps**:
```python
# Add debug output
st.write("All columns:", all_cols)
st.write("Priority columns:", priority_cols)
st.write("Final order:", final_col_order)
```

### Session State Conflicts

**Problem**: Weird behavior after column reordering

**Solution**: Clear all related session state:
```python
# Add this temporarily to force full refresh
for key in list(st.session_state.keys()):
    if 'edit' in key or 'search' in key:
        del st.session_state[key]
```

## Column Ordering Locations Reference

| Page | File | Line Numbers | Method |
|------|------|--------------|---------|
| Edit Policy Transactions | commission_app.py | ~4940 | Priority array |
| All Policy Transactions | commission_app.py | ~4607 | Preferred order array |
| Policy Revenue Ledger | commission_app.py | Various | Template-based |
| Reconciliation History | commission_app.py | ~7800 | Inline configuration |

## Future Enhancements

1. **Unified Column Ordering System**: Implement a single configuration file for all column orders
2. **User Preferences**: Allow users to save their preferred column orders
3. **Drag-and-Drop Everywhere**: Extend the Policy Revenue Ledger's drag-and-drop to all pages
4. **Column Groups**: Define logical groups that move together
5. **API for Column Management**: Create functions to manage column ordering programmatically

## Related Documentation

- [Edit Policy Transactions Column Selection Plan](../design/edit_policy_transactions_column_selection_plan.md)
- [Policy Revenue Ledger Reports](../features/Policy%20Revenue%20Ledger%20Reports.md)
- [Default Template Feature](../features/DEFAULT_TEMPLATE_FEATURE.md)
- [UI Design Standards](../design/UI_DESIGN_STANDARDS.md)