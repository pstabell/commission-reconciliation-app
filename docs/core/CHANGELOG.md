# Changelog

All notable changes to the Sales Commission App will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.9.11] - 2025-07-31 - Edit Transactions Column Order Fix

### Fixed
- **Edit Policy Transactions Column Order**
  - Fixed issue where column reordering wasn't persisting in the data editor
  - Column order now properly maintained throughout editing session
  - Auto-save preserves the correct column order
  - Session state properly stores and applies column order on display
  - Resolved UnboundLocalError by properly scoping column order storage

## [3.9.10] - 2025-07-31 - Separate Reviewed Transactions Table

### Added
- **Type → Column with Transaction Symbols**
  - New visual indicator column showing transaction type with simplified symbols
  - Clear and easy to understand symbols:
    - 💰 = STMT (Reconciliation Entry)
    - 🔴 = VOID (Voided Transaction)
    - ✏️ = END (Policy Endorsement)
    - 📄 = Regular Transaction (NEW, RWL, CAN, and all other types)
  - Column positioned after Reviewed checkbox for easy visibility

### Changed
- **Reviewed Transactions Filtering**
  - Reviewed transactions are now automatically filtered out of the main report display
  - Similar to hidden transactions, reviewed items don't clutter the working view
  - Keeps the main table focused on transactions that still need attention
  - Reviewed transactions remain accessible via "View Reviewed" button

### Fixed
- **STMT Symbol Display**
  - Changed STMT indicator from heart (💙) to dollar sign (💵)
  - Better represents the financial nature of statement entries
  - Matches user feedback about inappropriate heart symbol

### Removed
- **Column Order Info Message**
  - Removed the "📌 Column Order:" information message above the data table
  - Reduces visual clutter while maintaining the reordered columns
  - Column order tips still available in expandable section
- **Unnecessary Legend Items**
  - Removed "✅ Reviewed = Checkmark in Reviewed column" (redundant)
  - Removed "📄 Regular = Standard Transaction" (no symbol shown for regular)
  - Simplified legend to only show STMT and VOID indicators

## [3.9.9] - 2025-07-31 - Review Checkmarks for Policy Revenue Ledger Reports

### Added
- **Review Checkmark Feature**
  - New "Reviewed ✓" checkbox column in Policy Revenue Ledger Reports
  - Allows marking transactions as reviewed to track progress
  - "Save Reviewed" button to persist review status
  - Review Progress metric showing X/Y transactions reviewed with percentage
  - "View Reviewed" button to see all reviewed transactions
  - "Clear All Reviews" button to reset review status
  - Review status persists within session (clears on refresh)

- **Column Reordering for Better Navigation**
  - Reordered columns to put key fields first: Hide → Reviewed → Transaction ID → Customer → Transaction Type → Policy Type
  - Added column width optimization for better visibility
  - Added "Tips for Better Navigation" expandable guide
  - Includes keyboard shortcuts and browser zoom tips
  - Helps prevent losing context while scrolling through data

### Improved
- **Visual Transaction Type Legend**
  - Added legend showing transaction type indicators
  - ✅ Reviewed = Checkmark in Reviewed column
  - 💙 STMT = Statement/Reconciliation Entry (blue background)
  - 🔴 VOID = Voided Transaction (red background) 
  - 📄 Regular = Standard Transaction (gray background)
  - Helps users understand visual indicators at a glance

## [3.9.8] - 2025-07-31 - Edit Transactions Column Reordering

### Changed
- **Edit Policy Transactions Table Column Order**
  - Moved Carrier Name, MGA Name, Policy Type, Transaction Type before Policy Number
  - Moved Prior Policy Number to appear immediately after Policy Number
  - Moved STMT DATE to appear after Agent Paid Amount (STMT)
  - Moved Broker Fee, Policy Taxes & Fees, Commissionable Premium before Agency Estimated Comm/Revenue (CRM)
  - Moved Agent Comm % before Agent Estimated Comm $
  - Improved logical grouping of related columns for better workflow
  - Enhanced data entry efficiency with more intuitive column placement

## [3.9.7] - 2025-07-31 - Premium Calculator Label Updates

### Changed
- **Premium Sold Calculator Field Labels**
  - Changed "Existing Premium" to "Existing Net Premium" for clarity
  - Changed "New/Revised Premium" to "New/Revised Gross Premium" for clarity
  - Updated in both Edit Transaction form and Add New Policy Transaction form
  - Updated help text to reflect net/gross terminology
  - Updated CSS styling to target new field names
  - Updated formula documentation to use new terminology

## [3.9.6] - 2025-07-31 - Policy Revenue Ledger & Transaction Management Fixes

### Fixed
- **CAN Transaction Warning with Auto-Scroll**
  - Fixed warning message appearing at top of page with immediate auto-scroll
  - Warning now appears within the Edit form dialog context
  - Prevents users from missing important cancellation warnings
  - Improved user experience by keeping warnings visible near the action

- **X-DATE Display in Policy Revenue Ledger**
  - Fixed X-DATE column not showing in Policy Revenue Ledger (Editable)
  - Added Transaction Type indicators for better visibility (🆕 NEW, 🔄 RWL, 📝 END, etc.)
  - Column now appears between Policy Number and Premium Sold
  - Includes Transaction Type emoji column for quick visual identification

- **Auto-Select "All Terms" for Multi-Type Policies**
  - Fixed issue where policies with multiple transaction types (NEW + END + CAN) were defaulting to specific term filter
  - System now auto-selects "All Terms" when detecting CAN transactions
  - Ensures all related transactions are visible when cancellations are involved
  - Prevents confusion from missing transaction context

- **-IMPORT Transaction Cleanup**
  - Fixed double entry issue where -IMPORT transactions showed twice in reports
  - Corrected filter logic from IS NOT NULL to IS NULL
  - Prevents duplicate display of import transactions in Policy Revenue Ledger
  - Ensures clean, accurate transaction listings

- **Policy Type Mapping Confusion**
  - Resolved confusion between policy type mapping configurations
  - Clarified that policy_types_updated.json is the source configuration
  - policy_type_mappings.json is specifically for reconciliation statement mapping
  - Improved documentation to prevent future configuration errors

### Improved
- **User Experience**
  - Better warning placement for critical actions
  - More intuitive transaction type visibility
  - Smarter filter defaults based on transaction context
  - Cleaner transaction displays without duplicates

## [3.9.5] - 2025-07-31 - Void Improvements

### Added
- **Visual Styling for Void Reason Field**
  - Added yellow background (#fff3b0) to make field more visible
  - Added darker yellow border (#e6a800) with 2px width matching app standards
  - Made label bold with font-weight 600
  - Improves user experience by clearly indicating where to enter void reason
  - Addresses user feedback: "I have no idea where to click my mouse when it tells me to provide a reason for voiding!"

- **Double-Void Prevention**
  - Added validation to prevent voiding already-voided batches
  - Checks if VOID-{batch_id} already exists before allowing void action
  - Shows error message: "This batch has already been voided. You cannot void a batch twice."
  - Suggests using adjustment entries for corrections instead
  - Prevents duplicate VOID entries and balance calculation errors

## [3.9.4] - 2025-07-30 - Reconciliation Matching Logic Fixes

### Fixed
- **Reconciliation False Matches**
  - System was matching different policy numbers (e.g., TESTPOLICY123 to TESTPOLICY001) based on customer name alone
  - Now requires policy number match for automatic matching
  - Customer-only matches now require manual confirmation
  
- **Confidence Labeling**
  - "exact" label now only applies to 99%+ confidence matches
  - Added confidence tiers: exact (99%+), high (95%+), good (90%+), moderate (85%+), low (<85%)
  - Prevents misleading "exact" labels on partial matches
  
- **NaN Error Prevention**
  - Added NaN cleaning to `clean_data_for_database()` function
  - Converts NaN values to None before database insertion
  - Prevents database errors during reconciliation import

- **Import Button for Create-Only Reconciliations**
  - Fixed import button being disabled when only creating new transactions
  - Now enabled if there are matched, to create, OR pending manual matches
  - Automatically processes pending manual matches during import
  - Added helpful hint when manual matches are pending

- **Client ID Auto-Copy During Import**
  - New transactions created during reconciliation now copy Client ID from existing customer records
  - Prevents orphaned transactions without Client IDs
  - Maintains data consistency across all transactions for a customer

- **Nested UI Element Errors**
  - Fixed "Expanders may not be nested" error in reconciliation
  - Removed all UI feedback that could cause Streamlit conflicts
  - Graceful silent handling of missing clients table

### Added
- **Skip Option for Low Confidence Matches**
  - "Skip (Leave Unmatched)" button for matches below 90% confidence
  - Allows users to handle uncertain matches manually later
  - Improves workflow for ambiguous transactions

### Improved
- **Matching Logic Hierarchy**
  - Policy + Date match: 100% confidence
  - Customer + Policy match: 95% confidence  
  - Customer + Amount match: 90% confidence (with policy number verification)
  - Customer only: Requires manual selection
  - Prevents automatic matching without policy number verification

## [3.9.3] - 2025-07-30 - Duplicate Transaction & Agent Commission Override

### Added
- **Duplicate Transaction Feature**
  - New "📋 Duplicate Selected Transaction" button on Edit Policy Transactions page
  - Copies all transaction data except unique IDs and tracking fields
  - Generates new Transaction ID automatically
  - Opens edit form in "Create Duplicate" mode
  - Perfect for creating similar transactions or cancellations
  
- **Agent Comm % Override for Cancellations**
  - Agent Comm % field becomes editable for CAN transactions after clicking Calculate
  - Allows manual adjustment for special cases (e.g., 50% chargeback on NEW policy cancellations)
  - Shows "🔓 UNLOCKED" indicator when field is editable
  - Maintains automatic negative calculation for chargebacks

### Fixed
- **Add New Transaction Customer Name**
  - "Add New Transaction for This Client" now properly copies Customer name
  - Previously only copied Transaction ID and Client ID
  
- **Duplicate Button Selection Logic**
  - Fixed button being disabled when transaction selected
  - Moved selection count calculation before all buttons
  - Both Duplicate and Edit buttons now use same selection logic

### Improved
- **Commission Calculation Flow**
  - Agent Estimated Comm $ now respects manual rate overrides
  - Total Agent Comm updates correctly with overridden values
  - Better handling of cancellation chargeback scenarios

## [3.9.2] - 2025-07-30 - Policy Term Enhancement & Bug Fixes

### Added
- **Custom Policy Term Option**
  - Added "Custom" option to Policy Term dropdown for non-standard terms
  - Useful for policy cancellations and special endorsements
  - Manual X-DATE entry when Custom is selected

### Fixed
- **Policy Term Override Issue**
  - User changes to Policy Term were being forced back to 12 months on save
  - Removed auto-override logic in save function
  - Now respects user's manual selection
  
- **Session State Error for X-DATE Updates**
  - Fixed "st.session_state.modal_X-DATE cannot be modified" error
  - Implemented pending state pattern for widget updates
  - Calculate button now properly updates X-DATE

### Changed
- **Policy Term Database Schema**
  - Changed from INTEGER to TEXT type to support "Custom" value
  - Updated CHECK constraint to allow '3', '6', '9', '12', or 'Custom'
  - Migration script: `update_policy_term_constraint_for_custom.sql`

### Improved
- **X-DATE Auto-Calculation**
  - X-DATE updates automatically when Policy Term is changed
  - Shows pending calculation message
  - Calculate button applies the update
  - No auto-calculation for Custom term

## [3.8.15] - 2025-01-28 - Hide Rows Functionality

### Added
- **Hide Rows Feature for Policy Revenue Ledger Reports**
  - Interactive "Hide" checkbox column using `st.data_editor`
  - "🙈 Hide Selected" button to hide checked rows
  - Hidden rows counter with quick access buttons
  - Hidden Transactions management section with unhide functionality
  - "✨ Unhide Selected" for selective unhiding
  - Persistent within session (clears on refresh)

### Changed
- **Report Preview Display**
  - Switched from `st.dataframe` to `st.data_editor` for checkbox support
  - All columns except "Hide" remain read-only
  - Maintains all existing formatting and styling

- **UI Layout Improvements**
  - Moved hidden rows indicator below Saved Templates section
  - Hidden Transactions expander properly grouped with other collapsed features
  - Cleaner layout with better organization

### Improved
- Ability to focus on good transactions by hiding voided ones
- Visual feedback for hidden row management
- Intuitive checkbox interface for row selection
- Maintained all existing functionality (templates, formatting, exports)

## [3.8.14] - 2025-01-27 - Column Rename and Formatting Improvements

### Changed
- **Database Column Rename**
  - Renamed "Agent Comm (NEW 50% RWL 25%)" to "Agent Comm %" throughout the application
  - Updated all code references, configurations, and templates
  - Direct database rename for cleaner implementation
  
- **Decimal Formatting**
  - Fixed numeric columns showing 6 decimal places in Policy Revenue Ledger Reports
  - All numeric values now display with exactly 2 decimal places
  - Automatic detection and formatting of numeric columns

- **Admin Panel Enhancement**
  - Added column mapping edit functionality to Admin Panel
  - Users can now change display names without code modifications

### Improved
- Cleaner column names throughout the application
- Professional numeric formatting in all reports
- Better user experience with consistent decimal display
- Expandable sections in Policy Revenue Ledger Reports (start collapsed)

## [3.8.13] - 2025-01-27 - Default Template Feature

### Added
- **Default Template for Policy Revenue Ledger Reports**
  - Set any saved template as default with "⭐ Set as Default" button
  - Default template auto-loads when visiting the page
  - Visual indicators (⭐) show which template is default
  - Option to unset default status
  - Info message displays when default template is loaded

### Improved
- User experience by preventing "missing column" errors
- Workflow efficiency with automatic template loading
- Template management with clear default indicators

## [3.8.12] - 2025-01-27 - Contacts Edit Functionality

### Added
- **Carrier Edit Functionality**
  - Edit button on carrier detail page
  - Update carrier name, NAIC code, producer code, status, and notes
  - Form-based editing with save/cancel options
  
- **MGA Edit Functionality**  
  - Edit button on MGA detail page
  - Update MGA name, contact info, phone, email, and notes
  - Clickable MGA search results leading to detail view
  
- **MGA Section on Main Page**
  - Recent MGAs displayed as cards
  - Shows count of associated carriers
  - Click to view MGA details and associated carriers

### Improved
- User experience - no database access required for contact updates
- Search results now clickable for both carriers and MGAs
- Better organization with separate detail views

## [3.8.11] - 2025-01-27 - Policy Revenue Ledger Improvements

### Changed
- **Policy Ledger Display**
  - Renamed from "Policy Ledger (Editable)" to "Policy Ledger" (view-only)
  - Removed all editing capabilities - now purely for viewing
  - Removed Delete column functionality
  - Removed Edit Details button from Policy Details section
  - Removed Save Changes and Test Mapping buttons
  
- **Column Layout**
  - Reordered Transaction Type to appear after Transaction ID
  - Moved Description column to be the last column
  - Columns now auto-size to fit content without excess space
  
- **Policy Details Section**  
  - Updated date formatting to MM/DD/YYYY for consistency
  - Moved (X-DATE) label inline with Expiration Date in subtle gray
  - Policy Origination Date label now on single line

### Improved
- Centralized all editing in Edit Policy Transactions page
- Cleaner, more focused interface for viewing policy data
- Better column visibility with auto-sizing
- Consistent date formatting throughout

### Removed
- Client ID debug section
- All inline editing functionality from Policy Ledger
- Edit Details button and associated form

## [3.8.10] - 2025-01-27 - Policy Revenue Ledger Search Layout

### Changed
- **Policy Revenue Ledger Search Criteria**
  - Reorganized all search filters into a single row with 4 equal columns
  - Improved space utilization with full page width dropdowns
  - Maintained logical flow: Customer → Type → Date → Policy Number
  - Better visual alignment and cleaner interface
  - Selections remain visible after choosing values

### Improved
- User experience with streamlined filter selection
- Page layout efficiency with better use of horizontal space
- Visual consistency across the application

## [3.8.9] - 2025-01-26 - Policy Details Card Layout

### Changed
- **Policy Details Display**
  - Replaced table view with modern app-style card layout
  - Information now organized in visual cards with icons
  - Better visual hierarchy with grouped related information
  - Policy Origination Date displayed in subtle gray text
  - Effective and Expiration dates in full month format

- **Edit Functionality**
  - Changed from inline table editing to form-based editing
  - Single Edit Details button launches dedicated edit form
  - Cleaner save/cancel workflow

### Improved
- User experience with better visual organization
- Readability with proper information hierarchy
- Mobile responsiveness with card-based layout

## [3.8.8] - 2025-01-26 - Policy Ledger Financial Columns

### Added
- **Financial Columns in Policy Revenue Ledger**
  - Premium Sold, Policy Taxes & Fees, Commissionable Premium, Broker Fee, Broker Fee Agent Comm
  - Columns appear to the right of Delete column with horizontal scrolling
  - Maintains clean default view with financial details accessible on demand

- **Policy Financial Summary Section**
  - New section below Ledger Totals showing financial totals
  - Two rows of metrics for comprehensive financial overview
  - Automatically calculates totals for all financial columns

- **STMT/VOID Transaction Protection**
  - Delete checkbox disabled for STMT and VOID transactions
  - Save operation skips STMT and VOID rows to prevent edits
  - Visual and functional protection for reconciliation entries

### Changed
- Policy Revenue Ledger now supports horizontal scrolling for extended column view
- Save Changes logic updated to handle all columns including financial fields

## [3.8.7] - 2025-01-26 - Special Colors for STMT and VOID Transactions

### Added
- **Visual Highlighting for STMT and VOID Transactions**
  - STMT transactions now display with light blue background (#e6f3ff) 
  - VOID transactions now display with light red background (#ffe6e6)
  - Applied consistently across all data tables throughout the app
  - Makes reconciliation and void entries immediately identifiable
  - Implemented in Dashboard, All Policy Transactions, Reports, Policy Revenue Ledger Reports, and Reconciliation sections

### Changed
- Added `style_special_transactions()` utility function to apply consistent styling
- Updated dataframe displays to use styled output where Transaction ID is visible
- Policy Revenue Ledger (Editable) now includes a Type column with emoji indicators since st.data_editor doesn't support row styling

## [3.8.6] - 2025-01-25 - Statement Month and X-DATE Filters

### Added
- **Statement Month Filter in Policy Revenue Ledger Reports**
  - Filter policies by effective date month for monthly cohort tracking
  - Month selection dropdown with "All Months" default
  - Shows policy/transaction count for selected month
  - Month-specific balance due calculation
  - Selected month included in export metadata

- **X-DATE Filter in Policy Revenue Ledger (Individual)**
  - Optional filter to show transactions for specific policy term
  - "All Terms" default shows complete history
  - Smart filtering includes NEW/RWL, ENDs within term, and related payments
  - Term date range display
  - Transaction count for selected term

- **Effective Date Column in Ledger**
  - Added to transaction display for better visibility
  - Helps verify transactions within policy terms

### Changed
- **Ledger Sorting**
  - Now sorts by Effective Date chronologically (oldest first)
  - Missing dates appear at bottom
  
- **Dynamic Table Height**
  - Tables adjust to show actual rows (max 11 + blank row)
  - Scrollbar for additional rows
  
- **Export Metadata**
  - Now includes Statement Month and View Mode selections

### Fixed
- **Client ID Display in Policy Details**
  - Intelligently selects transaction with Client ID populated
  - Shows most complete information available
  - Handles cases where some transactions lack Client ID

- **Excel Update Tool**
  - Fixed datetime serialization errors
  - Excludes calculated fields (Policy Balance Due)
  - Better multi-sheet detection for Policy Revenue Report exports
  - Improved error messages

## [3.8.5] - 2025-01-24 - Excel Update Tool and View Toggle

### Added
- **Excel Update Tool in Tools → Import/Export**
  - Bulk update existing transactions from modified Excel files
  - Transaction ID matching ensures only existing records are updated
  - Selective column updates - only modifies columns present in Excel
  - Preview shows which transactions and columns will be affected
  - Progress tracking with real-time status updates
  - Comprehensive Excel report with summary, details, and error sheets
  - Both Excel and CSV download options for update reports

- **View Toggle in Policy Revenue Ledger Reports**
  - Switch between "Aggregated by Policy" and "Detailed Transactions" views
  - Aggregated view: One row per policy with summed values
  - Detailed view: All individual transactions with full details
  - Metrics adjust based on view mode
  - Context-specific help text for each view
  - All report features (filters, exports) work with both views
  - Missing columns (Transaction Type, etc.) now available in detailed view

- **Template Persistence**
  - Report templates now save to JSON file for persistence
  - Templates survive page navigation and app restarts
  - Auto-loads saved templates on page visit
  - Added prl_templates.json to .gitignore

### Changed
- **Excel Update Warning**
  - Clarified that only columns in Excel file are updated
  - Other database columns remain unchanged
  - Added visual confirmation of which columns will be modified

### Fixed
- **Report Templates Not Saving**
  - Templates now persist in config_files/prl_templates.json
  - Fixed loss of templates on page navigation

## [3.8.4] - 2025-07-19 - Balance Filters, Audit Help, and Date Formatting

### Added
- **Balance Filters in Policy Revenue Ledger Reports**
  - New dropdown filter to show policies by balance status
  - Options: All Balances, Positive Only (>$0), Zero Only (=$0), Negative Only (<$0), Non-Zero (≠$0)
  - Filter selection included in export metadata
  - Shows count of policies matching selected filter

- **Policy Audit Strategy in Help Page**
  - Comprehensive guide for auditing policy records
  - Located in Help > Features Guide tab
  - Includes prioritized approach, red flags, and daily strategies
  - Expandable section for easy access

### Changed
- **Date Display Format**
  - Removed date formatting overrides to show raw YYYY-MM-DD format
  - Dates now display exactly as stored in database
  - Updated date saves to consistently use YYYY-MM-DD format
  - Changed help text to reflect correct date format

- **Edit Renewal Transaction Form**
  - NOTES field now clears when creating renewal transactions
  - Prevents copying notes from original policy to renewal

### Fixed
- **Commission Rate Display**
  - Fixed commission rates not showing next to carrier names
  - Improved error handling for carrier data loading
  - Added retry mechanism for database connections

## [3.8.3] - 2025-07-17 - Enable IMPORT Transaction Deletion

### Changed
- **IMPORT Transaction Deletion**
  - Enabled deletion of IMPORT transactions (transactions with -IMPORT suffix)
  - Previously, IMPORT transactions were protected from deletion
  - Reconciliation transactions (-STMT-, -VOID-, -ADJ-) remain protected
  - Added informational message when deleting IMPORT transactions
  - Useful for cleaning up duplicate or erroneous import records

## [3.8.2] - 2025-07-17 - Table Width Fix

### Fixed
- **Edit Policy Transactions Table Width**
  - Fixed table not using full screen width
  - Issue: st.data_editor was inside a column context limiting its width
  - Solution: Moved table outside column structure to page level
  - Table now matches width of "Find Policies to Edit" section
  - All features preserved: checkboxes, buttons, edit modal, delete functionality
  - Fixed multiple indentation errors that resulted from the restructuring

### Technical
- Restructured approximately 650 lines of code to fix indentation
- Removed redundant else/elif statements causing syntax errors
- Table now uses use_container_width=True at page level

## [3.8.1] - 2025-07-17 - Enhanced Policy Term & Origination Date Features

### Added
- **Auto-populate 12-month Policy Term for NEW/RWL**
  - NEW and RWL transactions (except AUTO) automatically get 12-month term
  - X-DATE auto-calculates as Effective Date + 12 months
  - Visual feedback before saving with info messages
  - Works on form load and when pressing Enter
  - Fallback on Save button ensures values are always set

- **Enhanced Policy Origination Date for Endorsements**
  - END transactions now properly trace back to NEW transaction
  - Fixed policy number lookup to use user's input instead of original data
  - Improved auto-population for continuation transactions
  - More aggressive population for END, RWL, PCH, REWRITE types

### Fixed
- Policy Term dropdown not displaying calculated value
- Session state conflicts with Policy Term widget
- Policy number format mismatch preventing origination date lookup
- Debug messages removed after successful testing

## [3.8.0] - 2025-07-17 - Policy Origination Date Auto-Population

### Added
- **Policy Term Auto-Population**
  - Automatically calculates Policy Term based on Effective Date and X-DATE
  - Rounds to standard terms (3, 6, 9, 12 months) with 15-day tolerance
  - Updates in real-time as dates are changed

- **Policy Origination Date Auto-Population**
  - NEW transactions: Auto-populates from Effective Date
  - BoR transactions: Uses Effective Date (new relationship)
  - Other types: Traces back through policy chains to find original NEW transaction
  - Follows Prior Policy Number chains recursively
  - Circular reference protection
  - Clear visual feedback with auto-populate messages

- **Batch Update Tool for Policy Origination Dates**
  - New tool in Tools → Data Tools
  - Analyzes all transactions missing Policy Origination Date
  - Excludes reconciliation transactions (-STMT-, -VOID-, -ADJ-)
  - Preview changes before applying
  - Progress tracking during updates
  - Downloadable report of all changes
  - Metrics show Total, Regular, and Missing counts

### Fixed
- Progress bar error when value exceeded 1.0
- Date format handling for mixed date formats
- Proper exclusion of reconciliation transactions from analysis

### Technical
- Added recursive `find_origination_date()` function
- Improved date handling without forced formatting
- Better progress tracking with enumerate()
- Added filtering for reconciliation transactions

## [3.7.6] - 2025-07-17 - Policy Type Consistency & Accounting Page Removal

### Fixed
- **Policy Type Consistency**
  - Edit Transaction and Add New Policy forms now use same policy types as Admin Panel
  - Both forms load from `policy_types_updated.json` instead of old `policy_types.json`
  - Shows HOME, CONDO, DP1, AUTO etc. instead of old hardcoded list
  - Added proper format conversion for compatibility

- **Delete Error Message Logic**
  - Fixed "Could not identify transaction IDs" appearing for import transactions
  - Error only shows when Transaction ID column truly can't be found
  - Properly handles protected transaction warnings without duplicate errors

- **UnboundLocalError in Edit Form**
  - Fixed `current_transaction_type` variable scope issue
  - Variable now defined before column creation
  - Available in both col11 and col12 for calculations and help text

### Removed
- **Accounting Page**
  - Safely removed redundant Accounting page from navigation
  - All functionality already exists in enhanced Reconciliation page
  - No broken dependencies or references
  - Cleaner, more focused navigation menu

### Technical
- Updated `load_policy_types()` and `load_policy_types_config()` functions
- Improved error handling for transaction deletion
- Better variable scoping in commission calculations

## [3.7.5] - 2025-07-16 - Date Format Simplification & Update Fix

### Fixed
- **Cancellation Commission Calculations (CAN/XCL)**
  - Fixed CAN and XCL transactions not calculating negative commissions
  - Now properly calculates chargebacks based on original commission rate
  - Uses Prior Policy Number to determine if chargeback is at 25% (renewal) or 50% (new)
  - Both Agency and Agent commissions show as negative amounts
  - Added "(CHARGEBACK)" label to help text for clarity

### Fixed
- **Edit Transaction Form Update Error**
  - Fixed "Update may have failed - no data returned" error
  - Added `.select()` to update operation to return data
  - Supabase doesn't return data after UPDATE by default
  - Now properly confirms successful updates
  - Changed error message to warning for edge cases

### Changed
- **Removed All Date Format Overrides**
  - Deleted format_dates_mmddyyyy() function completely
  - Removed all format="MM/DD/YYYY" parameters from st.date_input() widgets
  - Updated convert_timestamps_for_json() to use ISO format (isoformat())
  - Removed date formatter tool from Tools page
  - Let Streamlit handle all date formatting naturally

### Impact
- Dates now display consistently in ISO format (YYYY-MM-DD)
- Resolves persistent date reversal issues
- Significantly simplifies codebase
- Better international compatibility
- More reliable date handling
- Database dates stored in standard format

### Technical
- Removed ~50 lines of date formatting code
- Eliminated format override conflicts with Streamlit
- Cleaner JSON serialization with ISO dates
- No more MM/DD/YYYY vs YYYY-MM-DD confusion

## [3.7.4] - 2025-07-16 - Contacts Page UX Improvements

### Added
- **Add MGA Form Implementation**
  - Created missing MGA form functionality
  - Added fields: MGA Name*, Contact Name, Phone, Email, Website, Notes
  - Form appears when "Add MGA" selected from Quick Add dropdown
  - Saves new MGAs to database with Active status

### Changed
- **Form Positioning for Better UX**
  - Moved Add Carrier form to appear immediately after Quick Add dropdown
  - Add MGA form appears right after Add Carrier form
  - Both forms now "above the fold" - visible without scrolling
  - Removed duplicate Add Carrier form from bottom of page
  - Better user experience - users can see forms are working

### Technical
- Forms appear conditionally based on session state
- Consistent form styling with two-column layout
- Primary action buttons with Cancel option
- Auto-clear session state and rerun after successful submission

## [3.7.3] - 2025-07-15 - Policy Type Rename Feature

### Added
- **Rename Policy Types Feature in Admin Panel**
  - New "Rename Policy Types" section in Policy Types tab
  - Allows renaming existing policy types to new standardized names
  - Text input for new name (e.g., rename "Auto" to "AUTO")
  - Shows transaction count for the type being renamed
  - Validates that new name doesn't already exist
  - Updates all transactions to use the new name
  - Automatically updates policy type mappings if renamed type was mapped
  - Clear success feedback showing number of updated transactions

### Technical
- Positioned between Merge and Backup sections
- Reuses policy type data from merge section when available
- Prevents renaming to existing names (suggests merge instead)
- Updates config_files/policy_type_mappings.json automatically
- Clears cache after rename for immediate updates

## [3.7.2] - 2025-07-15 - Policy Type Merge Feature

### Added
- **Merge Policy Types Feature in Admin Panel**
  - New "Merge Policy Types" section in Policy Types tab
  - Select source type (to be merged from) and target type (to be merged into)
  - Shows transaction count for each policy type before merging
  - Updates all transactions to use the target type
  - Automatically updates policy type mappings if merged type was mapped
  - Clear warning about irreversible action
  - Clears cache after merge to reflect changes immediately

### Technical
- Queries database for unique policy types and transaction counts
- Uses Supabase update to change all matching transactions
- Updates config_files/policy_type_mappings.json if needed
- Prevents merging a type into itself
- Shows helpful preview of what will happen

## [3.7.1] - 2025-07-15 - Policy Type Mapping Validation

### Added
- **Policy Type Mapping Validation During Import**
  - Reconciliation import now checks for unmapped policy types before processing
  - Shows clear error message listing all unmapped types found in statement
  - Prevents import until mappings are configured in Admin Panel
  - Protects data integrity by ensuring all policy types map to standardized values
  - Helpful instructions guide users to Policy Type Mapping tab

### Technical
- Added validation check after clicking "Process & Match Transactions"
- Loads both policy_type_mappings.json and policy_types_updated.json
- Checks statement policy types against both mappings and existing types
- Uses st.stop() to halt processing if unmapped types found
- Maintains existing mapping application during transaction creation

## [3.7.0] - 2025-07-15 - Enhanced Pending Renewals & Premium Calculator

### Added
- **Premium Sold Calculator for Endorsements in Edit Transaction Form**
  - Added endorsement calculator with Existing Premium and New/Revised Premium fields
  - Automatically calculates difference (positive or negative)
  - Changed "Direct Premium Entry" to "New Policy Premium" to match Add New Policy form
  - Premium Sold field auto-populates from calculator when used
  - Helpful text indicates when calculator value is being used

- **Enhanced Pending Policy Renewals**
  - Shows ALL past-due renewals (removed -30 day limit)
  - Summary metrics: Past Due, Due This Week, Due This Month, Total Pending
  - Time range filtering: All, Past Due Only, This Week, 30/60/90 days
  - Visual status indicators: 🔴 Past Due, 🟡 Urgent (0-7 days), ✅ OK
  - Status column added for at-a-glance renewal urgency
  - Past-due renewals sorted first for immediate attention
  - CAN and XCL transactions continue to exclude policies from renewals

- **Carrier Commission Rate Loading in Pending Renewals**
  - Added carrier/MGA selection UI to Edit Renewal Transaction form
  - Commission rates automatically populate when carrier/MGA selected
  - Renewal rates applied based on RWL transaction type
  - Visual tip reminder to select carrier from dropdown
  - Shows commission rule description when rate found
  - Consistent with Edit Policy Transactions functionality

- **Policy Revenue Ledger "All Dates" Option**
  - Added "All Dates" option to Effective Date filter dropdown
  - Allows viewing all policies regardless of effective date
  - Helps handle date format issues without requiring immediate fixes
  - Maintains backward compatibility with specific date selection

### Changed
- Pending renewals now sorted by Days Until Expiration (ascending)
- Updated empty state messages to be more informative based on filters

### Fixed
- Removed debug captions from carrier commission lookup
- Fixed "Days Until Expiration" database error when creating renewals
- Fixed redundant "Use None" button in client search results
- Made all Policy Information fields start empty in Add New Policy form

### Technical
- Enhanced `get_pending_renewals()` to show all past-due with no lower limit
- Added `style_renewal_rows()` function (ready for future styling support)
- Added status icon column as visual workaround for st.data_editor limitations
- Integrated carrier/MGA selection UI into renewal edit workflow
- Updated `clean_data_for_database()` to include 'Days Until Expiration' and 'Status' fields
- Enhanced client search to filter out entries without valid Client IDs
- Changed date field defaults from today's date to None for cleaner form resets

## [3.6.5] - 2025-07-15 - Void Date Extraction Fix

### Fixed
- **Void Transactions Date Issue**
  - Fixed void transactions using current date instead of statement date
  - Issue: Void entries created with today's date, making them invisible in historical views
  - Root cause: Date extraction only handled IMPORT- prefix, not REC- or MNL- formats
  - Solution: Enhanced to use regex pattern `-(\d{8})-` to extract date from any batch ID
  - Now supports all batch formats: IMPORT-YYYYMMDD-X, REC-YYYYMMDD-X, MNL-YYYYMMDD-X
  - Both Transaction ID suffix and STMT DATE now use correct statement date
  - Impact: Void transactions appear in correct time period in reconciliation history

### Technical
- Replaced hardcoded prefix checks with flexible regex pattern matching
- Extracts YYYYMMDD pattern from any position in batch ID
- Maintains backward compatibility with all existing batch formats

## [3.6.4] - 2025-07-15 - Search & Filter Column Name Fix

### Fixed
- **Search & Filter KeyError**
  - Fixed KeyError: 'Transaction_ID' preventing filter functionality
  - Issue: Code used underscore-separated column names but database has space-separated
  - Solution: Updated all column references to use correct names
  - Changes:
    - Text filters: Transaction ID, Policy Number, Client ID
    - Dropdown filters: Policy Type, Transaction Type
    - Date filter: Effective Date
    - Numeric filters: Agent Paid Amount (STMT), Policy Balance Due
  - Impact: Search & Filter page now fully functional

## [3.6.3] - 2025-07-14 - Extended Checkbox Performance Fix

### Fixed
- **Regular Search Checkbox Performance**
  - Extended checkbox performance optimization to regular search results
  - Previously only attention filter had instant response
  - Issue: 7-second delay after clicking checkbox before Edit button became available
  - Solution: Implemented cached selection state that only recalculates when selection changes
  - Technical: Caches selected count and index in session state for immediate access
  - Impact: All checkbox interactions now instant across entire Edit Policy Transactions page

## [3.6.2] - 2025-07-13 - Performance Optimization & Bug Fixes

### Fixed
- **Wright Flood MGA Loading Error**
  - Fixed UUID parsing error causing 500 error when loading Wright Flood records
  - Issue: Database contained UUID values that couldn't be parsed in data display
  - Solution: Implemented safe UUID conversion with error handling
  - Impact: Wright Flood commission rules now load and display correctly

- **Edit Policy Transactions Checkbox Performance**
  - Fixed 6-7 second delay when clicking checkboxes due to DataFrame operations
  - Root cause: Session state updates triggering full data refresh with every click
  - Solution: Optimized checkbox handling to update only necessary state
  - Impact: Checkbox interactions now instant, dramatically improved user experience

- **IndexError on Transaction Selection**
  - Fixed "IndexError: index 0 is out of bounds" when selecting edited transactions
  - Issue: Row indices changing after edits caused selection misalignment
  - Solution: Added validation to ensure indices are within bounds before access
  - Impact: Transaction selection now works reliably after any edits

- **Client ID Debug Caption Position**
  - Repositioned debug caption for Client ID field from above to below the field
  - Improved form layout and readability
  - Better user experience with clearer field relationships

### Technical
- Added comprehensive error handling for UUID operations throughout the application
- Optimized session state management for checkbox operations
- Implemented bounds checking for all DataFrame index operations
- Improved debug information positioning in forms

### Impact
Significant performance improvements in the Edit Policy Transactions page, eliminated critical errors preventing MGA data access, and enhanced overall application stability. Users experience faster, more reliable operation with better error resilience.

## [3.6.1] - 2025-07-13 - Client ID Generation in Edit Transaction Form

### Added
- **Generate Client ID Button in Edit Transaction Form**
  - New "Generate Client ID" button appears when Client ID field is empty
  - Automatically generates unique 8-character ID in format CL-XXXXXXXX
  - Updates both the form field and database immediately
  - Button disappears after successful generation
  - Maintains data integrity by ensuring unique Client IDs
  - Available in both Edit Policy Transactions page and modal forms

### Technical
- Client ID generation uses same logic as Add New Policy form
- Real-time database update without requiring form save
- Session state synchronization for immediate UI updates
- Prevents duplicate Client ID generation

### Impact
Users can now generate Client IDs for existing transactions that are missing them, ensuring all transactions have proper client identification for reporting and data integrity.

## [3.6.0] - 2025-07-13 - Contacts & Commission Structure Management

### Added
- **NEW: Contacts & Commission Structure Management**
  - Added dedicated Contacts page with Carriers and MGAs tabs
  - Carrier management with NAIC codes, producer codes, and status tracking
  - MGA (Managing General Agency) management with contact information
  - Commission rules system with carrier/MGA/policy type specific rates
  - Support for NEW and RWL (renewal) commission rates
  - Payment terms tracking (Advanced vs As Earned)
  - Island architecture implementation for complete page isolation
  - Database schema for carriers, MGAs, relationships, and commission rules

- **Modern Policy Types Configuration**
  - Redesigned Admin Panel Policy Types section with compact grid layout
  - Visual category grouping for better organization
  - Configuration file-based management for safety
  - Download configuration option for backup
  - Clear documentation for adding new policy types

### Database
- Created new tables: carriers, mgas, carrier_mga_relationships, commission_rules
- Added optional carrier_id and mga_id columns to policies table
- Created indexes for performance optimization
- Added update timestamp triggers
- Full backward compatibility maintained

### Technical
- Island architecture implementation for Contacts page
- Configuration file approach for policy types (policy_types_updated.json)
- SQL scripts for table creation and initial data population
- Support for complex commission structures from Excel data

## [3.5.15] - 2025-07-12 - Enhanced Reconciliation UI & Client ID Matching

### Added
- **Enhanced Reconciliation UI**
  - Clear "Force match" labels with transaction ID display
  - Smart warning system for customer name mismatches (red text)
  - Improved "Create new transaction" labels showing customer names
  - Pre-fill confirmation messages for better clarity
  - Flipped checkbox order - safer "Create new" option on left, riskier "Force match" on right

- **Client ID Matching for New Transactions**
  - Automatic client lookup when creating new transactions during reconciliation
  - Radio button selection for existing clients vs creating new
  - Shows exact matches and similar client names
  - Creates new client records with auto-generated Client IDs (CL-XXXXXXXX)
  - Links all new transactions to appropriate Client IDs

- **Transactions Requiring Attention Filter**
  - New button on Edit Policies page: "Show Transactions Requiring Attention"
  - Filters transactions with payments but missing premium/commission data
  - Helps ensure accurate ledger reports by catching incomplete data
  - Uses existing edit workflow for quick data completion

- **Agency Comm Received Made Optional**
  - Moved from required to optional fields in reconciliation
  - Positioned in right column with other optional fields
  - Allows reconciliation without agency commission data

### Changed
- **Reconciliation Success Message Delay**
  - Extended from 2 to 4 seconds for better visibility
  - Ensures users can read confirmation details

### Fixed
- **Smart Warning Logic**
  - No warnings for high-confidence name reversals (≥95%)
  - No warnings for exact matches or business name variations
  - Red warnings only for genuine mismatches

### Technical
- Enhanced `find_potential_customer_matches` for client lookup
- Client record creation during transaction import
- Proper session state handling for client selections

## [3.5.14] - 2025-07-11 - Statement Details in Unmatched Transactions

### Added
- **Statement Details Display**
  - LOB/Chg (Line of Business/Change) shown for unmatched transactions
  - Transaction type from statement displayed
  - Commission Rate shown with smart percentage formatting
  - Rate field added to optional column mappings
  - Helps identify transactions during manual matching

### Fixed
- **Duplicate Rate Display**
  - Removed redundant Rate display when mapped column matches direct column
  - Cleaner statement details without duplicate information
- **Rate Field Database Error**
  - Created `clean_data_for_database()` function to remove UI-only fields before insertion
  - Prevents "Could not find the 'Rate' column" error during import
  - Applied to all database insert operations throughout the app
- **Missing effective_date KeyError**
  - Fixed error when statement data missing required fields
  - Updated to use `.get()` with safe defaults for all dictionary access
  - Handles incomplete statement data gracefully

### Technical
- Smart column detection for variations (LOB/Chg, LOB, Tran, Transaction, Rate)
- Automatic percentage formatting (0.15 → 15%, 15 → 15%)
- Only displays fields with actual values
- Comprehensive UI-only field cleaning before database operations

## [3.5.13] - 2025-07-11 - Enhanced Transaction Matching & Debug Mode

### Added
- **Debug Mode for Unmatched Transactions**
  - New expandable debug section shows ALL transactions for a customer
  - Displays credit, debit, and balance calculations for each transaction
  - Explains why transactions aren't available (e.g., zero balance)
  - Helps identify customer name mismatches or reconciliation issues

- **Improved Customer Name Matching**
  - Added "all words" matching (88% confidence) for any word order
  - Added "most words" matching (82% confidence) for partial matches
  - Better handles variations like "Adam Gomes" vs "Gomes, Adam" vs "Adam J. Gomes"
  - Reduces false negatives in customer matching

### Technical
- Enhanced `find_potential_customer_matches` with fuzzy word-based matching
- Added detailed balance calculation display in debug mode
- Shows exact reasons why transactions are excluded from matching

### Impact
Users can now troubleshoot why specific transactions aren't appearing in the matching dropdown. The debug mode provides transparency into balance calculations and helps identify data issues. Improved customer matching reduces manual work when names don't match exactly.

## [3.5.12] - 2025-07-11 - Void Screen Agent Amount Fix

### Fixed
- **Void Screen Showing Wrong Amounts**
  - Fixed Adjustments & Voids tab showing Agency amounts instead of Agent amounts
  - Void selection dropdown now displays the same amounts as Reconciliation History
  - Ensures consistency between reconciliation and void operations

### Technical
- Changed all references in void section from 'Agency Comm Received (STMT)' to 'Agent Paid Amount (STMT)'
- Updated batch summary aggregation, dropdown display, batch total, and transaction details

### Impact
Users now see consistent commission amounts throughout the reconciliation system. The void screen correctly shows agent commissions (what you were paid) rather than agency commissions (what the agency received), preventing confusion and ensuring accurate void operations.

## [3.5.11] - 2025-07-11 - Reconciliation Error Handling

### Fixed
- **Missing effective_date KeyError**
  - Fixed error when reconciling statements with missing effective_date fields
  - Added safe fallbacks for customer, policy_number, and effective_date
  - Prevents crashes when processing incomplete statement data

### Technical
- Updated reconciliation entry creation to use .get() with empty string defaults
- Handles cases where statement items have None or missing required fields

### Impact
Reconciliation process is now more robust and can handle statements with incomplete or missing data fields without errors.

## [3.5.10] - 2025-07-11 - Manual Match Reconciliation Fixes

### Fixed
- **KeyError 'balance' for Manual Matches**
  - Fixed error when displaying manually matched transactions
  - Manual customer-only matches now display statement amount as balance
- **KeyError 'Policy Number' During Import**
  - Fixed error when creating reconciliation entries for manual matches
  - System now uses statement data when match fields are missing

### Added
- **Endorsement Reminder Caption**
  - Added helpful caption under "Create as new transaction" checkbox
  - Text: "*(Use for new policies or endorsements not yet in system)*"
  - Reminds users that endorsements are common reasons for unmatched transactions

### Technical
- Manual matches now gracefully handle missing transaction fields
- Improved error handling for customer-only matches

### Impact
Manual matching workflow is now fully functional, allowing users to match transactions even when exact database matches aren't found.

## [3.5.9] - 2025-07-11 - Manual Transaction Matching

### Added
- **"Match transaction" Checkbox**
  - New checkbox appears next to "Create as new transaction" for unmatched items
  - Allows manual matching to existing customers even without exact transaction match
  - Prevents duplicate customer entries (e.g., "D'Alessandro, Nicole" vs "Nicole D'Alessandro")
  - Displayed only when potential customer matches are found

### Changed
- **Repository Cleanup**
  - Moved all commission_app backup files to backups/ folder
  - Moved all .md files (except README) to docs/ folder structure
  - Removed 298,205 lines of backup files from root directory
  - Consolidated backup and backups folders into single backups/ folder

### Technical
- Added dual-checkbox layout for transaction handling options
- Implemented manual match logic to find transactions by customer/policy/date
- Falls back to customer-only match if no exact transaction found

### Impact
Significantly improves reconciliation workflow by allowing users to manually resolve customer name mismatches without creating duplicate entries. Repository is now clean and well-organized.

## [3.5.8] - 2025-07-10 (Late Evening) - Void Reconciliation Balance Fix

### Fixed
- **Unreconciled Transactions Not Showing After Void**
  - Fixed calculation in `calculate_transaction_balances` to include -VOID- entries
  - Voided reconciliations now properly show transactions as unreconciled
  - Balance calculation now accounts for negative void amounts that reverse payments
  - Aligns with Policy Ledger's correct accounting logic

### Technical
- Updated balance calculation to include both -STMT- and -VOID- entries
- -VOID- entries have negative amounts that properly offset original -STMT- entries
- Ensures voided transactions reappear in Unreconciled Transactions tab

### Impact
When a reconciliation batch is voided, the affected transactions now correctly show as having outstanding balances again, allowing them to be re-reconciled in future statements.

## [3.5.7] - 2025-07-10 (Late Evening) - Import Function Parameter Fix

### Fixed
- **"name 'all_data' is not defined" Error During Import**
  - Fixed error when clicking "Proceed with Import" in reconciliation
  - Added missing `all_data` parameter to `show_import_results` function
  - Ensures customer name matching works during import process

### Technical
- Updated function signature to pass `all_data` from reconciliation page context
- Maintains access to existing customer data for name matching

### Impact
Reconciliation imports now work without errors, maintaining the customer name consistency feature from v3.5.6.

## [3.5.6] - 2025-07-10 (Evening) - Customer Name Consistency Fix

### Fixed
- **Reconciliation Customer Name Format Issue**
  - Fixed inconsistent customer naming when creating new transactions during import
  - System now checks for existing customers before creating new ones
  - Uses existing customer name format instead of statement format (e.g., "Susmit K. Ghosh" not "Ghosh, Susmit")
  - Prevents duplicate customer entries with different name formats

### Technical
- Enhanced transaction creation logic to use `find_potential_customer_matches`
- Added customer name normalization for "Last, First" format matching
- Maintains data integrity by using consistent customer names across all transactions

### Impact
Reconciliation imports now maintain consistent customer naming conventions. When importing statements with different name formats, the system matches to existing customers and uses their established name format, preventing duplicate customer entries and ensuring data consistency.

## [3.5.5] - 2025-07-10 (Evening) - Duplicate Transaction Fix

### Fixed
- **Duplicate Transaction Creation on Inline Add/Edit**
  - Fixed issue where editing a newly added inline transaction created a duplicate instead of updating
  - Modal save logic now checks database for existing Transaction ID before deciding INSERT vs UPDATE
  - Resolves issue where inline-added transactions lacked `_id` in session state
  - Prevents duplicate records when using "Add New Transaction for This Client" followed by edit

### Technical
- Enhanced modal save logic to query database for existing records by Transaction ID
- Added fallback check when `_id` is not available in session state
- Ensures proper UPDATE operation for records that exist in database but not in local state

### Impact
Users can now safely add transactions inline and immediately edit them without creating duplicates. The system properly recognizes existing records regardless of how they were created, maintaining data integrity throughout the add/edit workflow.

## [3.5.4] - 2025-07-10 (Evening) - Void Visibility Enhancement

### Added
- **Comprehensive Void Status Tracking in Reconciliation History**
  - By Batch view now displays Status, Void ID, and Void Date columns
  - All Transactions view shows Reconciliation Status, Batch ID, and Is Void Entry columns
  - Color coding: Light red for voided batches, light orange for void entries
  - Clear visual indicators make voided reconciliations immediately apparent

### Fixed
- **Void Transactions Not Appearing in Reconciliation History**
  - Updated filter to include both `-STMT-` and `-VOID-` transactions
  - Fixed case-sensitive status comparisons (now handles lowercase 'void')
  - Enhanced void entry detection to check Transaction ID patterns
  - Original batches now correctly show as VOIDED when void entries exist

### Technical
- Modified reconciliation entry filter from single pattern to OR condition
- Added case-insensitive string comparisons throughout void detection
- Improved batch status aggregation logic
- Enhanced styling functions with proper void status highlighting

### Impact
Users can now clearly see which reconciliations have been voided without investigating individual transactions. The reconciliation history provides complete visibility into the status of all statements, preventing confusion about which are active vs. voided.

## [3.5.3] - 2025-07-10 (Evening - Critical Fix)

### Fixed
- **Critical Production Error**: StreamlitDuplicateElementKey error when editing transactions
  - Removed 657 lines of duplicate edit form code in Edit Policies page
  - Consolidated to use single reusable edit_transaction_form function
  - Added proper field tracking to prevent duplicate widget rendering
  - Fixed form name conflicts that caused production crashes

### Technical
- Eliminated duplicate form implementation that was causing key conflicts
- Improved field rendering tracking in edit forms
- Ensured consistent form behavior across all edit contexts

## [3.5.2] - 2025-07-10 (Evening)

### Added
- **UI Improvements for Pending Policy Renewals**
  - Added info box reminder about using Cancel button to switch transactions
  - Made all Calculate buttons primary (blue) type for better visibility
  - Improved user guidance during renewal editing workflow

- **Cancel/Rewrite Workflow Enhancement**
  - Added comprehensive Cancel/Rewrite Scenario Guide to Help page
  - Implemented automatic exclusion of cancelled policies from Pending Renewals
  - Added Prior Policy Number field to Add New Policy form for complete tracking
  - Documented best practices for handling mid-term policy changes

### Changed
- **Form Field Reorganization**
  - Moved Policy Type field to right column under MGA Name in Pending Renewals
  - Improved visual hierarchy and logical field grouping
  - Better balance between left and right columns in edit forms

### Fixed
- **Cancel/Rewrite Issues**
  - Cancelled policies (with CAN transactions) no longer appear in Pending Renewals
  - Prior Policy Number field now available in Add New Policy form
  - Proper handling of policy chains for cancelled and rewritten policies

### Technical
- Updated `get_pending_renewals()` to check for CAN transaction types
- Enhanced Add New Policy form with conditional Prior Policy Number field
- Improved edit transaction form layout with better field positioning

## [3.5.1] - 2025-07-10 (Afternoon)

### Added
- **Enhanced Pending Renewals Filtering**
  - Policies with renewal transactions are now automatically hidden from Pending Renewals
  - System checks Prior Policy Number field to identify already-renewed policies
  - Prevents duplicate renewal processing

### Changed
- **Data Loading Architecture**
  - Moved from global data loading to page-specific loading
  - Each page now loads fresh data independently
  - Eliminates stale data issues between page navigation
  - Cache TTL remains at 5 minutes for performance

### Fixed
- **Pending Policy Renewals Display Bug**
  - Fixed issue where "NEW" transactions incorrectly displayed as "RWL"
  - Removed inappropriate `duplicate_for_renewal()` call for display purposes
  - Transaction Types now display correctly without modification
- **Data Refresh Issues**
  - Fixed stale data showing in Pending Renewals after edits
  - Resolved cache synchronization between Edit and Pending Renewals pages
  - All pages now show current data after modifications

### Technical
- Removed multiple duplicate `else` statements causing syntax errors
- Fixed indentation issues in Policy Revenue Ledger section
- Improved error handling for missing data scenarios

## [3.5.0] - 2025-07-10 (Morning)

### Added
- **Policy Renewal Tracking System**
  - Prior Policy Number field to maintain complete policy chain history
  - Automatic tracking of policy number changes (common in commercial surplus lines)
  - Complete audit trail from original policy through all renewals
  - Policy Origination Date preservation throughout renewal chain
  - Prior Policy Number auto-population in renewal forms (read-only)
  - Universal tracking for all policies, not limited to surplus lines

- **Database Schema Enhancements**
  - Prior Policy Number column in policies table
  - Migration scripts for schema updates
  - Improved column naming consistency

- **Technical Improvements**
  - `convert_timestamps_for_json()` utility function for proper serialization
  - Unique Transaction ID generation with collision checking
  - Comprehensive column reordering system
  - Timestamped backup system for version control
  - Enhanced error handling with detailed debugging

- **Documentation**
  - Migration scripts with step-by-step instructions
  - Test scripts for renewal functionality verification
  - Future plan for column selection feature on Edit Policy Transactions

### Changed
- **Database Updates**
  - Renamed "NEW BIZ CHECKLIST COMPLETE" to "Policy Checklist Complete"
  - Standardized column naming conventions

- **UI/UX Improvements**
  - MGA Name now appears immediately after Carrier Name in all views
  - Policy Term moved to appear after Policy Origination Date
  - Standardized column order in All Policy Transactions page
  - All numeric columns now display with two decimal places (e.g., $3971.00)
  - Prior Policy Number positioned next to Policy Number for easy comparison

### Fixed
- JSON serialization error for pandas Timestamp objects during renewals
- Duplicate Transaction ID generation causing primary key violations
- Datetime column display errors in Dashboard Quick Client Search
- Column name mapping issues (expiration_date → X-DATE)
- Multiple schema mismatch errors during renewal process
- Non-existent UI fields causing database insert failures
- Dashboard search results number formatting

### Security
- All renewal operations maintain data integrity
- Audit trail ensures compliance tracking

## [3.4.0] - 2025-07-10 (Afternoon)

### Added
- **Shared Edit Transaction Form**
  - Reusable `edit_transaction_form()` function for consistency
  - Single source of truth for all transaction editing
  - Unified editing experience across application

- **Enhanced Renewal Mode**
  - Transaction Type auto-locked to "RWL"
  - Policy Origination Date preserved as read-only
  - Effective Date auto-population from previous expiration
  - X-DATE calculation based on Policy Term
  - Commission fields auto-clear for fresh entry
  - New Transaction ID preview as grayed-out field

- **Safe Edit Workflow**
  - Single Edit checkbox column with clear purpose
  - "Edit Selected Pending Renewal" button with validation
  - Prevention of accidental batch renewals
  - Clear error messages for multiple selections

### Changed
- Removed confusing dual checkbox columns
- Reorganized form sections for better logical flow
- All calculated fields now show formulas in tooltips

## [3.3.0] - 2025-07-10 (Morning)

### Added
- **MGA Name Column**
  - Managing General Agent tracking
  - Strategic placement after Carrier Name
  - Integration with all forms and displays

- **Policy Term Feature**
  - Duration tracking (3, 6, 9, or 12 months)
  - Accurate renewal date calculations
  - Successful migration of 98 existing policies
  - Dropdown UI next to Transaction Type

### Changed
- Date format standardization to MM/DD/YYYY
- Edit Policy Modal field reorganization
- Table display dynamic height calculation
- Documentation consolidation (9 files → 1 comprehensive guide)

### Fixed
- Date format display issues causing StreamlitAPIException
- Edit Policy Transactions showing excessive blank rows
- Renewal calculations using incorrect default terms

## [3.2.0] - 2025-07-08

### Added
- Broker fees and taxes implementation
- Premium reorganization with Commissionable Premium
- Field label standardization
- Calculate buttons for pre-save validation

### Changed
- Form sections reorganized for clarity
- Consolidated duplicate and confusing fields
- Improved calculation accuracy

## [3.1.0] - 2025-07-07

### Added
- Comprehensive formula documentation
- Enhanced UI/UX standards
- Improved error messaging

## [3.0.0] - 2025-07-06

### Added
- Complete Phase 0-2 formula implementation
- Double-entry reconciliation system
- Policy Revenue Ledger
- Security system with password protection

### Changed
- Complete application architecture overhaul
- Migration from CSV to Supabase database

## [2.0.0] - 2025-06-15

### Added
- Multi-user support
- Real-time data synchronization
- Advanced reporting features

## [1.0.0] - 2025-05-01

### Added
- Initial release
- Basic commission tracking
- CSV data storage
- Simple reporting

---

*For detailed version history and technical implementation details, see [PROJECT_HISTORY.md](docs/core/PROJECT_HISTORY.md)*