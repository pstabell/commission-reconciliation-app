# User Policy Types Schema Fix
**Date**: 2025-01-23  
**Issue**: Users starting with 0 policy types instead of 34 defaults  
**Root Cause**: Database schema mismatch between SQL tables and Python code  

## Problem Details
1. The Python code (`user_policy_types_db.py`) expects a JSONB column storing all policy types as an array
2. The SQL table was created with individual rows per policy type (normalized structure)
3. This mismatch caused the Python code to fail when trying to read/write policy types
4. New users would start with 0 policy types instead of the 34 defaults defined in the code

## Schema Mismatch
### Old (Incorrect) Schema:
```sql
CREATE TABLE user_policy_types (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    user_email TEXT NOT NULL,
    policy_type TEXT NOT NULL,  -- Individual rows per type
    display_order INTEGER,
    is_active BOOLEAN
);
```

### New (Correct) Schema:
```sql
CREATE TABLE user_policy_types (
    id UUID PRIMARY KEY,
    user_id UUID,
    user_email TEXT NOT NULL,
    policy_types JSONB NOT NULL DEFAULT '[]'::jsonb,  -- All types in one JSONB array
    default_type TEXT DEFAULT 'HO3',
    categories JSONB,
    version TEXT DEFAULT '1.0.0'
);
```

## Fix Applied
1. Created `sql_scripts/fix_user_policy_types_table.sql` to:
   - Backup existing data
   - Drop old table
   - Create new table with correct JSONB schema
   - Initialize all users with 34 default policy types

2. Updated `sql_scripts/create_user_settings_tables.sql` to use correct schema for future installations

3. Updated `sql_scripts/migrate_settings_to_user_specific.sql` to properly initialize default types

## Default Policy Types (34 total)
The system now properly initializes users with these default types:
- AUTOP, HOME, DFIRE, WC, AUTOB, GL, FLOOD, BOAT, CONDO, PROP-C
- PACKAGE-P, UMB-P, IM-C, GARAGE, UMB-C, OCEAN MARINE, WIND-P, PL
- COLLECTOR, PACKAGE-C, FLOOD-C, BOP, BPP, EXCESS, CYBER, D&O
- CYCLE, AUTO, RV, RENTERS, UMBRELLA (as UMBRELLA-C), MOBILE, WIND, UMBRELLA-P

## To Apply Fix
Run this SQL script in the database:
```bash
psql -d your_database -f sql_scripts/fix_user_policy_types_table.sql
```

## Prevention
- Always ensure database schema matches the expectations of the application code
- Test with new users to verify they get all default configurations
- Consider adding schema validation in the Python code to detect mismatches early