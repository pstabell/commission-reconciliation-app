# Default Template Feature

## Date: 2025-01-27

### Overview
Added the ability to set saved templates as default in Policy Revenue Ledger Reports, which automatically loads when visiting the page. This reduces user errors from forgetting to load their preferred template configuration.

### Features Added

#### 1. Set as Default
- **Star Button**: Each saved template now has a "⭐ Set as Default" button
- **One Default**: Only one template can be default at a time
- **Auto-Load**: Default template loads automatically when visiting the page
- **Persistence**: Default setting saved in JSON file across sessions

#### 2. Visual Indicators
- **Default Badge**: Default template shows ⭐ icon next to its name
- **Info Message**: Shows when default template is auto-loaded
- **Clear Indication**: Easy to see which template is currently default

#### 3. Unset Default
- **Remove Default**: Click "⭐ Unset Default" on current default template
- **Return to Manual**: Removes auto-loading behavior
- **User Control**: Full control over default behavior

### User Workflow

#### Setting a Default Template:
1. Navigate to Policy Revenue Ledger Reports
2. Load or create your preferred template
3. Save it with a descriptive name
4. Click "⭐ Set as Default" next to the template
5. Template now loads automatically on future visits

#### Removing Default Template:
1. Find the template marked with ⭐
2. Click "⭐ Unset Default"
3. No template will auto-load on next visit

### Benefits

1. **Error Prevention**: Reduces "missing column" confusion
2. **Time Saving**: No need to manually load template each visit
3. **Consistency**: Same view configuration every time
4. **Flexibility**: Can change or remove default at any time
5. **User-Friendly**: Clear visual indicators and messages

### Technical Implementation

#### JSON Storage
```json
{
  "template_name": {
    "columns": [...],
    "filters": {...},
    "is_default": true
  }
}
```

#### Auto-Load Logic
- Checks for default template on page load
- Applies template configuration automatically
- Shows info message about loaded template
- Falls back to manual selection if no default

### Files Modified
- `commission_app.py` - Main application file
  - Lines 12132-12148: Added default template loading logic
  - Template save/load functions updated with is_default flag
  - UI elements for setting/unsetting default status

### User Feedback
This feature was requested after user experienced confusion thinking columns were missing when they forgot to load their template. The default template ensures their preferred view is always ready.