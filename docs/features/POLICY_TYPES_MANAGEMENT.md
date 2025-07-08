# Policy Types Management

**Created**: January 7, 2025  
**Purpose**: Document the dynamic policy types management system implementation

## Overview

The Policy Types Management feature provides flexible configuration of policy types throughout the application. Previously hardcoded policy types are now dynamically managed through a JSON configuration file with both Admin Panel management and inline quick-add capabilities.

## Features

### 1. Centralized Configuration
- Policy types stored in `/config_files/policy_types.json`
- Each type has name, active status, and default flag
- Supports custom types via `allow_custom` setting

### 2. Admin Panel Management
- Dedicated tab in Admin Panel: "Manage Policy Types"
- Add new types with validation for duplicates
- Toggle active/inactive status
- Set default policy type
- Reorder types (coming soon)

### 3. Inline Quick Add (Option C)
- "+ Add New Type..." option in dropdowns
- Available in both Add New Policy and Edit Policy forms
- Instantly adds new type without leaving the form
- New types automatically saved to configuration

## Configuration File Structure

```json
{
  "policy_types": [
    {"name": "Auto", "active": true, "default": false},
    {"name": "Home", "active": true, "default": false},
    {"name": "Commercial", "active": true, "default": true},
    {"name": "Life", "active": true, "default": false},
    {"name": "Health", "active": true, "default": false},
    {"name": "Umbrella", "active": true, "default": false},
    {"name": "Flood", "active": true, "default": false},
    {"name": "Other", "active": true, "default": false}
  ],
  "allow_custom": true,
  "last_updated": "2025-01-07"
}
```

## Implementation Details

### Functions Added

1. **`load_policy_types_config()`**
   - Loads configuration from JSON file
   - Creates default config if file doesn't exist
   - Returns dictionary with policy types and settings

2. **`save_policy_types_config(config)`**
   - Saves configuration to JSON file
   - Updates last_updated timestamp
   - Thread-safe implementation

3. **`add_policy_type(name, active=True)`**
   - Adds new policy type if not duplicate
   - Sets active status
   - Returns success boolean

4. **`toggle_policy_type_status(name)`**
   - Toggles active/inactive status
   - Preserves all other settings

5. **`set_default_policy_type(name)`**
   - Sets single default type
   - Clears previous default

6. **`get_active_policy_types()`**
   - Returns list of active type names
   - Used by forms for dropdown options

## Usage Examples

### Admin Panel Management
1. Navigate to Admin Panel
2. Click "Manage Policy Types" tab
3. Use "Add New Policy Type" to add types
4. Toggle checkboxes to activate/deactivate
5. Use radio buttons to set default

### Inline Quick Add
1. In Add/Edit Policy form
2. Click Policy Type dropdown
3. Select "+ Add New Type..."
4. Enter new type name
5. Type is immediately available

### Code Integration
```python
# Load active types for dropdown
policy_types_config = load_policy_types_config()
active_types = [pt['name'] for pt in policy_types_config['policy_types'] if pt['active']]

# Add custom option if allowed
if policy_types_config.get('allow_custom', True):
    active_types.append("+ Add New Type...")

# Create selectbox
selected_type = st.selectbox("Policy Type", options=active_types)
```

## Benefits

1. **Flexibility**: Add/remove policy types without code changes
2. **Consistency**: Single source of truth for all policy types
3. **User Control**: Admins can manage types without developer help
4. **Efficiency**: Quick add option saves time during data entry
5. **Backward Compatible**: Existing policy types preserved

## Security Considerations

- Configuration file has same permissions as application
- No SQL injection risk (JSON file based)
- Type names validated for basic safety
- Admin Panel access required for management

## Future Enhancements

1. **Type Ordering**: Drag-and-drop reordering
2. **Type Categories**: Group related policy types
3. **Type Descriptions**: Add help text for each type
4. **Usage Analytics**: Track most used types
5. **Import/Export**: Bulk type management
6. **Type Mapping**: Map old types to new during imports

## Troubleshooting

### Policy types not showing
- Check `/config_files/policy_types.json` exists
- Verify JSON syntax is valid
- Ensure types are marked as active

### Can't add new types
- Check `allow_custom` is true in config
- Verify write permissions on config directory
- Check for duplicate type names

### Default type not working
- Only one type can be default
- Verify default type is also active
- Check form is reading default correctly

---

*This feature ensures policy types can be managed dynamically without code changes while maintaining data integrity and user convenience.*