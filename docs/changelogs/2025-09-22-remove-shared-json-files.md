# Remove Shared JSON Files - September 22, 2025

## Summary
Removed ALL shared JSON file operations from commission_app.py to ensure complete user data isolation. All user-specific data is now stored in session state or database tables.

## Changes Made

### 1. CSV Column Mappings (saved_mappings.json)
- **Previous**: Stored in `config_files/saved_mappings.json` (shared by all users)
- **Fixed**: Now stored in session state with user email prefix
- **Functions updated**: 
  - `load_saved_column_mappings()` - reads from session state
  - `save_column_mappings_to_file()` - saves to session state only

### 2. Policy Types (policy_types.json)
- **Previous**: Still writing to JSON file despite having database module
- **Fixed**: Removed all JSON write operations, using `user_policy_types` database module only
- **Lines fixed**: 12830-12843, 12996-13010

### 3. Transaction Type Mappings (transaction_type_mappings.json)
- **Previous**: Reading from shared JSON file
- **Fixed**: Using `user_mappings.get_user_transaction_type_mappings()` database function
- **Line fixed**: 4162-4166

### 4. PRL Templates (prl_templates.json)
- **Previous**: Stored in `config_files/prl_templates.json` (shared by all users)
- **Fixed**: Created new database table and module for user-specific storage
- **New files created**:
  - `user_prl_templates_db.py` - Database module for PRL templates
  - `sql_scripts/create_user_prl_templates_table.sql` - Table creation script
- **Functions updated**:
  - Template loading - reads from database
  - Template saving - saves to database
  - Template updating - updates in database
  - Template deletion - deletes from database
- **Note**: Default template functionality temporarily disabled (needs database schema update)

## Database Table Created
```sql
CREATE TABLE user_prl_templates (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    user_email TEXT NOT NULL,
    template_name TEXT NOT NULL,
    columns TEXT[] NOT NULL,
    view_mode TEXT DEFAULT 'all',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, template_name),
    UNIQUE(user_email, template_name)
);
```

## Impact
- No more shared JSON files being written
- Complete user data isolation
- All user preferences and settings are now properly isolated per user
- Prevents any possibility of users seeing each other's data through shared files

## Migration Notes
- The app will still read from old JSON files once for backward compatibility
- After reading, data is stored in the new user-specific location
- Old JSON files in `config_files/` can be archived after all users have migrated