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
- **Horizontal Scrolling**: Use browser zoom-out (Ctrl -) to see more columns
- **Formatted Display**: Currency and date fields are properly formatted
- **Responsive Height**: Table adjusts to show data efficiently

**Best Practices**:
- Use browser zoom-out to see more columns
- Scroll horizontally for wide tables
- Use this view to get a complete picture of your data

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
- **Editable Ledger**: Modify individual transactions
- **Running Totals**: See credits, debits, and balance due
- **Audit Protection**: Critical fields are protected from accidental changes

**How to use**:
1. **Search for Policy**: Use the dropdown filters to locate a specific policy
2. **Review Transactions**: See all related transactions in ledger format
3. **Edit Details**: Modify policy-level information
4. **Update Ledger**: Make transaction-level changes as needed
5. **Save Changes**: Commit all modifications

---

## 📊 Policy Revenue Ledger Reports

**What it does**: Advanced reporting with templates and customization

**Key Features**:
- **View Toggle**: Switch between aggregated (one row per policy) and detailed (all transactions) views
- **Policy Aggregation**: One row per policy with totals (in aggregated view)
- **Transaction Details**: See all individual transactions with types and terms (in detailed view)
- **Template System**: Save and reuse report configurations (persists between sessions)
- **Column Selection**: Choose exactly what to display
- **Balance Filters**: Filter by positive, zero, negative, or non-zero balances
- **Pagination**: Handle large datasets efficiently
- **Enhanced Export**: Include report parameters in exports

**Advanced Features**:
1. **View Mode Selection**: 
   - Aggregated by Policy: Summary view with one row per policy
   - Detailed Transactions: All transactions visible for dispute resolution
2. **Template Management**: Save, load, edit, and delete report templates
3. **Quick Presets**: Use predefined column sets (Financial Focus, Basic Info)
4. **Column Reordering**: Drag and drop to arrange columns
5. **Metadata Export**: Export includes report parameters and timestamps

---

## 🛠️ Tools

**What it does**: Utility functions for data management and calculations

**Key Sections**:

### Data Tools
- **Commission Calculator**: Quick premium and commission calculations
- **ID Generators**: Create Client IDs and Transaction IDs
- **Policy Origination Date Tool**: Bulk populate missing origination dates

### Import/Export Tools
- **Export Data**: Download all policies as CSV or formatted Excel
- **Import Data**: Upload CSV or Excel files (validation only)
- **Update Existing Transactions**: Bulk update from modified Excel files

**NEW - Excel Update Tool**:
1. **Purpose**: Update multiple existing transactions without creating new ones
2. **How it works**:
   - Upload Excel file with Transaction ID column
   - System matches Transaction IDs to existing records
   - Preview shows which transactions and columns will be updated
   - Only columns in your Excel are updated, others remain unchanged
3. **Safety Features**:
   - No new transactions created
   - Preview before committing changes
   - Detailed error reporting
   - Excel report with update summary
4. **Use Cases**:
   - Bulk corrections after export
   - Update specific fields across many transactions
   - Fix data issues discovered in reports