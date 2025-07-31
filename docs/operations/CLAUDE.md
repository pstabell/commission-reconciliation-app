# CLAUDE.md - AI Development Guide & Context

This file contains important context and guidelines for AI assistants (like Claude) working on the Sales Commission App.

**Last Updated**: July 31, 2025  
**Current Version**: 3.9.18

## Quick Context
- **Language**: Python with Streamlit
- **Database**: Supabase (PostgreSQL)
- **Architecture**: Single-file app (commission_app.py) - intentionally monolithic
- **Authentication**: Password-based (environment variable)
- **State Management**: Streamlit session state
- **Caching**: In-memory with manual cache clearing

## Recent Major Changes (v3.9.18)
1. **STMT Transaction Client ID Inclusion Fix**:
   - Fixed missing STMT transactions in Policy Revenue Ledger
   - STMT transactions often have missing or different Client IDs
   - Now retrieves transactions by Client ID + Policy Number
   - ALSO includes any STMT transactions matching Policy Number regardless of Client ID
   - Ensures all reconciliation entries appear under correct policy
   - Prevents orphaned STMT transactions due to Client ID mismatches

## Prior Major Changes (v3.9.17)
1. **Simplified Checkbox Interface in Policy Revenue Ledger Reports**:
   - Replaced two checkbox columns (Hide, Reviewed) with single "Select" column
   - Actions determined by buttons: "Hide Selected" and "Mark as Reviewed"
   - Added "View Reviewed" button to access reviewed transactions
   - Cleaner interface with less horizontal scrolling
   - Follows common UI pattern of select-then-act

## Prior Major Changes (v3.9.16)
1. **Policy Number Whitespace Fix**:
   - Fixed duplicate policy entries caused by leading/trailing spaces in policy numbers
   - STMT transaction had ' 1AA338948' (with space) vs original '1AA338948'
   - Now trims all policy numbers before comparison and grouping
   - Applied trimming in both dropdown population and transaction retrieval
   - Resolves issue where same policy appeared twice in Policy Revenue Ledger

## Prior Major Changes (v3.9.15)
1. **Policy Revenue Ledger Grouping Fix**:
   - Fixed duplicate policy entries in dropdown when customer names have slight variations
   - Now groups by Client ID + Policy Number instead of relying on exact customer name matches
   - When retrieving policy transactions, uses Client ID + Policy Number to get ALL related transactions
   - Prevents splitting of policies due to punctuation differences (commas, periods, etc.)
   - Ensures STMT transactions show under the correct policy even with name mismatches

## Prior Major Changes (v3.9.14)
1. **Client ID in Reconciliation Edit Form**:
   - Added Client ID as editable field in reconciliation edit form
   - Allows fixing missing Client IDs on STMT transactions directly from reconciliation page
   - Helps properly link transactions for Policy Revenue Ledger grouping
   - Shows "was: [original value]" format like other editable fields
   - Includes help text: "Enter the Client ID to properly link this transaction"

## Prior Major Changes (v3.9.13)
1. **MGA Contact Info Fix**:
   - Fixed "Could not find the 'contact_name' column of 'mgas'" error
   - MGAs use JSONB contact_info column, not individual contact fields
   - Updated MGA edit form to properly save contact data to contact_info JSONB
   - Updated MGA display to read from contact_info.contact_name, etc.
   - Add MGA form already correctly used JSONB format

## Prior Major Changes (v3.9.12)
1. **Policy Term Custom Default**:
   - Policy Term now defaults to "Custom" instead of auto-calculating 12 months
   - X-DATE updates immediately when Policy Term is selected (no Calculate button needed)
   - Removed automatic 12-month term calculation for NEW/RWL transactions
   - Users must explicitly choose term length for better data accuracy
   - Shows success message when X-DATE is automatically calculated
   - Fixed session state modification error by removing form callbacks (not allowed in Streamlit forms)
   - X-DATE calculation now shows info message when Policy Term is selected
   - Added help text explaining bidirectional relationship: Policy Term → X-DATE (immediate) and X-DATE → Policy Term (on Calculate)
   - Fixed critical issue: X-DATE no longer changes automatically when editing existing transactions
   - X-DATE only updates when user explicitly changes Policy Term value

## Prior Major Changes (v3.9.11)
1. **Edit Transactions Column Order Fix**:
   - Fixed persistent column ordering in Edit Policy Transactions table
   - Column order now maintained throughout editing sessions
   - Auto-save preserves correct column order
   - Session state properly stores and restores column order
   - Fixed UnboundLocalError with proper variable scoping

## Prior Major Changes (v3.9.10)
1. **Transaction Type Symbols & Reviewed Transactions**:
   - Added Type → column with transaction symbols in Policy Revenue Ledger Reports
   - Symbols: 💰=STMT, 🔴=VOID, ✏️=END, ❌=CAN, 📄=Other
   - Reviewed transactions now filter out of main display (like hidden transactions)
   - Reviewed transactions accessible via "View Reviewed" button
   - Fixed initialization error for prl_reviewed_rows session state
   - Removed column order info message to reduce clutter
   - Updated Policy Revenue Ledger page to include END and CAN symbols

## Prior Major Changes (v3.9.5)
1. **Void Improvements**:
   - Added double-void prevention validation
   - System checks if VOID-{batch_id} already exists before allowing void
   - Shows error: "This batch has already been voided. You cannot void a batch twice."
   - Void reason field now has yellow styling (#fff3b0 background, #e6a800 border)
   - Matches app-wide input field styling for consistency

## Prior Major Changes (v3.9.4)
1. **Reconciliation Matching Logic Fixes**:
   - Fixed false matches where different policy numbers (TESTPOLICY123 vs TESTPOLICY001) were matched based on customer name alone
   - Now requires policy number match for automatic matching (95% confidence)
   - Customer-only matches require manual confirmation
   - "exact" label now only for 99%+ confidence matches
   - Added confidence tiers: exact, high, good, moderate, low
   - Added NaN cleaning to prevent database errors
   - Added "Skip" option for low confidence matches

## Prior Major Changes (v3.9.3)
1. **Duplicate Transaction Feature**:
   - New "📋 Duplicate Selected Transaction" button on Edit Policy Transactions page
   - Copies all transaction data except unique IDs and tracking fields
   - Opens form in "Create Duplicate" mode for easy modification
   - Perfect for creating cancellations, endorsements, or similar policies
2. **Agent Comm % Override for Cancellations**:
   - Agent Comm % field becomes editable for CAN transactions after Calculate
   - Allows manual adjustment for special cases (e.g., 50% chargeback on NEW cancellations)
   - Shows "🔓 UNLOCKED" indicator when field is editable
3. **Add New Transaction Customer Name Fix**:
   - "Add New Transaction for This Client" now properly copies Customer name
   - Previously only copied Transaction ID and Client ID

## Prior Major Changes (v3.9.2)
1. **Policy Term Enhancements**:
   - Added "Custom" option to Policy Term dropdown
   - Fixed override issue where changes were forced back to 12 months
   - Implemented pending state pattern for X-DATE updates
   - Changed database schema from INTEGER to TEXT for Policy Term

## Prior Major Changes (v3.8.2)
1. **Table Width Fix in Edit Policy Transactions**:
   - Fixed table not using full screen width
   - Moved st.data_editor outside column context to page level
   - Fixed 650+ lines of indentation issues from restructuring
   - All features preserved and working correctly
2. **Prior Changes (v3.8.1)
1. **Enhanced Policy Term & Origination Features**:
   - NEW/RWL transactions (except AUTO) auto-populate 12-month term and X-DATE
   - END transactions properly trace back to NEW for origination date
   - Fixed policy number lookup to use user's current input
   - Session state handling improved for Policy Term dropdown
   - Visual feedback shows auto-calculated values before saving
2. **Prior Changes (v3.8.0)**: Initial Policy Origination Date auto-population and batch tool
3. **Prior Changes (v3.7.6)**: Fixed policy type consistency across forms
2. **Delete Logic Fix**: Fixed "Could not identify transaction IDs" error when selecting import transactions
   - Error now only shows when truly can't find Transaction ID column
   - Properly handles import and reconciliation transaction warnings
3. **Variable Scope Fix**: Fixed UnboundLocalError in edit transaction form
   - `current_transaction_type` now properly scoped for both columns
   - Available for chargeback calculations and help text
4. **Accounting Page Removal**: Safely removed redundant Accounting page
   - All functionality already exists in Reconciliation page
   - No dependencies or broken links
   - Cleaner navigation menu

## Prior Release (v3.7.5)
1. **Fixed Cancellation Commission Calculations**: CAN/XCL now calculate chargebacks
   - Fixed CAN and XCL transactions showing $0 instead of negative commissions
   - Properly calculates negative amounts for both Agency and Agent commissions
   - Uses Prior Policy Number to determine chargeback rate (25% or 50%)
   - Added clear "(CHARGEBACK)" labels in help text
2. **Fixed Edit Transaction Update Error**: Resolved "no data returned" issue
   - Added `.select()` to Supabase update operation
   - Supabase doesn't return data after UPDATE by default
   - Now properly confirms successful updates
   - Fixed inline-added transaction edit workflow
2. **Removed All Date Format Overrides**: Let Streamlit handle dates naturally
   - Removed format_dates_mmddyyyy() function entirely
   - Removed all format="MM/DD/YYYY" from date_input widgets
   - Updated convert_timestamps_for_json to use ISO format
   - Removed date formatter tool from Tools page
   - Dates now display in ISO format (YYYY-MM-DD) consistently
   - Resolves ongoing date reversal issues
   - Simplifies codebase significantly
2. **Prior Release (v3.7.4)
1. **Contacts Page Forms Above the Fold**: Improved UX by moving Add Carrier/MGA forms
   - Add Carrier form now appears immediately after Quick Add dropdown
   - Implemented missing Add MGA form functionality  
   - Both forms appear above the fold without scrolling
   - Users can now see forms are working without confusion
   - Added complete MGA fields: name, contact, phone, email, website, notes
2. **Prior Release (v3.7.3)
1. **Policy Type Rename Feature**: Added ability to rename policy types
   - New section in Admin Panel → Policy Types tab
   - Text input for new name (can rename to any name not already in use)
   - Perfect for standardizing names (e.g., "Auto" → "AUTO", "HO3" → "HOME")
   - Shows transaction count before renaming
   - Updates all affected transactions automatically
   - Also updates policy type mappings if needed
2. **Prior Release (v3.7.2)
1. **Policy Type Merge Feature**: Added ability to merge duplicate policy types
   - New section in Admin Panel → Policy Types tab
   - Select source and target policy types for merging
   - Shows transaction counts before merging
   - Updates all affected transactions automatically
   - Also updates policy type mappings if needed
   - Includes clear warnings about irreversible action
2. **Prior Release (v3.7.1)
1. **Policy Type Mapping Validation**: Added import validation for unmapped policy types
   - Reconciliation import now validates all policy types before processing
   - Shows error with list of unmapped types if found
   - Prevents import until mappings are configured in Admin Panel
   - Ensures data consistency by requiring all types to be mapped
   - User-friendly error messages with clear next steps
2. **Prior Release (v3.7.0)
1. **Enhanced Pending Renewals & Premium Calculator**: Major improvements to renewal tracking and endorsement handling
   - Added Premium Sold Calculator for Endorsements to Edit Transaction form
   - Shows ALL past-due renewals (removed -30 day limit)
   - Added time range filtering (All, Past Due, This Week, 30/60/90 days)
   - Visual status indicators: 🔴 Past Due, 🟡 Urgent, ✅ OK
   - Summary metrics for quick overview
   - Past-due renewals sorted first for immediate attention
   - Added carrier/MGA commission rate loading to Edit Renewal Transaction form
   - Green tip reminder to select carrier from dropdown for automatic rate loading
   - Policy Revenue Ledger now has "All Dates" option to bypass date filtering
2. **Prior Release (v3.6.5) - Void Date Extraction Fix**: Fixed void transactions using current date instead of statement date
   - Issue: Void transactions created with current date, making them invisible in historical views
   - Cause: Code only handled IMPORT- prefix, not REC- or MNL- prefixes
   - Solution: Enhanced regex pattern to extract YYYYMMDD from any batch ID format
   - Now supports: IMPORT-YYYYMMDD-X, REC-YYYYMMDD-X, MNL-YYYYMMDD-X
   - Void transactions now appear in correct time period with proper dates
   - Fixed Transaction ID suffix and STMT DATE to use statement date
2. **Prior Release (v3.6.4) - Search & Filter Fix**: Fixed column name references
   - Updated all column references from underscore to space-separated names
   - Fixed KeyError preventing filter functionality
   - Search & Filter page now fully functional
3. **Prior Release (v3.6.3) - Import Transaction Protection**: Protected import-created transactions
   - Added -IMPORT suffix to transaction IDs
   - Implemented partial edit restrictions and delete protection
   - Migrated 45 existing transactions to new format
   - Extended checkbox performance optimization to regular search results
3. **Prior Release (v3.6.2) - Performance & Bug Fixes**: Major performance improvements and critical error fixes
   - Fixed Wright Flood MGA loading error (UUID parsing issue) - MGA data now loads correctly
   - Optimized checkbox performance in Edit Policy Transactions (6-7 second delay eliminated)
   - Fixed IndexError when selecting transactions after edits
   - Repositioned Client ID debug caption for better UI flow
2. **Prior Release (v3.6.1) - Client ID Generation**: Generate missing Client IDs
   - "Generate Client ID" button appears when Client ID field is empty
   - Generates unique CL-XXXXXXXX format ID
   - Updates database immediately without requiring form save
   - Available in both Edit Policy Transactions page and modal forms
3. **Prior Release (v3.6.0) - Contacts & Commission Structure**: Complete carrier and MGA management system
   - Dedicated Contacts page with Carriers and MGAs tabs
   - Commission rules engine with carrier/MGA/policy type specific rates
   - Support for NEW and RWL (renewal) commission rates
   - Payment terms tracking (Advanced vs As Earned)
   - Rule priority system for complex scenarios
   - Initial data import: 22 carriers and 11 MGAs from Excel
3. **Island Architecture**: Contacts page fully isolated following app architecture principles
   - Complete error containment within module
   - Independent data loading per page
   - No cross-page dependencies
   - Prepared for future modular architecture
4. **Modern Policy Types UI**: Redesigned Admin Panel with compact grid layout
   - Visual category grouping (Personal, Commercial, Specialty)
   - Configuration file-based management for safety
   - Download configuration option for backup
   - Clear documentation for adding new types
4. **Database Schema Expansion**: Added 4 new tables for commission structure
   - carriers: Carrier information with NAIC codes
   - mgas: MGA details and contact information
   - carrier_mga_relationships: Links carriers to MGAs
   - commission_rules: Complex rule definitions with priority
   - Optional carrier_id and mga_id added to policies table

## Prior Changes (v3.5.15)
1. **Client ID Matching**: New transactions from reconciliation now properly link to Client IDs
2. **Enhanced Reconciliation UI**: Clear force match warnings, improved create transaction labels
3. **Transactions Requiring Attention**: New filter on Edit Policies page for incomplete data
4. **Agency Comm Optional**: Moved to optional fields, allowing reconciliation without it
5. **Smart Warning Logic**: Only shows warnings for genuine customer name mismatches

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
- Rate (commission rate from statement - display only)
- Days Until Expiration (calculated field)
- Status (UI display field for renewals)
- _id (internal row identifier)
**Solution**: Use `clean_data_for_database()` function before any insert operations

### 4. Date Format Standardization (REMOVED in v3.7.5)
**Standard**: ISO format (YYYY-MM-DD) - Streamlit's natural handling
**Note**: All date formatting overrides have been removed to let Streamlit handle dates naturally

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

### 13. Manual Match Customer Name Mismatches (FIXED in v3.5.9)
**Issue**: Cannot reconcile when customer names don't match exactly (e.g., "Last, First" vs "First Last")
**Cause**: Auto-match requires exact name matches, no manual override option
**Solution**: Added "Match transaction" checkbox for manual customer selection
**Impact**: Users can now match transactions despite name format differences

### 14. Manual Match KeyErrors (FIXED in v3.5.10)
**Issue**: KeyError 'balance' and 'Policy Number' when processing manual matches
**Cause**: Manual matches don't have all fields that automatic matches have
**Solution**: Added .get() with fallbacks for missing fields
**Impact**: Manual matching now works without errors

### 15. Missing Statement Fields (FIXED in v3.5.11)
**Issue**: KeyError 'effective_date' when statement data incomplete
**Cause**: Direct dictionary access without checking field existence
**Solution**: Use .get() with empty string defaults for all statement fields
**Impact**: Reconciliation handles incomplete statements gracefully

### 16. Void Screen Shows Agency Amounts Instead of Agent (FIXED in v3.5.12)
**Issue**: Adjustments & Voids tab showed different amounts than Reconciliation History
**Cause**: Hardcoded to use 'Agency Comm Received (STMT)' instead of 'Agent Paid Amount (STMT)'
**Solution**: Changed all void screen references to use Agent amounts
**Impact**: Void screen now shows consistent amounts with reconciliation, preventing confusion

### 17. Transactions Not Showing in Matching Dropdown (ENHANCED in v3.5.13)
**Issue**: Users report transactions with balance not appearing in reconciliation matching
**Common Causes**:
- Customer name variations (e.g., "Adam Gomes" vs "Gomes, Adam")
- Transaction has zero commission amount
- Transaction already fully reconciled
**Solution**: Added debug mode showing all customer transactions with balance calculations
**Enhanced**: Improved fuzzy customer matching with word-based algorithms
**Impact**: Users can now troubleshoot missing transactions and system handles name variations better

### 18. Column Mapping Load Not Working (FIXED in v3.5.14)
**Issue**: Saved column mappings appeared to load but dropdowns didn't update
**Cause**: Streamlit doesn't allow modifying widget state after creation
**Solution**: Use column_mapping to set selectbox index parameter on creation
**Impact**: Saved mappings now properly populate all dropdown selections

### 19. Cross-Reference Key Database Error (FIXED in v3.5.14)
**Issue**: PGRST204 error - "Could not find the 'Cross-Reference Key' column"
**Cause**: Code tried to insert field that doesn't exist in database
**Solution**: Removed Cross-Reference Key, tracking info preserved in NOTES field
**Impact**: Reconciliation imports work without database schema changes

### 20. Rate Field Database Error (FIXED in v3.5.14)
**Issue**: PGRST204 error - "Could not find the 'Rate' column of 'policies'"
**Cause**: UI-only field (Rate) was being included in database insert operations
**Solution**: Created `clean_data_for_database()` function to remove all UI-only fields before insertion
**Impact**: Import process now works without database errors, Rate still displays in UI

### 21. Missing Statement Fields KeyError (FIXED in v3.5.14)
**Issue**: KeyError 'effective_date' when processing statement data
**Cause**: Direct dictionary access without checking if fields exist
**Solution**: Updated all dictionary access to use `.get()` with safe defaults
**Impact**: Handles incomplete or missing statement data without crashing

### 22. Missing Client IDs on New Transactions (FIXED in v3.5.15)
**Issue**: New transactions created during reconciliation had no Client ID
**Cause**: System wasn't looking up or creating client records during import
**Solution**: Added client matching UI with radio buttons for existing/new clients
**Impact**: All new transactions now properly linked to Client IDs

### 23. Transactions with Missing Data (ADDRESSED in v3.5.15)
**Issue**: Transactions with payments but no premium/commission data cause incorrect reports
**Cause**: Created during reconciliation without complete information
**Solution**: Added "Show Transactions Requiring Attention" filter on Edit Policies page
**Impact**: Easy identification and completion of incomplete transaction data

### 24. Import-Created Transactions Not Protected (FIXED in v3.6.3)
**Issue**: Transactions created during import could be deleted, breaking reconciliation
**Cause**: No special identification or protection for import-created transactions
**Solution**: 
- Added -IMPORT suffix to transaction IDs (e.g., D5D19K7-IMPORT)
- Implemented partial edit restrictions (payment fields read-only)
- Added delete protection with clear error messages
- Created comprehensive explanation box in edit form
**Migration**: Updated database validation function and migrated 45 existing transactions
**Impact**: Import transactions now protected while allowing commission data completion

### 25. Search & Filter Column Name Errors (FIXED in v3.6.4)
**Issue**: KeyError: 'Transaction_ID' when using Search & Filter page
**Cause**: Code used underscore-separated column names but database has space-separated
**Solution**: Updated all column references to use correct names:
- `Transaction_ID` → `Transaction ID`
- `Policy_Number` → `Policy Number`
- `Client_ID` → `Client ID`
- `Policy_Type` → `Policy Type`
- `Transaction_Type` → `Transaction Type`
- `Effective_Date` → `Effective Date`
- `Commission_Paid` → `Agent Paid Amount (STMT)`
- `Balance_Due` → `Policy Balance Due`
**Impact**: Search & Filter functionality now works correctly

### 26. Void Transactions Using Current Date (FIXED in v3.6.5)
**Issue**: Void transactions created with current date instead of statement date
**Cause**: Date extraction only handled IMPORT- prefix, not REC- or MNL- formats
**Example**: Voiding REC-20240831-XXX created transactions with 20250715 dates
**Solution**: 
- Enhanced date extraction using regex pattern `-(\d{8})-` 
- Extracts YYYYMMDD from any batch ID format
- Sets both Transaction ID suffix and STMT DATE to statement date
**Impact**: Void transactions now appear in correct historical period

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

# Clean data before database insertion
clean_data = clean_data_for_database(data)
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