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

## Row Level Security (RLS) Issues

### CSV Import Fails with "row violates row-level security policy"
**Symptoms**:
- Error: "new row violates row-level security policy for table 'policies'"
- All rows fail to import with the same error
- User email shows correctly in debug output

**Cause**:
Row Level Security (RLS) is enabled on the policies table and the authenticated user's email doesn't match the data being inserted.

**Solution**:
1. **Check RLS status** - Run this SQL in Supabase:
```sql
-- Check if RLS is enabled on policies table
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE tablename = 'policies' AND schemaname = 'public';

-- Check existing RLS policies
SELECT * FROM pg_policies 
WHERE tablename = 'policies' AND schemaname = 'public';
```

2. **For Demo Users** - Create a policy allowing demo access:
```sql
CREATE POLICY "demo_user_policy" ON policies
FOR ALL
TO authenticated
USING (user_email = 'Demo@AgentCommissionTracker.com' OR user_email = auth.email())
WITH CHECK (user_email = 'Demo@AgentCommissionTracker.com' OR user_email = auth.email());
```

3. **Alternative** - Temporarily disable RLS (use with caution):
```sql
ALTER TABLE policies DISABLE ROW LEVEL SECURITY;
```

### Carriers, MGAs, and Commission Rules Not Visible
**Symptoms**:
- Dropdown lists for Carriers and MGAs appear empty
- Commission rules don't load or apply
- Error messages about missing carriers/MGAs when saving
- Debug logs show "0 carriers found" or "0 MGAs found"

**Cause**: 
Row Level Security (RLS) is enabled on these tables but no policies are configured, effectively blocking all access.

**Solution**:
1. **Immediate Fix** - Disable RLS on affected tables:
```sql
-- Disable RLS on all affected tables
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;
ALTER TABLE commission_rules DISABLE ROW LEVEL SECURITY;

-- Verify RLS is disabled
SELECT 
    tablename,
    rowsecurity as rls_enabled,
    CASE 
        WHEN rowsecurity THEN '🔒 RLS ENABLED - Data blocked'
        ELSE '🔓 RLS DISABLED - Data accessible'
    END as status
FROM pg_tables 
WHERE tablename IN ('carriers', 'mgas', 'commission_rules')
    AND schemaname = 'public';
```

2. **Verify Data Access**:
```sql
-- Check that data is now accessible
SELECT COUNT(*) as carrier_count FROM carriers;
SELECT COUNT(*) as mga_count FROM mgas;
SELECT COUNT(*) as rule_count FROM commission_rules;
```

3. **Long-term Solution**: 
   - Create proper RLS policies for multi-tenant access when needed
   - For single-tenant apps, keep RLS disabled on these reference tables
   - Document which tables should have RLS enabled vs disabled

### Testing for RLS Issues
**Quick diagnostic query**:
```sql
-- Check all tables with RLS status
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled,
    hasindexes
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY rowsecurity DESC, tablename;
```

**Common tables that may need RLS disabled**:
- `carriers` - Insurance carrier reference data
- `mgas` - Managing General Agent reference data  
- `commission_rules` - Commission rate configurations
- `policy_types` - Policy type definitions
- Any other shared reference/lookup tables

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

*Last Updated: January 13, 2025*

---

## CRITICAL SECURITY ISSUES

### Cache Poisoning - Users Seeing Other Users' Data
**Date Discovered**: January 13, 2025
**Severity**: CRITICAL

**Symptoms**:
- User A logs in and sees their data
- User B logs in and sees User A's data
- Clearing cache temporarily fixes but problem returns
- Data randomly appears/disappears between users

**Root Cause**:
Streamlit's `@st.cache_data` caches globally across ALL users, not per user.

**Solution**:
```python
# REMOVE ALL CACHING from sensitive data functions
def load_policies_data():
    # NO @st.cache_data decorator!
    # Always fetch fresh data
```

**See full details**: [CSV Import and RLS Issues Guide](../troubleshooting/CSV_IMPORT_RLS_ISSUES_2025.md)