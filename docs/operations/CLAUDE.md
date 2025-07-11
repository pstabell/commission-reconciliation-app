# CLAUDE.md - AI Development Guide & Context

This file contains important context and guidelines for AI assistants (like Claude) working on the Sales Commission App.

**Last Updated**: July 10, 2025 (Late Evening)  
**Current Version**: 3.5.8

## Quick Context
- **Language**: Python with Streamlit
- **Database**: Supabase (PostgreSQL)
- **Architecture**: Single-file app (commission_app.py) - intentionally monolithic
- **Authentication**: Password-based (environment variable)
- **State Management**: Streamlit session state
- **Caching**: In-memory with manual cache clearing

## Recent Major Changes (v3.5.8)
1. **Void Balance Calculation**: Fixed unreconciled transactions not showing after void
2. **Import Parameter Fix (v3.5.7)**: Fixed "all_data not defined" error during import
3. **Customer Name Consistency (v3.5.6)**: Fixed reconciliation import using inconsistent name formats
4. **Prior Fix (v3.5.5)**: Resolved duplicate creation on inline add/edit workflow
5. **Prior Fix (v3.5.4)**: Complete reconciliation void visibility

## Known Issues & Solutions

### 1. Column Names with Spaces
**Issue**: Supabase/PostgreSQL requires quotes for columns with spaces
```python
# Wrong
supabase.table('policies').select('Transaction ID')

# Correct
supabase.table('policies').select('"Transaction ID"')
```

### 2. Timestamp Serialization
**Issue**: pandas Timestamp objects can't be JSON serialized
**Solution**: Use `convert_timestamps_for_json()` function before database operations

### 3. UI-Only Fields
**Issue**: Some fields exist only in UI, not database
**Current UI-only fields**:
- Edit, Select, Action, Details (table checkboxes)
- new_effective_date, new_expiration_date (renewal helpers)
- expiration_date (maps to X-DATE in database)

### 4. Date Format Standardization
**Standard**: MM/DD/YYYY throughout the application
**Function**: `format_dates_mmddyyyy()` handles conversions

### 5. Data Loading & Caching (v3.5.1)
**Issue**: Stale data between page navigation
**Solution**: Each page loads `all_data = load_policies_data()` independently
**Note**: Form data is safe - refresh only occurs on page load, not during form filling

### 6. Pending Renewals Display
**Issue**: `duplicate_for_renewal()` was modifying display data
**Solution**: Use `.copy()` for display, only transform when actually creating renewals
**Impact**: Transaction types now display correctly

### 7. Duplicate Form Names (FIXED in v3.5.3)
**Issue**: StreamlitDuplicateElementKey error preventing all edits
**Cause**: Two implementations of edit form with same name
**Solution**: Removed 657 lines of duplicate code, consolidated to single function
**Prevention**: Track rendered fields to avoid duplicate widget keys

### 8. Void Transactions Not Visible (FIXED in v3.5.4)
**Issue**: Voided reconciliations appeared ACTIVE in history
**Cause**: Filter only looked for `-STMT-` transactions, not `-VOID-`
**Solution**: Updated filter to include both patterns with OR condition
**Note**: Also fixed case-sensitive status comparisons (handles lowercase 'void')

### 9. Duplicate Transactions on Inline Add/Edit (FIXED in v3.5.5)
**Issue**: Editing inline-added transactions created duplicates instead of updating
**Cause**: Modal save logic only checked `_id` field which wasn't in session state
**Solution**: Added database check for existing Transaction ID before INSERT/UPDATE
**Prevention**: Modal now queries database to verify record existence

### 10. Customer Name Format Inconsistency (FIXED in v3.5.6)
**Issue**: Reconciliation created new transactions with statement name format instead of existing
**Cause**: System didn't check for existing customers when creating new transactions
**Solution**: Added customer matching before transaction creation
**Example**: "Ghosh, Susmit" from statement now uses existing "Susmit K. Ghosh"

### 11. Import Function Missing Parameter (FIXED in v3.5.7)
**Issue**: "name 'all_data' is not defined" error when clicking "Proceed with Import"
**Cause**: show_import_results function needed access to all_data but wasn't receiving it
**Solution**: Added all_data parameter to function signature and call
**Impact**: Reconciliation imports now work without errors

### 12. Voided Reconciliations Not Showing as Unreconciled (FIXED in v3.5.8)
**Issue**: Transactions remained reconciled after voiding the batch
**Cause**: calculate_transaction_balances only counted -STMT- entries, not -VOID-
**Solution**: Updated to include -VOID- entries (which have negative amounts)
**Impact**: Voided transactions now properly show as unreconciled and can be re-reconciled

## Development Guidelines

### 1. Before Making Changes
- Always create timestamped backup of commission_app.py
- Check column_mapping_config.py for field name mappings
- Verify field exists in database before operations

### 2. Database Operations
- Use Supabase client, not raw SQL
- Quote column names with spaces
- Handle NaN values (convert to None)
- Clear cache after writes: `clear_policies_cache()`

### 3. Form Development
- Use `edit_transaction_form()` for consistency
- Preserve disabled field values manually
- Apply formula calculations on form load
- Format dates before display

### 4. Testing Renewals
Test with policy that changes numbers:
- Client: Starr Window Tinting LLC
- Original Policy: 1AA338948
- Renewed to: 277B513884
- Type: Commercial surplus lines

### 5. Common Pitfalls
- Don't assume column names match UI labels
- Check for both None and NaN values
- Remember field_counter starts at 0 for column positioning
- Transaction ID must be unique (check before insert)

## File Organization
```
/
├── commission_app.py              # Main application (monolithic by design)
├── column_mapping_config.py       # UI to database field mappings
├── README.md                     # Project overview (ONLY .md file in root)
├── .env                          # Environment variables (not in git)
├── docs/
│   ├── core/                    # Essential documentation
│   │   ├── CHANGELOG.md         # Version history
│   │   ├── PROJECT_HISTORY.md   # Detailed development chronicle
│   │   └── NEXT_STEPS.md       # Current status and roadmap
│   ├── features/               # Feature-specific docs
│   │   └── RENEWAL_DIAGNOSIS.md # Renewal feature analysis
│   └── operations/            # Operational guides
│       ├── CLAUDE.md          # This file - AI context guide
│       └── PUSH_TO_GITHUB.md  # Git workflow guide
├── migration_scripts/         # Database migration scripts
├── plans/                    # Future feature plans
└── help_content/            # User help documentation
```

## Current Focus Areas
1. **Renewal Tracking**: Policy chains with Prior Policy Number
2. **Data Integrity**: Bulletproof renewal process
3. **UI Consistency**: Field ordering and formatting
4. **Performance**: Efficient column reordering

## Helpful Commands
```python
# Clear cache after database changes
clear_policies_cache()

# Generate unique Transaction ID
new_id = generate_transaction_id()

# Format dates for display
df = format_dates_mmddyyyy(df)

# Convert timestamps for JSON
data = convert_timestamps_for_json(data)
```

## Testing Checklist for Changes
- [ ] Create timestamped backup
- [ ] Test with commercial surplus policy renewal
- [ ] Verify all numeric fields show 2 decimals
- [ ] Check date formats (MM/DD/YYYY)
- [ ] Test with policies containing special characters
- [ ] Verify cache clears after saves
- [ ] Check error messages are user-friendly
- [ ] Test reconciliation void visibility
- [ ] Verify case-insensitive status handling
- [ ] Test inline add followed by immediate edit (no duplicates)

## Contact & Support
- **Repository**: https://github.com/pstabell/commission-reconciliation-app
- **Primary Developer**: Patrick Stabell
- **Development Assistant**: Claude (Anthropic)

---

*This file helps AI assistants understand the codebase quickly and avoid common pitfalls.*