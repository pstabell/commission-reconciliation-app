# Changelog

All notable changes to the Sales Commission App will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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