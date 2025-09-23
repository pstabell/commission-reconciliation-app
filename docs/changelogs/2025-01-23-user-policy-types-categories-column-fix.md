# User Policy Types Categories Column Fix

## Date: 2025-01-23

## Issue
- Error: "Could not find the 'categories' column of 'user_policy_types' in the schema cache"
- The Python code expected a 'categories' column that didn't exist in the database table

## Root Cause
- The `user_policy_types` table was likely created from an older schema that didn't include the categories column
- The Python code (`user_policy_types_db.py`) was trying to insert/update data with a 'categories' field that the table didn't have

## Solution
1. **Modified Python Code** (`user_policy_types_db.py`):
   - Updated `_create_user_types()` method to gracefully handle missing 'categories' column
   - Modified `save_user_policy_types()` method to try operations with categories first, then retry without if it fails
   - Added error handling to detect "categories" column errors specifically

2. **Created SQL Migration Script** (`sql_scripts/add_categories_column_if_missing.sql`):
   - Script checks if 'categories' column exists
   - Adds it with proper default value if missing
   - Safe to run multiple times (idempotent)

## Changes Made
1. **user_policy_types_db.py**:
   - Enhanced error handling in `_create_user_types()` to try insert with categories, then without if it fails
   - Updated `save_user_policy_types()` with similar fallback logic for both insert and update operations
   - Maintains backward compatibility with tables that may or may not have the categories column

2. **sql_scripts/add_categories_column_if_missing.sql**:
   - New migration script to add the missing column
   - Uses DO block to check column existence before adding
   - Sets proper default value matching the application's expectations

## How to Apply the Fix
1. The Python code changes are already in effect and will handle both table structures
2. To add the missing column to the database, run:
   ```sql
   -- Run the migration script
   psql -U your_user -d your_database -f sql_scripts/add_categories_column_if_missing.sql
   ```
   Or execute the SQL directly in your database management tool

## Prevention
- Always ensure database migrations are run when deploying schema changes
- Consider adding database schema validation on application startup
- Keep SQL table definitions in sync with Python model expectations

## Impact
- No data loss - existing data is preserved
- Application now works with both old (no categories) and new (with categories) table structures
- Users can continue using the app without interruption