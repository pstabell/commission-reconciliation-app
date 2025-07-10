# Shared Edit Transaction Form Implementation Plan

## Overview
Implement the Edit Transaction form from "Edit Policy Transactions" page on the "Pending Policy Renewals" page to ensure consistency and single-source maintenance.

## Current State Analysis

### Edit Transaction Form Location
- **Function**: `edit_transaction_form()` in commission_app.py
- **Current Usage**: Only on Edit Policy Transactions page
- **Form Elements**: All policy fields, validation, calculations, save logic

### Pending Policy Renewals Current State
- Displays renewable policies in a table
- Has "Renew Selected" and "Delete Selected" buttons
- No editing capability currently

## Implementation Strategy

### Phase 1: Add Edit Capability to Pending Renewals Table

#### Step 1.1: Add Edit Button Column
- Add a new column to the pending renewals table with "Edit" buttons
- Each row gets its own Edit button
- Button opens the same modal/form used in Edit Policy Transactions

#### Step 1.2: Create Modal Container
- Add modal/expander container on Pending Policy Renewals page
- This will house the edit_transaction_form when triggered

### Phase 2: Connect Shared Form

#### Step 2.1: Refactor Form Invocation
- When Edit button clicked on Pending Renewals:
  ```python
  if st.button(f"Edit", key=f"edit_renewal_{row_id}"):
      st.session_state.editing_renewal = True
      st.session_state.renewal_to_edit = policy_data
  ```

#### Step 2.2: Display Form in Modal
- Check for editing state
- If editing, show form in modal:
  ```python
  if st.session_state.get('editing_renewal', False):
      with st.expander("Edit Policy Transaction", expanded=True):
          edit_transaction_form(
              policy_data=st.session_state.renewal_to_edit,
              source_page="pending_renewals"
          )
  ```

### Phase 3: Handle Form Context

#### Step 3.1: Add Source Parameter
- Modify `edit_transaction_form()` to accept optional `source_page` parameter
- This helps track where the form was called from

#### Step 3.2: Conditional Save Logic
- If source_page == "pending_renewals":
  - After save, refresh the pending renewals list
  - Clear the renewal editing state
- If source_page == "edit_policies":
  - Current behavior (refresh edit policies view)

### Phase 4: Synchronization Benefits

#### Automatic Synchronization
- Any changes to form fields automatically apply to both pages
- New fields added once, available everywhere
- Validation rules consistent across pages
- Calculation logic maintained in one place

## Technical Implementation Details

### Session State Management
```python
# Add to session state initialization
if 'editing_renewal' not in st.session_state:
    st.session_state.editing_renewal = False
if 'renewal_to_edit' not in st.session_state:
    st.session_state.renewal_to_edit = None
```

### Form Function Modification
```python
def edit_transaction_form(policy_data, source_page="edit_policies"):
    # Existing form code...
    
    # At save button:
    if save_button:
        # Existing save logic...
        
        # Context-specific cleanup
        if source_page == "pending_renewals":
            st.session_state.editing_renewal = False
            st.session_state.renewal_to_edit = None
            st.rerun()
```

### Pending Renewals Page Addition
```python
# In the pending renewals table display
for index, row in renewals_df.iterrows():
    col1, col2, col3, edit_col = st.columns([3, 3, 3, 1])
    # ... existing columns ...
    with edit_col:
        if st.button("✏️", key=f"edit_renewal_{row['Transaction_ID']}"):
            st.session_state.editing_renewal = True
            st.session_state.renewal_to_edit = row.to_dict()

# After the table
if st.session_state.get('editing_renewal', False):
    st.divider()
    with st.container():
        st.subheader("Edit Policy Transaction")
        edit_transaction_form(
            st.session_state.renewal_to_edit,
            source_page="pending_renewals"
        )
```

## Benefits of This Approach

1. **Single Source of Truth**: Form definition exists in one place only
2. **Consistent UX**: Users see the same form regardless of entry point
3. **Easier Maintenance**: Update form once, changes reflect everywhere
4. **Reduced Bugs**: No risk of forms getting out of sync
5. **Future Scalability**: Easy to add form to other pages if needed

## Testing Checklist

- [ ] Edit button appears on each renewal row
- [ ] Clicking Edit opens the form with correct data
- [ ] All fields populate correctly
- [ ] Save updates the correct record
- [ ] Form closes after successful save
- [ ] Pending renewals list refreshes
- [ ] Cancel button works without saving
- [ ] Form appears identical to Edit Policy Transactions version
- [ ] Field changes on one page reflect on the other

## Rollback Plan

If issues arise:
1. Remove Edit buttons from Pending Renewals page
2. Remove modal/form display code
3. No changes needed to core form function
4. Both pages continue working independently

## Future Enhancements

1. **Quick Edit Mode**: Edit certain fields inline without opening full form
2. **Bulk Edit**: Select multiple renewals and edit common fields
3. **Form Templates**: Pre-fill form based on renewal type
4. **Keyboard Shortcuts**: Quick navigation between renewals

## Implementation Order

1. **Day 1**: Add Edit buttons and session state management
2. **Day 2**: Connect form and test display
3. **Day 3**: Handle save logic and page refresh
4. **Day 4**: Testing and refinement
5. **Day 5**: Documentation update

## Success Criteria

- Form changes made on either page are reflected on both
- No duplicate code for form definition
- User experience is seamless and consistent
- No performance degradation
- All existing functionality preserved

---

This plan ensures that the Edit Transaction form becomes a truly shared component, eliminating the need to remember to update it in multiple places when changes are needed.