# Missing Carriers and MGAs Issue - January 2025

## Problem
Carriers and MGAs disappear from dropdown menus in Add New Policy Transaction and Edit Policy Transactions pages, even after being previously fixed.

## Root Cause
Row Level Security (RLS) is being re-enabled on the commission structure tables (carriers, mgas, carrier_mga_relationships, commission_rules) in the production database. This blocks the application from reading the data.

## Why This Keeps Happening
1. **Supabase Default Behavior**: New tables created in Supabase have RLS enabled by default
2. **Database Migrations**: When tables are recreated or modified, RLS may be re-enabled
3. **Shared Tables**: These tables are meant to be shared across all users (no user_email column), but RLS blocks access

## Quick Fix
Run the following SQL in Supabase SQL Editor:

```sql
-- Disable RLS on all commission tables
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;
ALTER TABLE carrier_mga_relationships DISABLE ROW LEVEL SECURITY;
ALTER TABLE commission_rules DISABLE ROW LEVEL SECURITY;
```

## Complete Diagnostic and Fix
Use the SQL script: `/sql_scripts/fix_missing_carriers_mgas.sql`

This script will:
1. Check if tables exist
2. Show RLS status (likely the problem)
3. Count existing data
4. Disable RLS on all tables
5. Insert basic carriers if tables are empty
6. Verify the fix

## Prevention
1. **After any database migration**, check RLS status on these tables
2. **Document in deployment notes** to always disable RLS on commission tables
3. **Consider adding a startup check** in the app to warn if RLS is enabled

## Technical Background
- The app uses service role key which bypasses RLS
- But in production, the anon key is used which respects RLS
- Since these tables have no RLS policies defined, when RLS is enabled, it blocks ALL access
- The tables need RLS disabled because they contain shared reference data

## Related Issues
- Similar to CSV Import RLS issue (see `/docs/troubleshooting/CSV_IMPORT_RLS_ISSUES_2025.md`)
- Part of the broader RLS vs Custom Auth challenge in the app

## Verification Steps
1. Go to Contacts page - should see carriers and MGAs
2. Go to Add New Policy Transaction - carrier dropdown should populate
3. Edit a transaction - should be able to select carriers

## Long-term Solution
Consider one of:
1. Create proper RLS policies that allow read access to all authenticated users
2. Move to using service role key in production (security implications)
3. Create a public schema for shared reference data
4. Implement caching of carrier/MGA data in the app