# Troubleshooting Guide - Sales Commission App

This guide helps diagnose and resolve common issues in the Sales Commission Application.

## Table of Contents
1. [Using Debug Logs](#using-debug-logs)
2. [Common Errors and Solutions](#common-errors-and-solutions)
3. [Database Issues](#database-issues)
4. [Reconciliation Problems](#reconciliation-problems)
5. [Performance Issues](#performance-issues)

---

## Using Debug Logs

### Accessing Debug Logs
1. Navigate to **Admin Panel** in the sidebar
2. Click on the **Debug Logs** tab
3. View all system events, errors, and debug information

### Debug Log Features
- **Real-time Logging**: All operations are logged with timestamps
- **Error Capture**: Catches errors that flash too quickly to read
- **Filter by Level**: 
  - ERROR - Critical issues
  - WARNING - Important notices
  - INFO - General information
  - DEBUG - Detailed debugging data
- **Search**: Find specific errors or events
- **Export**: Download logs as JSON for analysis

### How to Use Debug Logs for Troubleshooting
1. **Reproduce the Issue**: Perform the action that causes the error
2. **Check Debug Logs**: Go to Admin Panel → Debug Logs
3. **Filter by ERROR**: Select "ERROR" from the Log Level dropdown
4. **Look for Recent Entries**: Newest logs appear at the top
5. **Expand Error Details**: Click on error entries to see full stack traces

### Example Debug Log Entry
```
[2025-07-04 00:44:49.275] Error inserting policy row 0: Could not find the 'Description' column
Error Details: {
  "message": "Could not find the 'Description' column of 'policies' in the schema cache",
  "code": "PGRST204"
}
```

---

## Common Errors and Solutions

### 1. "Column not found in schema cache"
**Error**: `Could not find the 'X' column of 'policies' in the schema cache`

**Causes**:
- Column name mismatch between UI and database
- Column doesn't exist in database
- Trying to insert into wrong column name

**Solutions**:
1. Check actual database column names in Supabase
2. Verify column mappings in Admin Panel → Column Mapping
3. Run appropriate ALTER TABLE command if needed

### 2. Flashing Error Messages
**Issue**: Error messages appear and disappear too quickly to read

**Solution**:
1. Check Debug Logs immediately after the error
2. Filter logs by "ERROR" level
3. The exact error will be captured with full details

### 3. Date Format Errors
**Error**: `The provided format ('%m/%d/%Y') is not valid`

**Solution**: Use `format="MM/DD/YYYY"` for all date inputs (uppercase format)

---

## Database Issues

### Connection Problems
**Symptoms**:
- "Error loading data from Supabase"
- Empty data tables
- Timeout errors

**Solutions**:
1. Check `.env` file for correct credentials:
   ```
   SUPABASE_URL=your_project_url
   SUPABASE_ANON_KEY=your_anon_key
   ```
2. Verify internet connection
3. Check Supabase project status

### Missing Tables
**Error**: `relation "table_name" does not exist`

**Solution**: Run the appropriate SQL script in Supabase:
- `create_deleted_policies_table.sql` for deletion history
- `create_simple_commission_payments.sql` for reconciliation

---

## Reconciliation Problems

### Reconciliation Not Saving
**Symptoms**:
- "Reconcile & Save" button doesn't work
- Transactions not added to policies table
- Errors flash and disappear

**Troubleshooting Steps**:
1. **Check Debug Logs** for specific error messages
2. **Verify Column Names** match between:
   - Manual commission entry form
   - Database columns
   - JSON field names
3. **Common Column Issues**:
   - "Agency Comm Received (STMT)" not "Agency Gross Comm Received"
   - "Agent Paid Amount (STMT)" not "Paid Amount"
   - "NOTES" not "Description"

### Phase 1 Works but Phase 2 Fails
**Issue**: Commission history saves but policies aren't updated

**Check**:
1. Debug logs for Phase 2 errors
2. Column name mismatches
3. Required fields missing data
4. Data type mismatches (numeric vs text)

---

## Performance Issues

### Slow Page Loading
**Causes**:
- Large dataset queries
- Missing database indexes
- Network latency

**Solutions**:
1. Use filtering to reduce data size
2. Enable caching (already implemented for 5 minutes)
3. Add indexes to frequently queried columns

### Checkbox Performance in Edit Policy Transactions (FIXED in v3.6.2-3.6.3)
**Symptoms**:
- 6-7 second delay when clicking checkboxes
- UI freezes while processing checkbox clicks
- Edit button not becoming available immediately after selection

**Previous Cause**: Session state updates triggering full DataFrame refresh
**Solutions**: 
- v3.6.2: Optimized checkbox interactions for attention filter
- v3.6.3: Extended optimization to regular search results with cached selection state

### Session State Errors
**Error**: `st.session_state has no key 'X'`

**Solution**: Initialize session state keys before use:
```python
if 'key_name' not in st.session_state:
    st.session_state.key_name = default_value
```

### UUID Parsing Errors (FIXED in v3.6.2)
**Error**: 500 error when loading certain MGA records (e.g., Wright Flood)

**Previous Cause**: UUID values in database couldn't be parsed
**Solution**: Implemented safe UUID conversion with error handling

### IndexError After Edits (FIXED in v3.6.2)
**Error**: `IndexError: index 0 is out of bounds for axis 0 with size 0`

**Previous Cause**: Row indices changing after edits
**Solution**: Added bounds checking before index access

---

## Quick Fixes Checklist

### Before Reporting an Issue:
- [ ] Check Debug Logs for error details
- [ ] Verify all column names match between UI and database
- [ ] Ensure required fields have data
- [ ] Check date formats are "MM/DD/YYYY"
- [ ] Confirm database connection in .env file
- [ ] Try clearing browser cache and refreshing

### Information to Provide When Reporting:
1. Screenshot of the error (if visible)
2. Debug log entries (filtered by ERROR)
3. Steps to reproduce the issue
4. What page/action caused the error
5. Any recent changes made

---

## SQL Scripts for Common Fixes

### Rename Column
```sql
ALTER TABLE policies 
RENAME COLUMN "old_name" TO "new_name";
```

### Check Column Names
```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'policies'
ORDER BY column_name;
```

### View Recent Errors in Reconciliation
```sql
SELECT * FROM commission_payments_simple 
ORDER BY payment_timestamp DESC 
LIMIT 5;
```

---

*Last Updated: July 4, 2025*