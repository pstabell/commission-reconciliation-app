# Hide Rows Functionality

## Date: 2025-01-28

### Overview
Added row-by-row hide functionality to Policy Revenue Ledger Reports, allowing users to hide voided transactions and their associated STMT entries to focus on good transactions.

### Features Implemented

#### 1. Hide Checkbox Column
- Added "Hide" checkbox as the first column in the Report Preview
- Uses `st.data_editor` instead of `st.dataframe` for interactive checkboxes
- All other columns remain read-only

#### 2. Hide Selected Button
- "🙈 Hide Selected" button below the data editor
- Hides all rows with checked Hide checkboxes
- Shows count of hidden rows in "View Hidden (X)" button

#### 3. Hidden Rows Indicator
- Warning message shows "🙈 X rows hidden from view"
- Located just above the Hidden Transactions section
- Only appears when rows are hidden

#### 4. Hidden Transactions Management
- Expandable "🙈 Hidden Transactions" section
- Shows hidden transactions with "Unhide" checkbox column
- Key columns displayed: Transaction ID, Customer, Policy Number, Transaction Type, financial columns
- "✨ Unhide Selected" button to unhide specific rows
- "Unhide All" button to unhide all at once
- Proper number formatting maintained

### Technical Implementation

#### Session State Management
```python
# Track hidden transaction IDs
if 'prl_hidden_rows' not in st.session_state:
    st.session_state.prl_hidden_rows = set()

# Store hidden count for display
st.session_state.prl_hidden_count = hidden_count
```

#### Data Filtering
```python
# Filter out hidden rows before display
if st.session_state.prl_hidden_rows and 'Transaction ID' in working_data.columns:
    working_data = working_data[~working_data['Transaction ID'].isin(st.session_state.prl_hidden_rows)]
```

#### Data Editor Configuration
```python
# Configure Hide checkbox column
column_config['Hide'] = st.column_config.CheckboxColumn(
    'Hide',
    help="Select rows to hide",
    default=False,
    width="small"
)

# Make only Hide column editable
edited_df = st.data_editor(
    editable_data,
    disabled=[col for col in editable_data.columns if col != 'Hide'],
    key="prl_data_editor"
)
```

### User Workflow
1. Check the "Hide" checkbox for rows to hide (e.g., VOID transactions)
2. Click "🙈 Hide Selected" button
3. Hidden rows are removed from the main view
4. Warning shows count of hidden rows
5. Click "View Hidden" to see hidden transactions
6. Use "Unhide" checkboxes to select rows to restore
7. Click "✨ Unhide Selected" or "Unhide All"

### Benefits
- Clean view focusing on good transactions
- Easy to hide/unhide specific transactions
- Visual feedback on hidden row count
- Maintains all existing functionality (templates, formatting, etc.)
- Intuitive checkbox interface

### UI Layout
The hide functionality is organized in the following order:
1. Balance Filters
2. Column Selection & Templates (collapsed)
3. Template Management (collapsed)
4. Saved Templates (collapsed)
5. Hidden Rows Warning (when applicable)
6. Hidden Transactions (expandable)
7. Report Preview (with Hide checkboxes)