# ❓ Frequently Asked Questions

## 🏁 Getting Started

### Q: I'm new to the system. Where should I start?
**A**: Begin with the "📖 Getting Started" tab in this Help section. Then:
1. Explore the Dashboard to understand the interface
2. Add your first policy in "Add New Policy Transaction"
3. Generate a simple report to see how data flows
4. Practice searching and filtering your data

### Q: How do I add my existing policies to the system?
**A**: You have several options:
- **Manual Entry**: Use "Add New Policy Transaction" for each policy
- **Bulk Upload**: Use Admin Panel to upload Excel/CSV files
- **Copy/Paste**: Use "Edit Policies in Database" to paste data from Excel

### Q: What file formats can I upload?
**A**: The system accepts:
- Excel files (.xlsx, .xls)
- CSV files (.csv)
- PDF files (.pdf) - for commission statements

## 📤 Import & Export Questions

### Q: How do I bulk update transactions after exporting to Excel?
**A**: Use the Update Existing Transactions tool:
1. Export your data from any report
2. Make changes in Excel (keep Transaction ID unchanged)
3. Go to Tools → Import/Export → Update Existing Transactions
4. Upload your modified Excel file
5. Review the preview and click Update Transactions

### Q: Will updating from Excel delete my other data?
**A**: No! The update tool:
- Only updates columns present in your Excel file
- Leaves all other columns unchanged
- Never deletes transactions
- Only updates existing records (matched by Transaction ID)

### Q: What happens to calculated fields like Policy Balance Due?
**A**: Calculated fields are:
- Automatically skipped during updates
- Recalculated when you view reports
- Not stored in the database
- Always based on current data

### Q: My Excel has multiple sheets. Which one is used?
**A**: The tool automatically:
1. Looks for "Policy Revenue Report" sheet first
2. Then searches for sheets with "report" or "policy" in the name
3. Uses the last sheet if no match found
4. Shows which sheet it's reading from

### Q: Can I change the column order in my Excel file?
**A**: Yes! Column order doesn't matter:
- Matching is done by column name, not position
- Rearrange columns however you prefer
- Just ensure column names match exactly

### Q: What if some Transaction IDs don't match?
**A**: Unmatched transactions are:
- Counted as "New/Unmatched"
- Listed in the preview
- Skipped during update (not created as new)
- Reported in the final summary

### Q: How do I know which columns will be updated?
**A**: The preview shows:
- List of columns to be updated
- Count of matching transactions
- Warning for calculated fields
- All before any changes are made

## 💰 Commission Calculations

### Q: How are commissions calculated?
**A**: Commission calculations depend on the Transaction Type:
- **NEW business**: 50% of agency commission
- **Renewals (RWL)**: 25% of agency commission
- **Endorsements (END)**: 50% if new policy, 25% if existing
- **Cancellations (CAN)**: 0%

### Q: Why can't I edit the commission calculation fields?
**A**: These fields are automatically calculated to ensure accuracy:
- Agent Estimated Comm $
- Agency Estimated Comm/Revenue (CRM)
- Policy Balance Due

To change these values, modify the underlying data (Premium Sold, Commission %, etc.).

### Q: What does "Policy Balance Due" mean?
**A**: Policy Balance Due = Commission Owed - Amount Paid
- **Positive amount**: You haven't been paid the full commission yet
- **Zero or negative**: You've been paid in full (or overpaid)

## 📊 Reports & Data

### Q: How do I create a monthly commission report?
**A**: 
1. Go to "Reports" page
2. Select relevant columns (Customer, Policy Number, Commission amounts)
3. Filter by date range (use Effective Date or Statement Date)
4. Add customer filter if needed
5. Export as Excel or CSV

### Q: What's the difference between "All Policies" and "Policy Revenue Ledger"?
**A**: 
- **All Policies**: Shows all transactions as separate rows
- **Policy Revenue Ledger**: Shows individual policy details with transaction history
- **Policy Revenue Ledger Reports**: Aggregates data (one row per policy)

### Q: Can I save report configurations?
**A**: Yes! In "Policy Revenue Ledger Reports":
1. Configure your columns and filters
2. Enter a template name
3. Click "Save Template"
4. Load saved templates anytime

## 🔧 Technical Issues

### Q: I added data but it's not showing up. What's wrong?
**A**: Try these steps:
1. Refresh the page (F5 or Ctrl+R)
2. Check "All Policies in Database" to verify data was saved
3. Verify column mapping in Admin Panel
4. Clear browser cache if issues persist

### Q: Why are some columns highlighted in yellow?
**A**: Yellow highlighting indicates editable input fields where you can enter or modify data. Non-highlighted fields are either:
- Read-only/display fields
- Automatically calculated fields
- System-generated fields (like IDs)

### Q: How do I backup my data?
**A**: Use the Admin Panel Enhanced Backup System:
1. Go to Admin Panel
2. Scroll to "Enhanced Database Backup & Restore System"
3. Enter a description and click "Create Enhanced Backup"
4. Backups are automatically created before major changes

## 💼 Business Workflow

### Q: How do I reconcile my commission statement?
**A**: Use the Reconciliation section:
1. Choose "Manual Entry" or "Upload File"
2. Enter each commission from your statement
3. Review totals to ensure they match your statement
4. Click "Reconcile & Save to History"
5. This creates an audit trail and updates payment records

### Q: How do I track payments from the insurance company?
**A**: 
1. Use "Reconciliation" for commission statement import and matching
2. Enter "Agent Paid Amount (STMT)" for each policy
3. The system automatically calculates Policy Balance Due
4. Use reports to track outstanding balances

### Q: Can I track multiple agents or producers?
**A**: Yes, but you'll need to:
1. Add an "Agent" or "Producer" column (Admin Panel)
2. Include agent name in policy data entry
3. Filter reports by agent name
4. Consider separate databases for completely different agents

## 🔒 Data Security

### Q: Is my data safe?
**A**: Yes, the system includes multiple protection layers:
- Automatic backups before major changes
- Database schema protection to prevent corruption
- Audit trails for all transactions
- Manual backup options
- Recovery tools in Admin Panel

### Q: What happens if I accidentally delete data?
**A**: 
1. Don't panic - data is likely recoverable
2. Go to Admin Panel → Database Recovery Center
3. Look for automatic backups created before the deletion
4. Restore from the most recent backup before the issue

### Q: Can I export all my data?
**A**: Yes:
1. Go to "All Policies in Database"
2. Use browser print function (Ctrl+P) for PDF
3. Or use "Reports" to export specific data as CSV/Excel
4. For complete backup, use Admin Panel download function

## 🎯 Advanced Features

### Q: What is column mapping and do I need it?
**A**: Column mapping tells the app which database columns correspond to which functions:
- **Needed when**: Uploading files with different column names
- **Access via**: Admin Panel
- **Auto-configured**: For standard setups
- **Manual setup**: Required for custom data structures

### Q: How do I add custom fields to track additional data?
**A**: 
1. Go to Admin Panel
2. Use "Add Column" section
3. Enter new column name
4. Confirm addition (this modifies database structure)
5. New field appears in all data entry forms

### Q: Can I change the commission calculation formulas?
**A**: Formula changes require code modification. The current formulas are:
- Built into the application logic
- Documented in the "🧮 Formulas" tab
- Changes need developer assistance

## 🆘 Still Need Help?

### Q: I can't find the answer to my question. What now?
**A**: Try these resources:
1. **Debug Mode**: Enable the debug checkbox in the sidebar for technical details
2. **Admin Panel**: Check the Database Recovery Center for system health
3. **Browser Console**: Press F12 → Console for error messages
4. **Contact Support**: Provide specific error messages and steps to reproduce the issue

### Q: How do I report a bug or request a feature?
**A**: When reporting issues, please include:
- Exact steps that led to the problem
- Error messages (screenshot if possible)
- Browser type and version
- What you expected to happen vs. what actually happened
- Whether the issue is consistent or intermittent

---

## 📞 Quick Reference
  **Emergency Recovery**: Admin Panel → Database Recovery Center
**Backup Data**: Admin Panel → Enhanced Backup System
**Export Data**: Reports → Download as CSV/Excel
**Get Technical Info**: Enable Debug checkbox in sidebar
**Formula Reference**: Help → Formulas tab
**Column Issues**: Admin Panel → Column Mapping