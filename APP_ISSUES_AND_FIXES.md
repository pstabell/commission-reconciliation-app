# Application Issues and Fixes - Technical Documentation

This document provides detailed technical information about issues encountered and their solutions.

## Table of Contents
1. [Session State KeyError Fix](#session-state-keyerror-fix)
2. [New Rows Disappearing Fix](#new-rows-disappearing-fix)
3. [Duplicate Creation Fix](#duplicate-creation-fix)
4. [Delete Functionality Fix](#delete-functionality-fix)
5. [Transaction ID Auto-Generation Fix](#transaction-id-auto-generation-fix)
6. [Number Formatting Fix](#number-formatting-fix)
7. [Client ID Consistency Fix](#client-id-consistency-fix)
8. [Deletion History Implementation](#deletion-history-implementation)
9. [Database Column Update](#database-column-update)
10. [Double-Entry Accounting System](#double-entry-accounting-system)
11. [Number Display Formatting Fix](#number-display-formatting-fix)
12. [JSON Serialization Error Fix](#json-serialization-error-fix)
13. [Page Refresh After Delete Fix](#page-refresh-after-delete-fix)
14. [Deletion History Restore Fix](#deletion-history-restore-fix)

---

## Session State KeyError Fix

### Issue
```
KeyError: 'st.session_state has no key "edit_policies_editor"'
```

### Root Cause
Streamlit session state was not properly initialized before accessing the data editor key.

### Solution
Added session state initialization at the beginning of the Edit Policies function:

```python
# Line ~850 in commission_app.py
if 'edit_policies_editor' not in st.session_state:
    st.session_state.edit_policies_editor = None
```

### Technical Details
- Streamlit creates session state keys dynamically when components are rendered
- Accessing a key before the component exists causes KeyError
- Solution ensures key exists before any access attempts

---

## New Rows Disappearing Fix

### Issue
When clicking the "+" button in Streamlit's data_editor, new rows would disappear on save.

### Root Cause
Streamlit's data_editor has a known limitation where the "+" button duplicates the last row's data, including the Transaction_ID, causing unique constraint violations.

### Solution
Implemented a manual "Add New Transaction" button that adds truly blank rows:

```python
# Line ~900 in commission_app.py
if st.button("➕ Add New Transaction", type="primary"):
    # Create a new row with only Client_ID populated
    new_row = pd.DataFrame({
        'Transaction_ID': [''],
        'Client_ID': [selected_client_id],
        # ... other columns with empty values
    })
    edit_df = pd.concat([edit_df, new_row], ignore_index=True)
```

### Technical Details
- Removed reliance on data_editor's built-in "+" button
- Manual button creates rows with empty Transaction_ID
- IDs are generated only when saving to database

---

## Duplicate Creation Fix

### Issue
Editing existing transactions created duplicates instead of updating the original records.

### Root Cause
The save logic was treating all rows as new inserts, ignoring existing Transaction_IDs.

### Solution
Implemented proper INSERT vs UPDATE logic:

```python
# Line ~950 in commission_app.py
for index, row in edited_df.iterrows():
    transaction_id = row.get('Transaction_ID', '')
    
    if pd.isna(transaction_id) or transaction_id == '':
        # Generate new ID for insert
        transaction_id = generate_unique_transaction_id()
        # INSERT operation
    else:
        # UPDATE operation for existing ID
        result = supabase.table('policies').update(
            row_dict
        ).eq('Transaction_ID', transaction_id).execute()
```

### Technical Details
- Check if Transaction_ID exists and is not empty
- Empty IDs trigger INSERT with new generated ID
- Existing IDs trigger UPDATE to preserve record identity

---

## Delete Functionality Fix

### Issue
Delete functionality was selecting wrong rows due to index mismatch.

### Root Cause
Using DataFrame indices for deletion didn't account for filtering and sorting.

### Solution
Implemented checkbox-based selection:

```python
# Line ~1100 in commission_app.py
# Add selection column
edit_df.insert(0, 'Select', False)

# After editing
selected_rows = edited_df[edited_df['Select'] == True]
if len(selected_rows) > 0:
    if st.button("🗑️ Delete Selected", type="secondary"):
        for _, row in selected_rows.iterrows():
            # Archive to deleted_policies table
            # Delete from main table
```

### Technical Details
- Added "Select" checkbox column at position 0
- Tracks selection state in data_editor
- Iterates through selected rows by Transaction_ID
- Archives before deletion for recovery

---

## Transaction ID Auto-Generation Fix

### Issue
Transaction IDs were being generated when clicking "+", causing confusion and potential duplicates.

### Root Cause
ID generation was happening at row creation time instead of save time.

### Solution
Moved ID generation to the save operation:

```python
# Line ~970 in commission_app.py
def generate_unique_transaction_id():
    while True:
        new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        # Check if ID exists in database
        result = supabase.table('policies').select('Transaction_ID').eq('Transaction_ID', new_id).execute()
        if not result.data:
            return new_id
```

### Technical Details
- IDs are 7 characters (A-Z, 0-9)
- Generated only when saving to database
- Uniqueness verified against existing records
- Retry logic if collision occurs

---

## Number Formatting Fix

### Issue
Currency values displayed inconsistent decimal places (e.g., "100.5" instead of "100.50").

### Root Cause
Python's default float formatting doesn't enforce decimal places.

### Solution
Applied consistent formatting to all currency columns:

```python
# Line ~1200 in commission_app.py
currency_columns = ['Premium', 'Agent_Commission', 'Company_Commission', 'Total_Commission']
for col in currency_columns:
    if col in df.columns:
        df[col] = df[col].apply(lambda x: f"{float(x):.2f}" if pd.notna(x) else "0.00")
```

### Technical Details
- Identifies all currency columns
- Applies .2f format to ensure 2 decimal places
- Handles NaN values with default "0.00"
- Applied consistently across all pages

---

## Client ID Consistency Fix

### Issue
New transactions added under a client in Edit Policies received different Client_IDs.

### Root Cause
Client_ID wasn't being propagated to new rows.

### Solution
Auto-populate Client_ID for new rows based on current client:

```python
# Line ~910 in commission_app.py
# When creating new row
new_row = pd.DataFrame({
    'Transaction_ID': [''],
    'Client_ID': [selected_client_id],  # Use current client's ID
    # ... other columns
})
```

### Technical Details
- Extracts Client_ID from first row of current data
- Applies same Client_ID to all new rows
- Maintains client grouping integrity

---

## Deletion History Implementation

### Issue
No way to recover accidentally deleted records.

### Solution
Created comprehensive deletion archive system:

### 1. Database Table Creation
```sql
-- create_deleted_policies_table.sql
CREATE TABLE deleted_policies (
    deletion_id SERIAL PRIMARY KEY,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_by TEXT,
    Transaction_ID TEXT,
    Client_ID TEXT,
    -- ... all original columns
    restoration_notes TEXT
);
```

### 2. Archive Before Delete
```python
# Line ~1150 in commission_app.py
# Archive record before deletion
archive_data = row.to_dict()
archive_data['deleted_at'] = datetime.now().isoformat()
archive_data['deleted_by'] = 'user'

supabase.table('deleted_policies').insert(archive_data).execute()
```

### 3. Restoration Capability
```python
# Line ~2800 in commission_app.py (Admin Panel)
def restore_deleted_record(deletion_id):
    # Get record from archive
    deleted_record = supabase.table('deleted_policies').select('*').eq('deletion_id', deletion_id).execute()
    
    # Remove deletion metadata
    restore_data = {k: v for k, v in deleted_record.items() 
                   if k not in ['deletion_id', 'deleted_at', 'deleted_by']}
    
    # Insert back to main table
    supabase.table('policies').insert(restore_data).execute()
    
    # Remove from archive
    supabase.table('deleted_policies').delete().eq('deletion_id', deletion_id).execute()
```

### Technical Details
- Soft delete pattern with full recovery
- Tracks deletion timestamp and user
- Last 100 deletions viewable
- Export deletion history as CSV
- Permanent delete option available

---

## Database Column Update

### Issue
Column named "(AZ)" needed to be renamed to "(CRM)".

### Solution
Updated all references throughout the codebase:

```python
# Multiple locations in commission_app.py
# Before: '(AZ)'
# After: '(CRM)'

# Example - Line ~1500
columns = ['Transaction_ID', 'Client_Name', '(CRM)', 'Premium', ...]
```

### Technical Details
- Global find/replace operation
- Updated in column definitions
- Updated in display headers
- Updated in database queries
- Verified in all 13 pages

---

## Double-Entry Accounting System

### Implementation
Created a proper accounting system where commissions earned and payments received are separate transactions.

### Design Principles
1. **Original Transactions = Credits** (what you're owed)
2. **Reconciliation Transactions = Debits** (what you've been paid)
3. **Immutable History** - Never modify original transactions

### Manual Commission Entries Table
```sql
CREATE TABLE manual_commission_entries (
    entry_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Transaction_ID TEXT,
    Policy_Number TEXT,
    Entry_Type TEXT, -- 'PAYMENT', 'ADJUSTMENT', etc.
    Amount DECIMAL(10,2),
    Entry_Date DATE,
    Notes TEXT,
    Created_By TEXT
);
```

### Reconciliation Logic
```python
# Line ~2500 in commission_app.py
# Instead of updating original transaction:
# OLD: UPDATE policies SET Paid = true WHERE Transaction_ID = X

# NEW: Create reconciliation entry
reconciliation_entry = {
    'Transaction_ID': generate_unique_transaction_id(),
    'Policy_Number': original_policy_number,
    'Transaction_Type': 'RECONCILIATION',
    'Premium': -original_premium,  # Negative to offset
    'Agent_Commission': -commission_paid,
    'Notes': f'Payment received for {original_transaction_id}'
}
supabase.table('policies').insert(reconciliation_entry).execute()
```

### Benefits
- Complete audit trail
- No data loss
- Tracks payment lifecycle
- Supports partial payments
- Enables payment history reports

---

## File Organization

### Issue
Project files were cluttered in root directory.

### Solution
Organized into logical folders:

```
SALES COMMISSIONS APP/
├── app_backups/          # All timestamped backups
├── sql_scripts/          # SQL schemas and migrations
├── migration_scripts/    # Database migration tools
├── utility_scripts/      # Fix scripts and utilities
├── archive/              # Old versions
├── config_files/         # Configuration files
└── logs_and_temp/        # Logs and temporary files
```

### Implementation
```bash
# Create folders
mkdir -p app_backups sql_scripts migration_scripts utility_scripts archive config_files logs_and_temp

# Move files (examples)
mv commission_app_backup_*.py app_backups/
mv *.sql sql_scripts/
mv fix_*.py utility_scripts/
```

### Benefits
- Clean root directory
- Easy to find related files
- Better version control
- Simplified backups
- Clear separation of concerns

---

## Technical Lessons Learned

### 1. Streamlit Limitations
- data_editor "+" button duplicates data
- Session state requires explicit initialization
- Widget keys must be unique across reruns

### 2. Database Best Practices
- Always validate unique constraints
- Use soft deletes for recovery
- Implement proper transaction handling
- Separate concerns (earned vs paid)

### 3. User Experience
- Provide clear feedback for all operations
- Make destructive actions reversible
- Show preview before bulk operations
- Maintain data consistency

### 4. Code Organization
- Modular architecture improves maintainability
- Separate configuration from logic
- Use descriptive function names
- Comment complex operations

---

## Number Display Formatting Fix

### Issue
Numeric columns like "Premium Sold" displaying as "915" instead of "915.00" and "Agency Estimated Comm/Revenue (CRM)" showing as "91.5" instead of "91.50".

### Root Cause
Streamlit dataframes weren't configured with proper number formatting for display columns.

### Solution
Added column configuration with NumberColumn formatting across all data displays:

```python
# Lines 1220-1238, 1094-1120, etc. in commission_app.py
column_config = {}
numeric_cols = [
    'Agent Estimated Comm $',
    'BALANCE DUE', 
    'Policy Gross Comm %',
    'Agency Estimated Comm/Revenue (CRM)',
    'Agency Gross Comm Received',
    'Premium Sold',
    'Agent Paid Amount (STMT)',
    'Agency Comm Received (STMT)'
]

for col in numeric_cols:
    if col in data.columns:
        column_config[col] = st.column_config.NumberColumn(
            col,
            format="%.2f",
            step=0.01
        )

# Apply to dataframe
st.dataframe(data, column_config=column_config)
```

### Pages Updated
- Edit Policies in Database
- All Policies in Database  
- Dashboard (search results and recent activity)
- Search & Filter results

---

## JSON Serialization Error Fix

### Issue
"Object of type int64 is not JSON serializable" error when deleting transactions and archiving to deleted_policies table.

### Root Cause
NumPy int64, float64 and other numpy scalar types aren't directly JSON serializable.

### Solution
Convert numpy types to Python native types before JSON serialization:

```python
# Lines 1519-1534 in commission_app.py
if pd.notna(value):
    # Convert to Python native types for JSON serialization
    if hasattr(value, 'item'):  # numpy scalar
        policy_dict[col] = value.item()
    elif isinstance(value, (int, float, bool, str)):
        policy_dict[col] = value
    else:
        policy_dict[col] = str(value)
```

### Technical Details
- `hasattr(value, 'item')` detects numpy scalars
- `.item()` method returns the Python native equivalent
- Fallback to string conversion for other types

---

## Page Refresh After Delete Fix

### Issue
After deleting records in Edit Policies page, the deleted rows remained visible until manual page refresh.

### Root Cause
Streamlit session state for the data editor wasn't being cleared after deletion.

### Solution
Clear all related session state keys before rerun:

```python
# Lines 1552-1565 in commission_app.py
# Clear the editor session state to force refresh
if 'edit_policies_editor' in st.session_state:
    del st.session_state['edit_policies_editor']
if 'edit_policies_editor_widget' in st.session_state:
    del st.session_state['edit_policies_editor_widget']
if 'last_search_edit_policies_editor' in st.session_state:
    del st.session_state['last_search_edit_policies_editor']

st.rerun()
```

### Impact
- Immediate UI update after deletion
- No manual refresh required
- Better user experience

---

## Deletion History Restore Fix

### Issue
Multiple errors when restoring deleted records:
1. "invalid input syntax for type integer: '184.0'"
2. "Could not find the 'customer_name' column of 'policies'"

### Root Cause
1. Float values with .0 weren't being converted to integers for integer columns
2. Metadata columns from deleted_policies table were being included in restore data

### Solution
Proper type conversion and column exclusion:

```python
# Lines 2196-2214 in commission_app.py
# Exclude metadata columns that aren't part of policies table
if col not in ['Restore', 'deletion_id', 'deleted_at', 'transaction_id', 'customer_name']:
    if pd.notna(row[col]):
        value = row[col]
        # Clean numeric values for proper data types
        if isinstance(value, (int, float)):
            # Check if it should be an integer (no decimal part)
            if isinstance(value, float) and value.is_integer():
                restore_data[col] = int(value)
            else:
                restore_data[col] = clean_numeric_value(value)
        else:
            restore_data[col] = value
```

### Technical Details
- Checks if float values have no decimal part using `.is_integer()`
- Converts "184.0" → 184 for integer columns
- Excludes all metadata columns from restore operation
- Only restores actual policy data fields

---

## Reconciliation Column Mapping Issues

### Issue
Commission reconciliation failing with multiple "column not found" errors that flashed too quickly to read.

### Root Causes
1. Database column names didn't match UI field names
2. Code was trying to insert non-existent columns
3. Inconsistent field naming across the application

### Errors Encountered
1. `Could not find the 'Agency Comm Received (STMT)' column` - Database had "Agency Gross Comm Received"
2. `Could not find the 'Agent Paid Amount (STMT)' column` - Database had "Paid Amount"
3. `Could not find the 'Description' column` - Database had "NOTES" instead
4. Field name mismatches in reconciliation JSON ("Commission Paid" vs "Amount Paid" vs "Agent Paid Amount (STMT)")

### Solution
Implemented comprehensive column renaming to ensure consistency:

#### 1. Database Column Renames
```sql
-- Renamed columns in policies table
ALTER TABLE policies RENAME COLUMN "Agency Gross Comm Received" TO "Agency Comm Received (STMT)";
ALTER TABLE policies RENAME COLUMN "Paid Amount" TO "Agent Paid Amount (STMT)";
ALTER TABLE policies DROP COLUMN IF EXISTS "Balance Due";  -- Removed unused column
```

#### 2. Code Updates
```python
# Updated all references throughout the application
# Before:
agency_comm_col = get_mapped_column("Agency Comm Received (STMT)") or "Agency Gross Comm Received"
agent_paid_col = get_mapped_column("Agent Paid Amount (STMT)") or "Paid Amount"

# After:
agency_comm_col = get_mapped_column("Agency Comm Received (STMT)") or "Agency Comm Received (STMT)"
agent_paid_col = get_mapped_column("Agent Paid Amount (STMT)") or "Agent Paid Amount (STMT)"

# Fixed Description to NOTES
notes_col = get_mapped_column("NOTES") or "NOTES"
```

#### 3. Consistent Field Naming
```python
# Standardized all occurrences of "Amount Paid" to "Agent Paid Amount (STMT)"
# This ensures consistency across:
# - Manual entry forms
# - JSON statement details
# - Database inserts
# - Display tables
```

### Debug Logging Implementation
Added comprehensive debug logging system to catch fleeting errors:

```python
# Added debug log functions
def log_debug(message, level="INFO", error_obj=None):
    """Add a debug log entry to session state."""
    if "debug_logs" not in st.session_state:
        st.session_state.debug_logs = []
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    log_entry = {
        "timestamp": timestamp,
        "level": level,
        "message": message
    }
    
    if error_obj:
        log_entry["error_details"] = str(error_obj)
    
    st.session_state.debug_logs.append(log_entry)

# Added Debug Logs tab in Admin Panel
# - View all system events and errors
# - Filter by log level (ERROR, WARNING, INFO, DEBUG)
# - Search functionality
# - Export logs as JSON
# - Persistent error capture
```

### Technical Details
- **Column Mapping System**: Used centralized column_mapping_config.py but ensured UI and DB names match
- **Error Visibility**: Debug logs capture all errors that flash too quickly to read
- **Data Consistency**: All field names now consistent across UI, database, and JSON structures

### Lessons Learned
1. **Consistency is Key**: Having different names for the same field in UI vs database causes confusion
2. **Debug Early**: Implement logging before issues arise to capture fleeting errors
3. **Test Incrementally**: Column renames should be tested one at a time
4. **Document Mappings**: Keep a clear record of all field name mappings

---

*Last Updated: July 4, 2025*