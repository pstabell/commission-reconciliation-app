# Policy Type Mapping Save Error Fix

**Date**: 2025-01-26
**Issue**: Policy Type Mapping fails to save with "Failed to save mapping" error
**Root Cause**: Database table structure mismatch

## Problem Details

When trying to add a policy type mapping (e.g., "AUTOP" → "AUTOP"), the system shows "Failed to save mapping" error.

### Investigation Results

1. **Python Code Expectation** (user_mappings_db.py):
   - Expects a JSONB column called `mappings` 
   - Saves data as: `{'mappings': {'AUTOP': 'AUTOP', ...}}`

2. **Actual Database Structure** (create_user_settings_tables.sql):
   - Has individual columns: `statement_value` and `mapped_type`
   - Cannot accept JSONB data structure

3. **Error Location**:
   - commission_app.py line 12170: `user_mappings.add_policy_mapping(from_type.upper(), to_type)`
   - user_mappings_db.py line 74-85: Tries to upsert JSONB into non-JSONB columns

## Solution

Run the SQL migration script to fix the table structure:

```bash
psql -U your_username -d your_database -f sql_scripts/fix_user_policy_type_mappings_structure.sql
```

Or run in Supabase SQL Editor:
1. Go to Supabase Dashboard → SQL Editor
2. Copy contents of `sql_scripts/fix_user_policy_type_mappings_structure.sql`
3. Execute the script

## What the Fix Does

1. Backs up existing mappings data
2. Drops and recreates both mapping tables with JSONB structure:
   - `user_policy_type_mappings` with `mappings` JSONB column
   - `user_transaction_type_mappings` with `mappings` JSONB column
3. Migrates existing data to new structure
4. Adds default mappings for users without any

## Prevention

- Always ensure database schema matches code expectations
- Test save/load operations after schema changes
- Use migrations to keep database and code in sync

## Verification

After running the fix:
1. Go to Tools → System Tools → Policy Type Mapping
2. Add a new mapping (e.g., "AUTOP" → "AUTOP")
3. Should save successfully without error
4. Refresh page to verify mapping persists