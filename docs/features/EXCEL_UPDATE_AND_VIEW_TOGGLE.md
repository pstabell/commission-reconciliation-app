# Excel Update Tool and View Toggle Features

## Date: 2025-01-24

### Overview
Added two major features to improve data management and reporting flexibility:
1. Excel Update Tool - Bulk update existing transactions from Excel files
2. View Toggle - Switch between aggregated and detailed views in Policy Revenue Ledger Reports

### Feature 1: Excel Update Tool

#### Location
Tools → Import/Export Tools → Update Existing Transactions from Excel

#### Purpose
Allows users to download reports in Excel, make bulk corrections offline, and upload the modified Excel to update only the existing transactions without creating new ones.

#### Key Features
- **Safe Updates Only** - Will ONLY update existing transactions, never create new ones
- **Transaction ID Matching** - Uses the Transaction ID column to match records
- **Selective Column Updates** - Only updates columns present in the Excel file
- **Preview Before Update** - Shows exactly which transactions and columns will be updated
- **Progress Tracking** - Real-time progress bar during updates
- **Error Handling** - Detailed error reporting if any updates fail
- **Multi-sheet Excel Report** - Comprehensive update report with summary, details, and errors

#### How It Works
1. Upload an Excel file containing Transaction ID column
2. System matches Transaction IDs with existing database records
3. Shows preview of matching transactions and columns to be updated
4. Only updates the columns present in the Excel file
5. All other database columns remain unchanged
6. Generates detailed Excel report after completion

#### Technical Implementation
```python
# Only update columns present in Excel, preserve all others
update_data = {}
for col in update_df.columns:
    if col != 'Transaction ID' and col != '_id':
        value = row[col]
        if pd.isna(value):
            update_data[col] = None
        else:
            update_data[col] = value
```

### Feature 2: Policy Revenue Ledger Reports View Toggle

#### Location
Policy Revenue Ledger Reports → Report View Mode section

#### Purpose
Allows users to switch between aggregated (one row per policy) and detailed (all transactions) views based on their reporting needs.

#### View Options
1. **Aggregated by Policy** (Default)
   - One row per unique policy number
   - Sums monetary values (commissions, payments, etc.)
   - Shows first value for descriptive fields
   - Ideal for summary reports and balance reviews

2. **Detailed Transactions**
   - Shows all individual transactions
   - Displays Transaction Type, policy terms, and individual amounts
   - Perfect for commission disputes and detailed auditing
   - Shows transaction-level granularity

#### Key Features
- Radio button toggle for easy switching
- Visual feedback showing active view mode
- Metrics adjust based on view (Total Policies vs Total Transactions)
- Context-specific help text for each view
- All other report features (filters, templates, exports) work with both views

#### Technical Implementation
```python
if view_mode == "Aggregated by Policy":
    # Group by Policy Number with aggregation rules
    agg_dict = {
        # Descriptive fields: take first
        'Customer': 'first',
        'Transaction Type': 'first',
        # Monetary fields: sum
        'Agent Estimated Comm $': 'sum',
        'Agent Paid Amount (STMT)': 'sum'
    }
    working_data = working_data.groupby('Policy Number', as_index=False).agg(agg_dict)
else:
    # Detailed view - no aggregation
    working_data = all_data.copy()
```

### Feature 3: Template Persistence

#### Enhancement
Fixed template saving to persist between sessions using JSON file storage.

#### Location
Policy Revenue Ledger Reports → Template Management

#### Technical Details
- Templates saved to `config_files/prl_templates.json`
- Automatically loaded on page visit
- File added to .gitignore for privacy

### User Benefits

#### Excel Update Tool
1. **Efficiency** - Bulk updates without manual editing each transaction
2. **Safety** - No risk of creating duplicate transactions
3. **Flexibility** - Update only the fields you need to change
4. **Audit Trail** - Complete report of all changes made

#### View Toggle
1. **Versatility** - One report serves multiple purposes
2. **Dispute Support** - Detailed view shows exact transaction types and terms
3. **Summary Analysis** - Aggregated view for high-level reporting
4. **User Choice** - Switch views instantly based on current need

### Files Modified
- `commission_app.py` - Main application file with all feature implementations
- `.gitignore` - Added prl_templates.json to ignore list
- `docs/features/EXCEL_UPDATE_AND_VIEW_TOGGLE.md` - This documentation file

### Important Notes
1. Always backup before bulk updates
2. Excel file must contain Transaction ID column for matching
3. Empty cells in Excel will clear those fields in database
4. View toggle affects export data - choose appropriate view before exporting