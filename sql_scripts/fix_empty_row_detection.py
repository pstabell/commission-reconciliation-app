"""
Fix for reconciliation skipping all rows as empty

The issue:
1. When column_mapping doesn't contain 'Customer' or 'Policy Number', 
   the code defaults to empty string ''
2. When pandas reads empty cells, they become NaN, and str(NaN) = 'nan'
3. The empty check treats 'nan' as empty, so legitimate rows are skipped

The fix needs to:
1. Check if the column mapping is properly configured
2. Handle NaN values correctly - they shouldn't automatically mean "skip"
3. Only skip rows that are truly empty (no data at all)
"""

# Current problematic code:
"""
customer = str(row[column_mapping['Customer']]).strip() if 'Customer' in column_mapping else ''
policy_num = str(row[column_mapping['Policy Number']]).strip() if 'Policy Number' in column_mapping else ''
...
if (not customer or customer.lower() in ['', 'nan', 'none']) and (not policy_num or policy_num.lower() in ['', 'nan', 'none']):
    debug_matches['skipped_empty'] += 1
    continue
"""

# Fixed code should be:
"""
# Extract mapped values more carefully
customer = ''
policy_num = ''
if 'Customer' in column_mapping and column_mapping['Customer'] in row.index:
    val = row[column_mapping['Customer']]
    if pd.notna(val) and str(val).strip():
        customer = str(val).strip()

if 'Policy Number' in column_mapping and column_mapping['Policy Number'] in row.index:
    val = row[column_mapping['Policy Number']]
    if pd.notna(val) and str(val).strip():
        policy_num = str(val).strip()

# Check for truly empty rows - all key fields are missing
# A row needs at least customer OR policy number OR amount to be valid
amount = 0
if 'Agent Paid Amount (STMT)' in column_mapping and column_mapping['Agent Paid Amount (STMT)'] in row.index:
    try:
        amount = float(row[column_mapping['Agent Paid Amount (STMT)']])
    except (ValueError, TypeError):
        amount = 0

# Skip only if ALL key fields are empty/zero
if not customer and not policy_num and amount == 0:
    debug_matches['skipped_empty'] += 1
    continue
"""