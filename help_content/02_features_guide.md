# 🔧 Complete Features Guide

## 🔐 Security & Login

**What it does**: Protects your commission data with password authentication

**Key Features**:
- **Password Protection**: Required login before accessing any data
- **Session Management**: Stay logged in across different pages
- **Logout Option**: Secure logout button in sidebar

**How to use**:
1. Enter your password at the login screen
2. Access all features after successful login
3. Click "Logout" in sidebar when finished
4. Close browser to automatically end session

---

## 📊 Dashboard

**What it does**: Provides an overview of your commission data and quick access to client information

**Key Features**:
- **Metrics Display**: See total transactions and commission amounts at a glance
- **Client Search**: Quickly find and edit specific client data
- **Pagination**: Browse through client policies 10 at a time
- **Quick Edit**: Add new transactions for existing clients directly from the dashboard
- **Visual Indicators**: STMT and VOID transactions are highlighted in blue and red respectively

**How to use**:
1. Select a client from the dropdown to see their policies
2. Use the page navigation to browse through multiple policies
3. Edit data directly in the table and click "Update This Client's Data"
4. Add new transactions by filling the blank row at the bottom

---

## 📝 Add New Policy Transaction

**What it does**: Adds new insurance policies and transactions to your database

**Key Features**:
- **Client ID Lookup**: Search existing clients by name to auto-fill Client ID
- **Premium Calculator**: Calculate premium sold for endorsements (New - Existing)
- **Live Commission Preview**: See estimated commission as you type
- **Auto-Generated IDs**: Automatic Client ID and Transaction ID creation
- **Date Fields**: Easy date entry with MM/DD/YYYY format

**Step-by-step process**:
1. **Search for existing client** (optional): Type client name to find existing Client ID
2. **Use Premium Calculator** (for endorsements): Enter existing and new premiums
3. **Enter Premium Sold**: This auto-calculates Agency Estimated Commission
4. **Fill out the form**: All yellow highlighted fields are editable
5. **Submit**: Click "Add Transaction" to save

**Pro Tips**:
- The Transaction Type determines commission calculations
- Date fields use MM/DD/YYYY format automatically
- Client ID and Transaction ID are auto-generated for uniqueness

---

## 📋 Reports

**What it does**: Creates customizable reports with filtering and export capabilities

**Key Features**:
- **Column Selection**: Choose exactly which fields to include
- **Date Range Filtering**: Filter by any date field in your data
- **Customer Filtering**: Focus on specific clients
- **Balance Due Filtering**: Find policies with outstanding balances
- **Export Options**: Download as CSV or Excel

**How to create a report**:
1. **Select Columns**: Choose which data fields to include
2. **Set Date Range**: Pick a date column and specify the range
3. **Apply Filters**: Optionally filter by customer or balance due status
4. **Preview**: Review the report in the preview section
5. **Export**: Download as CSV or Excel for further analysis

---

## 📁 All Policies in Database

**What it does**: Displays all policy data in a comprehensive table view

**Key Features**:
- **Complete Data View**: See all policies and transactions at once
- **Visual Transaction Highlighting**: 
  - STMT transactions display with light blue background
  - VOID transactions display with light red background
- **Horizontal Scrolling**: Use browser zoom-out (Ctrl -) to see more columns
- **Formatted Display**: Currency and date fields are properly formatted
- **Responsive Height**: Table adjusts to show data efficiently

**Best Practices**:
- Use browser zoom-out to see more columns
- Scroll horizontally for wide tables
- Use this view to get a complete picture of your data
- Look for colored rows to identify reconciliation and void entries

---

## ✏️ Edit Policies in Database

**What it does**: Search and edit existing policy data with two editing methods

**Key Features**:
- **Search Function**: Find specific policies by customer, ID, or policy number
- **Two Edit Modes**: Table editing with auto-save OR form-based editing
- **Auto-Save Toggle**: Enable/disable automatic saving of changes
- **Form Editor**: Reliable single-transaction editing without interruptions
- **Add New Transactions**: Button to add new rows for existing clients

**Two Ways to Edit**:

### Method 1: Quick Table Edits (with Auto-Save)
1. **Search**: Enter search term and click "Find Records"
2. **Edit Directly**: Click in any cell to modify
3. **Auto-Save**: Changes save automatically as you type
4. **Warning**: App may refresh frequently, interrupting your work

### Method 2: Form-Based Editing (Recommended)
1. **Search**: Find the transaction you want to edit
2. **Select**: Check ONE transaction's checkbox
3. **Click**: "Edit Selected Transaction" button
4. **Edit**: Use the form with proper field types
5. **Save**: Click "Save Changes" when done

**Pro Tips**:
- Use form editing for anything beyond simple number changes
- Auto-save shows status messages as it saves
- Export to Excel for bulk edits, then import back
- The form method prevents data loss from page refreshes

---

## 🔍 Search & Filter

**What it does**: Advanced search and filtering capabilities for finding specific policies

**Key Features**:
- **Column-Specific Search**: Search within any database column
- **Text Matching**: Find partial matches (case-insensitive)
- **Balance Due Filtering**: Show only policies with/without outstanding balances
- **Export Filtered Results**: Download search results as CSV or Excel

**Search Strategies**:
- **By Customer**: Find all policies for a specific client
- **By Policy Number**: Locate a specific policy
- **By Carrier**: See all policies with a particular insurance company
- **By Date Range**: Use effective date or other date fields

---

## ⚙️ Admin Panel

**What it does**: Advanced administrative functions for managing the database structure

**⚠️ Warning**: This section can affect your entire database. Use with caution!

**Key Features**:
- **Column Mapping**: Map database columns to app functions
- **Add/Delete Columns**: Modify database structure
- **Header Renaming**: Change column names
- **Enhanced Backup & Restore**: Database protection and recovery
- **File Upload Mapping**: Configure mapping from uploaded files

**Common Admin Tasks**:
1. **Backup Database**: Always create Enhanced backup before making changes
2. **Column Mapping**: Ensure app functions work with your data structure
3. **Add Columns**: Add new fields as your business needs evolve
4. **Restore**: Recover from backups if needed

---

## 💰 Reconciliation

**What it does**: Comprehensive commission reconciliation and payment tracking

**Key Features**:
- **Statement Import**: Upload commission statements from Excel/CSV files
- **Smart Matching**: Automatically match statement entries to database transactions
- **Manual Adjustments**: Add individual entries or adjustments
- **Payment History**: Track all payments and reconciliations
- **Void Management**: Void and reprocess batches as needed
- **Audit Trail**: Complete history of all reconciliation activities

**Reconciliation Process**:
1. **Import Statement**: Upload Excel/CSV file with commission data
2. **Map Columns**: Map statement columns to database fields
3. **Match Transactions**: Review automated matches and handle exceptions
4. **Process Batch**: Save matched transactions as reconciliation batch
5. **View History**: Review past reconciliations and payment history

---

## 📑 Policy Revenue Ledger

**What it does**: Detailed transaction-level view of individual policies

**Key Features**:
- **Granular Search**: Find policies by customer, type, date, and number
- **Transaction History**: See all transactions for a specific policy
- **X-DATE Term Filter**: NEW! Optional filter to show only transactions for a specific policy term
- **Effective Date Column**: See when each transaction occurred
- **Chronological Sorting**: Transactions ordered by date (oldest first)
- **Editable Ledger**: Modify individual transactions
- **Running Totals**: See credits, debits, and balance due
- **Smart Client ID Display**: Shows most complete policy information available
- **Audit Protection**: Critical fields are protected from accidental changes

**NEW - X-DATE Filter**:
1. **All Terms** (default): Shows complete policy history
2. **Specific Term**: Filter by X-DATE to show only that policy term
3. **Smart Inclusion**: Shows NEW/RWL, endorsements, and payments for the term
4. **Perfect for Disputes**: Present focused data for specific policy periods

**How to use**:
1. **Search for Policy**: Use the dropdown filters to locate a specific policy
2. **Select Term** (optional): Choose specific X-DATE or keep "All Terms"
3. **Review Transactions**: See all related transactions in chronological order
4. **Edit Details**: Modify policy-level information
5. **Update Ledger**: Make transaction-level changes as needed
6. **Save Changes**: Commit all modifications

---

## 📊 Policy Revenue Ledger Reports

**What it does**: Advanced reporting with templates and customization

**Key Features**:
- **Statement Month Filter**: NEW! Filter by effective date month for monthly cohort tracking
- **View Toggle**: Switch between aggregated (one row per policy) and detailed (all transactions) views
- **Policy Aggregation**: One row per policy with totals (in aggregated view)
- **Transaction Details**: See all individual transactions with types and terms (in detailed view)
- **Template System**: Save and reuse report configurations (persists between sessions)
- **Column Selection**: Choose exactly what to display
- **Balance Filters**: Filter by positive, zero, negative, or non-zero balances
- **Pagination**: Handle large datasets efficiently
- **Enhanced Export**: Include report parameters in exports

**NEW - Statement Month Filter**:
1. **All Months** (default): Shows all policies across all time
2. **Specific Month**: Filter to policies effective in that month (e.g., "January 2025")
3. **Monthly Cohorts**: Track what became effective each month
4. **Month Balance**: See total balance due for selected month

**Advanced Features**:
1. **View Mode Selection**: 
   - Aggregated by Policy: Summary view with one row per policy
   - Detailed Transactions: All transactions visible for dispute resolution
2. **Statement Month**: Create monthly sales cohorts by effective date
3. **Template Management**: Save, load, edit, and delete report templates
4. **Quick Presets**: Use predefined column sets (Financial Focus, Basic Info)
5. **Column Reordering**: Drag and drop to arrange columns
6. **Metadata Export**: Export includes report parameters, filters, and timestamps

---

## 🛠️ Tools

**What it does**: Utility functions for data management and calculations

**Key Sections**:

### Data Tools
- **Commission Calculator**: Quick premium and commission calculations
- **ID Generators**: Create Client IDs and Transaction IDs
- **Policy Origination Date Tool**: Bulk populate missing origination dates

### Import/Export Tools

#### 📥 Export Data
**Purpose**: Download your commission data for offline analysis or backup

**Available Formats**:
- **CSV Export**: Simple, universal format that opens in any spreadsheet program
- **Excel Export**: Formatted Excel file with proper column widths and headers

**How to Export**:
1. Go to Tools → Import/Export tab
2. Click either "Export All Data to CSV" or "Export All Data to Excel"
3. File downloads with timestamp in filename (e.g., `all_policies_20250124_093045.xlsx`)

**Export from Reports**:
- Policy Revenue Ledger Reports also has export options
- These exports include only the filtered/selected data
- Multi-sheet Excel exports include Report Parameters sheet

---

#### 📤 Import Data (Validation Only)
**Purpose**: Validate data files before full import (currently in preview mode)

**Supported Formats**: CSV, Excel (.xlsx, .xls)

**Current Functionality**:
- Validates file structure and data
- Shows preview of first 10 rows
- Displays file statistics
- Does NOT actually import to database yet (coming soon)

---

#### 🔄 Update Existing Transactions (Bulk Update Tool)

**Purpose**: Update multiple existing transactions without creating new ones

**Step-by-Step Instructions**:

1. **Prepare Your Excel File**:
   - Must contain "Transaction ID" column (exact spelling with space)
   - Include only columns you want to update
   - Can be exported from Policy Revenue Ledger Reports
   - Multi-sheet files OK (reads "Policy Revenue Report" sheet automatically)
   - Column order doesn't matter - matches by name

2. **Upload Process**:
   - Go to Tools → Import/Export → Update Existing Transactions section
   - Click "Browse files" or drag & drop your Excel file
   - System automatically finds the correct data sheet

3. **Preview & Validation**:
   - Shows first 10 rows of your data
   - Lists which columns will be updated
   - Displays count of matching transactions
   - Shows warning for calculated fields (like Policy Balance Due)
   - No changes made yet - just preview

4. **Review Matches**:
   - "Matching Transactions": How many exist in database
   - "New/Unmatched": Records that won't be updated (no matching ID)
   - Click expander to see list of Transaction IDs to be updated

5. **Execute Update**:
   - Click "Update Transactions" button
   - Progress bar shows real-time status
   - Each transaction processed individually
   - Only updates fields present in your Excel

6. **Results & Report**:
   - Success count shows completed updates
   - Error details available if any fail
   - Download Excel report with:
     - Update Summary sheet
     - Update Details sheet
     - Errors sheet (if any)

**Important Notes**:

✅ **What WILL Be Updated**:
- Any column in your Excel that matches a database field
- Date fields (automatically converted to YYYY-MM-DD)
- Empty cells in Excel will clear those fields in database
- Only existing transactions (matched by Transaction ID)

❌ **What WON'T Be Updated**:
- Transaction ID itself (used for matching only)
- _id field (internal database ID)
- Calculated fields (Policy Balance Due)
- Any column not in your Excel file
- Transactions without matching IDs

**Common Errors & Solutions**:

1. **"Object of type datetime is not JSON serializable"**
   - Already fixed - dates now auto-convert to YYYY-MM-DD

2. **"Could not find the 'Policy Balance Due' column"**
   - This is a calculated field - will be skipped automatically
   - Balance recalculates when viewing reports

3. **"Column policies.TransactionID does not exist"**
   - Make sure column is named "Transaction ID" (with space)

4. **Multi-sheet Excel Issues**:
   - Tool auto-detects "Policy Revenue Report" sheet
   - Or uses last sheet if naming differs
   - Shows which sheet is being read

**Best Practices**:

1. **Always Backup First**: Export current data before bulk updates
2. **Test Small**: Try with a few records first
3. **Verify Column Names**: Must match exactly (case and spaces)
4. **Check Your Dates**: Ensure dates are in recognizable format
5. **Review Changes**: Use the preview to verify before updating

**Workflow Example**:

1. Run Policy Revenue Ledger Report
2. Export to Excel
3. Open in Excel, make corrections
4. Save file (keep Transaction ID column unchanged)
5. Upload to Update tool
6. Review preview and matching count
7. Execute update
8. Download report for records
9. Refresh reports to see updated balances

**Column Mapping Notes**:
- Column names must match EXACTLY
- "Transaction ID" not "Trans ID" or "TransactionID"
- "Agent Estimated Comm $" not "Agent Commission"
- Check the preview to ensure proper matching

**Safety Features**:
- Never creates new transactions
- Preview all changes before executing
- Detailed error reporting
- Comprehensive update report
- Transaction-by-transaction processing
- Original data preserved for unmatched records