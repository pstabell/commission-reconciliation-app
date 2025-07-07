# Phase 0 Implementation - Option A Code
**Approach**: Hide reconciliation transactions from Edit Policies page  
**Benefit**: Clean interface, reconciliation transactions only visible on Reconciliation page

## 📝 Code Changes Required

### 1. Add Helper Function (Top of commission_app.py, after imports)
```python
def is_reconciliation_transaction(transaction_id):
    """
    Check if transaction is a reconciliation entry that should be locked.
    Returns True for -STMT-, -VOID-, -ADJ- transactions.
    """
    if not transaction_id:
        return False
    
    transaction_id_str = str(transaction_id)
    reconciliation_types = ['-STMT-', '-VOID-', '-ADJ-']
    
    return any(suffix in transaction_id_str for suffix in reconciliation_types)
```

### 2. Update Edit Policies Page Search Results
Find the section in Edit Policies where search results are displayed (around line 2900-3000).

**Current Code** (approximate):
```python
if not customer_data.empty:
    st.success(f"Found {len(customer_data)} transactions for {selected_customer}")
    
    # Display the data editor
    edited_df = st.data_editor(
        customer_data[display_columns],
        # ... rest of configuration
```

**Replace With**:
```python
if not customer_data.empty:
    # Filter out reconciliation transactions
    total_count = len(customer_data)
    customer_data_editable = customer_data[
        ~customer_data['Transaction ID'].apply(is_reconciliation_transaction)
    ].copy()
    
    recon_count = total_count - len(customer_data_editable)
    
    # Show counts
    if recon_count > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"Found {len(customer_data_editable)} editable transactions")
        with col2:
            st.info(f"🔒 {recon_count} reconciliation entries (view in Reconciliation page)")
    else:
        st.success(f"Found {len(customer_data_editable)} transactions for {selected_customer}")
    
    if customer_data_editable.empty:
        st.warning("No editable transactions found. All transactions for this customer are reconciliation entries.")
    else:
        # Display the data editor with only editable transactions
        edited_df = st.data_editor(
            customer_data_editable[display_columns],
            # ... rest of existing configuration stays the same
```

### 3. Update Deletion Logic
Find the deletion section (where rows_to_delete is processed).

**Add Additional Check**:
```python
# When checking if deletion was requested
if st.button("🗑️ Delete Selected Transactions", type="primary", disabled=delete_disabled):
    if edited_df is not None and 'Select' in edited_df.columns:
        rows_to_delete = edited_df[edited_df['Select'] == True]
        
        if not rows_to_delete.empty:
            # Double-check for reconciliation transactions (belt and suspenders)
            recon_attempts = rows_to_delete[
                rows_to_delete['Transaction ID'].apply(is_reconciliation_transaction)
            ]
            
            if not recon_attempts.empty:
                st.error("🔒 Cannot delete reconciliation transactions. This should not happen - please report this error.")
                st.stop()
            
            # Continue with existing deletion logic...
```

### 4. Update Form-Based Editor
Find the form editor section (where single transaction editing happens).

**Add at Beginning of Form**:
```python
# In the form editor section
if st.button("✏️ Edit Selected Transaction", disabled=not bool(selected_row)):
    if selected_row:
        selected_index = customer_data_editable.index[selected_row[0]]
        selected_transaction = customer_data_editable.loc[selected_index].to_dict()
        
        # Safety check (should never happen with Option A)
        if is_reconciliation_transaction(selected_transaction.get('Transaction ID', '')):
            st.error("🔒 Cannot edit reconciliation transactions.")
            st.stop()
        
        # Show the edit form...
```

### 5. Update "Edit All" Mode
If there's an "Edit All" mode that shows many transactions:

```python
# In Edit All mode
if edit_mode == "Edit All":
    # Get data based on filter
    if filter_option == "Recent":
        all_data_filtered = all_data.head(50)
    else:
        all_data_filtered = all_data
    
    # Filter out reconciliation transactions
    all_data_editable = all_data_filtered[
        ~all_data_filtered['Transaction ID'].apply(is_reconciliation_transaction)
    ]
    
    # Show count if any were filtered
    filtered_count = len(all_data_filtered) - len(all_data_editable)
    if filtered_count > 0:
        st.info(f"🔒 {filtered_count} reconciliation transactions hidden. View them in the Reconciliation page.")
```

## 🧪 Quick Test Plan

### Test 1: Basic Filtering
1. Go to Edit Policies
2. Search for a customer with -STMT- transactions
3. ✓ Should see message about locked transactions
4. ✓ Should NOT see -STMT- transactions in editor

### Test 2: No Reconciliation Transactions
1. Search for a customer with only regular transactions
2. ✓ Should work normally, no warning message

### Test 3: All Reconciliation Transactions
1. Search for a customer with ONLY -STMT- transactions
2. ✓ Should see "No editable transactions found" message

### Test 4: Counts Are Correct
1. Search for customer with mixed transactions
2. ✓ Verify editable count + locked count = total

## 📊 Visual Result

**Before Implementation**:
```
Found 10 transactions for ABC Company
[Shows all 10 including -STMT- entries in editor]
```

**After Implementation**:
```
Found 7 editable transactions        🔒 3 reconciliation entries (view in Reconciliation page)
[Shows only 7 regular transactions in editor]
```

## ⚡ Quick Implementation Steps

1. **Add the function** (5 minutes)
   - Copy `is_reconciliation_transaction()` to top of file

2. **Update search results** (10 minutes)
   - Find customer search section
   - Add filtering logic
   - Update success messages

3. **Test** (15 minutes)
   - Search for customer with mixed transactions
   - Verify filtering works
   - Check counts are correct

4. **Deploy** (5 minutes)
   - Commit changes
   - Test in production

**Total Time**: ~35 minutes for basic implementation

## 🎯 Success Indicators

- ✅ No -STMT-, -VOID-, or -ADJ- transactions visible in Edit Policies
- ✅ Clear message about hidden reconciliation entries
- ✅ Users understand where to find reconciliation transactions
- ✅ No ability to accidentally edit or delete reconciliation entries

---

*This Option A implementation provides the cleanest solution with minimal code changes while ensuring complete protection of reconciliation data.*