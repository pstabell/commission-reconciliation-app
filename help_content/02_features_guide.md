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

## 💰 Accounting

**What it does**: Comprehensive commission reconciliation and accounting tools

**Key Features**:
- **Statement Reconciliation**: Match commission statements to database
- **Manual Entry**: Add commission entries individually
- **File Upload**: Import commission statements from files
- **Payment History**: Track all payments and reconciliations
- **Audit Trail**: Complete history of all accounting activities

**Reconciliation Process**:
1. **Choose Entry Method**: Manual entry or file upload
2. **Enter Statement Data**: Add each commission entry
3. **Review Entries**: Check totals and details
4. **Reconcile**: Save to history and mark as complete
5. **View History**: Review past reconciliations

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
- **Policy Aggregation**: One row per policy with totals
- **Template System**: Save and reuse report configurations
- **Column Selection**: Choose exactly what to display
- **Pagination**: Handle large datasets efficiently
- **Enhanced Export**: Include report parameters in exports

**Advanced Features**:
1. **Template Management**: Save, load, edit, and delete report templates
2. **Quick Presets**: Use predefined column sets (Financial Focus, Basic Info)
3. **Column Reordering**: Drag and drop to arrange columns
4. **Metadata Export**: Export includes report parameters and timestamps