# PRL KeyError 'STMT DATE' Fix - January 22, 2025

## Issue Description
Users encountered a KeyError when accessing the Policy Revenue Ledger Reports page in the "Detailed Transactions" section:
```
KeyError: 'STMT DATE'
File "/opt/render/project/src/commission_app.py", line 20393, in <lambda>
    lambda row: row['STMT DATE'] if ('-STMT-' in str(row['Transaction ID']) or '-VOID-' in str(row['Transaction ID'])) else row['Effective Date'],
```

## Root Cause
The error occurred when users had deselected certain columns (like 'STMT DATE') from their display preferences. The PRL sorting and grouping logic attempted to access these columns directly without checking if they existed in the filtered dataframe.

## Solution Implemented

### 1. Added Required Columns (Lines 20125-20129)
```python
# Also ensure columns needed for sorting and grouping are present
required_cols = ['STMT DATE', 'Effective Date', 'Transaction ID', 'Transaction Type', 'Policy Number', 'X-DATE']
for col in required_cols:
    if col not in editable_data.columns and col in working_data.columns:
        editable_data[col] = working_data[col]
```

### 2. Safe Column Access in Lambda Functions (Line 20399)
```python
# Changed from:
lambda row: row['STMT DATE'] if ('-STMT-' in str(row['Transaction ID']) or '-VOID-' in str(row['Transaction ID'])) else row['Effective Date']

# To:
lambda row: row.get('STMT DATE', row.get('Effective Date', '')) if ('-STMT-' in str(row.get('Transaction ID', '')) or '-VOID-' in str(row.get('Transaction ID', ''))) else row.get('Effective Date', '')
```

### 3. Updated get_type_sort_key Function (Lines 20367-20368)
```python
# Changed from:
trans_id = str(row['Transaction ID'])
trans_type = row['Transaction Type']

# To:
trans_id = str(row.get('Transaction ID', ''))
trans_type = row.get('Transaction Type', '')
```

## Impact
- Users can now access PRL reports regardless of their column selection preferences
- The sorting and grouping logic works correctly even when columns are hidden
- No loss of functionality - hidden columns are used internally for logic but not displayed

## Technical Details
The fix ensures that columns required for internal logic are always available in the dataframe, while respecting the user's display preferences. The columns are added back to `editable_data` only if they exist in `working_data`, preventing any new errors.

## Related Issues
This issue highlighted a broader pattern of hardcoded column references throughout the PRL section. A comprehensive update to use column mapping throughout is tracked as a future enhancement.

## Testing
- Verified that PRL reports load correctly with various column selections
- Tested with all date columns deselected
- Confirmed sorting and grouping logic works as expected
- No performance impact observed