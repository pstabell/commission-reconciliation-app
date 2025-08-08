# CLAUDE.md - AI Development Guide & Context

This file contains important context and guidelines for AI assistants (like Claude) working on the Sales Commission App.

**Last Updated**: August 8, 2025  
**Current Version**: 3.9.36

## Quick Context
- **Language**: Python with Streamlit
- **Database**: Supabase (PostgreSQL)
- **Architecture**: Single-file app (commission_app.py) - intentionally monolithic
- **Authentication**: Password-based (environment variable)
- **State Management**: Streamlit session state
- **Caching**: In-memory with manual cache clearing (5-minute TTL)

## Recent Major Changes (v3.9.36)
1. **Proactive Agent Deployment Directive**:
   - **Added Critical Guideline**: Always use Task agents for search and analysis operations
   - **Automatic Deployment**: Agents should be deployed proactively for code searches
   - **Benefits**: High-speed parallel searching with pin-point accuracy
   - **Use Cases**: Finding implementations, tracking dependencies, analyzing patterns
   - **Documentation**: Added as top priority (#0) in Development Guidelines

## Recent Major Changes (v3.9.35)
1. **MGA Dropdown Fixed for Commission Rules**:
   - **Issue**: MGAs with commission rules weren't showing in transaction edit dropdown
   - **Root Cause**: Dropdown only checked carrier_mga_relationships table, not commission rules
   - **Fix**: Modified `load_mgas_for_carrier()` to include MGAs from BOTH sources:
     - carrier_mga_relationships table (existing functionality)
     - commission_rules table (new functionality)
   - **Cache Management**: Added automatic cache clearing when commission rules are created/updated
   - **Impact**: CRC Group and other MGAs now appear in dropdown when linked via commission rules

## Recent Major Changes (v3.9.34)
1. **Reconciliation Import Improvements**:
   - **Financial Fields Exclusion**: Premium Sold, Policy Taxes & Fees, Commissionable Premium, Policy Gross Comm %, Broker Fee, and Broker Fee Agent Comm no longer imported unless explicitly mapped
   - **UI Layout Fix**: Statement Details moved to top of left column, customer matching below
   - **"Use" Button Positioning**: Moved to far left, immediately next to customer names for clear association
   - **Duplicate Prevention**: Added deduplication for unmatched transactions to prevent duplicates like "Stephen Randall" appearing twice
   - **Widget Key Fixes**: Fixed duplicate key errors in "Show all at once" mode by adding unique suffixes
   - **Import Integrity Issue**: Identified orphaned batch records in reconciliation history from aborted imports

## Recent Major Changes (v3.9.33)
1. **Transaction Type Mapping Implementation**:
   - **Admin Panel - New Tab**: Transaction Type Mapping interface
     - Maps statement types (e.g., STL) to standardized types (e.g., PMT)
     - Default mapping: STL → PMT for as-earned commission payments
     - Configuration stored in `config_files/transaction_type_mappings.json`
   - **Reconciliation Import Enhancement**:
     - Validates all transaction types have mappings before import
     - Automatically applies mappings during transaction creation
     - Shows visual feedback when mappings are applied
     - Added PMT to valid transaction types list

## Recent Major Changes (v3.9.32)
1. **Fixed Policy Term-Based Transaction Filtering**:
   - **Policy Revenue Ledger**: Fixed STMT transactions not appearing in terms
     - Changed STMT filtering from STMT DATE to Effective Date
     - Reordered logic to check "-STMT-" pattern before transaction types
     - Fixed issue where STMT with Type="END" were filtered as regular END transactions
   - **Policy Revenue Ledger Reports**: Completely rewrote filtering logic
     - Changed from date-based to term-based filtering
     - Now finds policies starting in selected month, shows ALL their transactions
     - Matches original design intent for complete policy lifecycle view

## Recent Major Changes (v3.9.31)
1. **Fixed Tab Jumping in Reconciliation Page**:
   - Date filters in Reconciliation History now use form with "Apply Filter" button
   - Prevents automatic page rerun when selecting dates
   - Tab no longer jumps back to "Import Statement" 
   - Selected dates preserved in session state for persistence

## Recent Major Changes (v3.9.30)
1. **Enhanced Contact Management UX**:
   - Add Carrier/MGA forms disappear after successful submission
   - Success message displayed prominently
   - Automatically navigates to newly created contact detail view
   - Improved workflow for immediate commission rule creation

2. **Fixed Transient Database Connection Errors**:
   - "Resource temporarily unavailable" errors now handled gracefully
   - Commission rule lookups cached to prevent rate changes on errors
   - MGA loading cached to reduce database calls
   - Error messages only logged to console, not shown to users

## Recent Major Changes (v3.9.29)
1. **Commission Rules with Policy Type Selection**:
   - Multi-select dropdown for policy types in commission rules
   - "All Policy Types" option for catch-all rules
   - Automatic rate selection based on carrier + MGA + policy type
   - Priority fallback: most specific to general rules
   - Policy type selection moved outside form in Add New Transaction

## Prior Major Changes (v3.9.21)
1. **View-Specific Columns in Policy Revenue Ledger Reports**:
   - Different default columns for "Aggregated by Policy" vs "Detailed Transactions" views
   - Aggregated view shows policy-level columns (Client ID, Carrier Name, MGA Name, Policy Origination Date, etc.)
   - Detailed view shows transaction-level columns (Transaction Type, focused on individual entries)
   - Column selection automatically resets when switching view modes
   - Hidden and Reviewed tables now use same columns as Report Preview (not hardcoded)
   - Table titles change based on view mode: "Hidden/Reviewed Policies" vs "Hidden/Reviewed Transactions"
   - Added extra row padding to Hidden/Reviewed tables for better visibility
   - Default sorting by Customer name then Policy Number in both views (all tables)
   - Expanded Detailed Transactions columns to include MGA Name, X-DATE, Policy Taxes & Fees, Commissionable Premium, Broker Fee, and Broker Fee Agent Comm

## Prior Major Changes (v3.9.20)
1. **Total Agent Comm Fixes**:
   - Policy Revenue Ledger now uses "Total Agent Comm" for Credit column (includes broker fees)
   - Policy Revenue Ledger Reports balance calculation uses "Total Agent Comm"
   - Column display automatically substitutes when "Agent Estimated Comm $" is selected
   - Default columns and presets updated to use "Total Agent Comm"
2. **Refresh Data Buttons**:
   - Added refresh buttons to Policy Revenue Ledger and Reports pages
   - Clears cache for real-time database updates
   - Helps sync data between local and live app instances

## Prior Major Changes (v3.9.19)
1. **Reconciliation Client ID Fixes**:
   - Fixed missing Client IDs in CSV/Excel reconciliation imports
   - STMT transactions now properly inherit Client ID from matched transactions
   - Added explicit Client ID preservation in reconciliation entry creation
   - Added Client ID column to Reconciliation History display
   - Removed debug messages for cleaner interface

## Prior Major Changes (v3.9.18)
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

## Streamlit Framework Limitations

### Tab Component Limitations
- **Cannot programmatically select tabs** - Always resets to first tab on rerun
- **Cannot dynamically reorder tab content** - Tab order is fixed at creation
- **Workarounds:**
  - Minimize reruns (use forms, avoid callbacks)
  - Keep frequently-used functionality on first tab
  - Use success messages instead of immediate refresh
  - Open in multiple browser tabs for different workflows

### Form Limitations
- **Cannot modify form fields based on other form fields** - All form state is isolated
- **Cannot have nested forms**
- **Workarounds:**
  - Use session state for complex interactions
  - Break complex forms into steps
  - Use regular widgets outside forms when real-time updates needed

### State Management
- **Page reruns reset all widget states unless explicitly stored**
- **Session state persists but can cause stale data issues**
- **Workarounds:**
  - Be selective about what goes in session state
  - Clear relevant session state when context changes
  - Use unique keys for widgets to prevent conflicts

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

### 27. Tab Jumping in Reconciliation Page (FIXED in v3.9.31)
**Issue**: Selecting dates in Reconciliation History caused tab to jump back to Import Statement
**Cause**: Date inputs triggered automatic page rerun, resetting to first tab
**Solution**: 
- Wrapped date inputs in form with "Apply Filter" button
- Added session state preservation for selected dates
- Each tab sets its active state when viewed
**Impact**: Users can now filter by date without losing their place

### 28. Transient Database Errors (FIXED in v3.9.30)
**Issue**: "Resource temporarily unavailable" errors disrupting user workflow
**Cause**: Temporary database connection issues shown directly to users
**Solution**: 
- Error messages now only logged to console
- Added caching for commission rules and MGA lists
- Cached data used when database temporarily unavailable
**Impact**: Smoother user experience during connection issues

### 29. Commission Rule Policy Type Selection (ENHANCED in v3.9.29)
**Issue**: Commission rules couldn't be specific to policy types
**Cause**: Rules only supported carrier and MGA, not policy type
**Solution**: 
- Added multi-select policy type dropdown to commission rules
- Implemented priority matching: carrier+MGA+type → carrier+type → carrier+MGA → carrier
- "All Policy Types" option for catch-all rules
**Impact**: More granular commission rate control

### 30. Tab Navigation in Reconciliation Page (LIMITATION)
**Issue**: Tabs jump back to "Import Statement" when applying date filters or saving edits
**Cause**: Streamlit's st.tabs() doesn't support programmatic tab selection
**Workaround**: 
- Date filters wrapped in form to minimize reruns
- Session state tracks selected tab but cannot set it programmatically
**Status**: Known Streamlit limitation - waiting for framework support
**Impact**: Users must manually click back to their desired tab after form submissions

### 31. Policy Term-Based Filtering Issues (FIXED in v3.9.32)
**Issue**: Incomplete transaction data when viewing policy terms or monthly reports
**Root Causes**: 
- Policy Revenue Ledger: STMT transactions filtered by wrong date field and wrong order
- Policy Revenue Ledger Reports: Entire page used date-based instead of term-based filtering
**Solutions**: 
- **Ledger**: Fixed STMT date filtering and check order
  - Filter STMT by Effective Date (not STMT DATE)
  - Check "-STMT-" pattern BEFORE transaction types
- **Reports**: Complete rewrite to term-based logic
  - Find policies starting in month
  - Show ALL transactions for those policies
**Impact**: Both pages now show complete policy lifecycle data as originally intended

## Development Guidelines

### 0. Proactive Agent Deployment (CRITICAL)
- **ALWAYS use Task agents for search and analysis operations**
- **15-SECOND RULE**: If a search or analysis takes longer than 15 seconds, IMMEDIATELY deploy the whole team of agents
- **Automatically deploy agents when:**
  - Searching for where functionality is implemented
  - Finding all usages of a function or pattern
  - Analyzing code dependencies or relationships
  - Investigating bugs across multiple files
  - Understanding complex feature implementations
  - ANY search taking more than 15 seconds
- **Deploy MULTIPLE agents in parallel**: Think like a coach - send the whole team out, don't wait for one player
- **Benefits of agent deployment:**
  - High-speed parallel searching
  - Pin-point accuracy in finding code patterns
  - Comprehensive analysis without missing edge cases
  - Reduced context usage for large searches
  - MUCH faster results with parallel execution
- **Example use cases:**
  - "Where is commission calculation handled?" → Deploy agent
  - "Find all places that update reconciliation status" → Deploy agent
  - "How does the MGA dropdown populate?" → Deploy agent
  - "Fix this bug" → Deploy MULTIPLE agents to find all related code
- **Agent results**: Trust agent findings but verify critical changes

### 1. Know When to Stop
- **If a solution is getting complex, STOP and reassess**
- **Warning signs of over-complexity:**
  - Multiple failed attempts with increasing complexity
  - Workarounds that require more workarounds
  - Fighting against framework limitations (like Streamlit's tab behavior)
  - Code that's hard to explain or understand
  - Solutions that might break existing functionality
- **Better approaches:**
  - Acknowledge the limitation and explain why
  - Suggest simpler alternatives
  - Revert changes if they're not working
  - Ask: "Is this worth the complexity?"
- **Example**: Tab reordering seemed simple but required dynamic content mapping that Streamlit doesn't support. Better to acknowledge this than create a confusing half-solution.

### 2. Before Making Changes
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