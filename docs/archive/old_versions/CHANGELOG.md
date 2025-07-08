# Sales Commission Management Application - CHANGELOG

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.6.0] - 2025-07-05 (Evening Update)

### Added
- **Statement Import Enhancements** - Major improvements to reconciliation workflow
  - **Column Mapping Persistence** - Save and load column mappings for repeated imports
    - Named mappings (e.g., "ABC Insurance Statement")
    - Validation when loading to ensure columns exist
    - Delete unwanted mappings
  - **Statement Total Verification** - Check-and-balance feature
    - Automatically detects and uses totals row from statements
    - Shows statement total vs reconciliation total
    - Visual indicators for perfect balance or discrepancies
  - **Enhanced Name Matching** - Handles real-world variations
    - First word matching: "Barboun" → "Barboun, Thomas"
    - Business name normalization: "RCM Construction" → "RCM Construction of SWFL LLC"
    - Interactive selection when multiple matches exist

### Changed
- **Dual-Purpose Reconciliation Clarification** - Fundamental shift in understanding
  - PRIMARY: Reconcile agent's commission payments (what YOU receive)
  - SECONDARY: Track agency's gross commission (for audit verification)
  - Agent Paid Amount (STMT) now primary required field
  - Agency Comm Received (STMT) now required for audit trail
  - All totals and displays updated to show agent amounts primarily
- **Totals Row Handling** - Skip matching but use for verification
  - Automatically skips rows with "total", "subtotal", etc. in customer name
  - Extracts total value for check-and-balance display
  - Prevents false matches on summary rows

### Fixed
- **Transaction Lookup in Import** - Resolved critical matching issue
  - Import now uses same balance calculation as Unreconciled Transactions tab
  - Eliminated stale data and lookup mismatches
  - Fixed "can't find transaction even with exact match" problem
- **Import Display** - Removed duplicate field descriptions
- **Session State Cleanup** - Clear statement totals after import

### Technical Notes
- Created `calculate_transaction_balances()` shared function for consistency
- Added `find_potential_customer_matches()` for intelligent name matching
- Implemented `normalize_business_name()` for business entity handling

## [3.5.0] - 2025-07-05

### Added
- **Reconciliation System - Complete Implementation** - Double-entry accounting for commission tracking
  - Balance-based transaction visibility (shows until fully reconciled to $0)
  - Drill-down selection: Customer → Policy Type → Policy Number → Effective Date
  - Batch reconciliation requiring exact statement total match
  - Special transaction IDs with suffixes (-STMT-, -VOID-, -ADJ-)
  - Void functionality to reverse entire reconciliation batches
  - Adjustment entries for error corrections
  - Full transaction history with payment tracking
  - Batch integrity checks and validation
- **Formulas & Calculations Tab** - New Admin Panel feature
  - Documents all calculated fields and their formulas
  - Shows relationships between fields
  - Provides transparency for commission calculations
- **Row Level Security (RLS)** - Enhanced database security
  - Enabled on all tables: policies, deleted_policies, manual_commission_entries
  - Restricts data access at database level
  - Works alongside application-level password protection

### Changed
- **Date Format Standardization** - All dates now display as MM/DD/YYYY
- **Removed Carrier Field** - Simplified reconciliation interface
- **Enhanced Reconciliation Display** - Shows full transaction details including all original fields

### Fixed
- **Transaction ID Generation** - Properly generates mixed alphanumeric IDs
- **Reconciliation Entry Creation** - Fixed transaction ID length validation
- **Batch Total Calculations** - Accurate decimal handling for statement matching

## [3.0.3] - 2025-07-04

### Added
- **Password Protection** - Implemented application-level security
  - Login screen requires password before accessing any data
  - Password stored securely in environment variables
  - Session-based authentication with logout functionality
  - Prevents unauthorized access to sensitive commission data
- **Form-Based Transaction Editor** - New reliable editing interface
  - "Edit Selected Transaction" button next to "Add New Transaction"
  - Modal-style form for single transaction editing
  - Organized fields by category (Client, Policy, Dates, Commission, Status)
  - Proper field types (date pickers, number inputs, checkboxes)
  - Tab-friendly navigation without screen jumping
- **Auto-Save Enhancement** - Improved data editor experience
  - Auto-save toggle in Edit Policies interface
  - Real-time saving of individual cell changes
  - Status indicators showing save progress
  - No page refresh on save (maintains scroll position)

### Fixed
- **Session State Password Error** - Fixed "KeyError: 'st.session_state has no key password'"
  - Added check for password key existence before access
  - Prevents crash when session state is corrupted
- **Edit Form Save Issues** - Form changes now properly save to database
  - Fixed partial field updates by including all fields in update
  - Added verification step to confirm saves
  - Improved error handling and debug messages
- **UI Elements Disappearing** - Fixed missing buttons and editing tips
  - Resolved Streamlit form variable scope issues
  - Fixed conditional rendering logic
  - Restored proper page structure

### Enhanced
- **Editing Tips Updated** - Clear guidance on two editing methods
  - Explains table editing with auto-save (quick but can be interrupted)
  - Recommends form editing for reliability
  - Notes about full-screen mode benefits
- **Security Documentation** - Updated SECURITY_IMPLEMENTATION.md
  - Marked Phase 1 (password protection) as complete
  - Updated security status and vulnerabilities
  - Added deployment instructions for secure environments

### Technical
- **Environment Variables** - Added APP_PASSWORD to .env configuration
- **Streamlit Cloud Deployment** - Successfully deployed with:
  - openpyxl dependency added to requirements.txt
  - Environment secrets configured in TOML format
  - Production app running with full security

## [3.0.2] - 2025-07-03

### Fixed
- **Number Formatting Issues** - All numeric columns now properly display with 2 decimal places in:
  - Edit Policies in Database page (Premium Sold, Agency Revenue, etc.)
  - All Policies in Database page
  - Dashboard search results and recent activity
  - Search & Filter results
- **JSON Serialization Error** - Fixed "Object of type int64 is not JSON serializable" when deleting transactions
  - Properly converts numpy int64/float64 types using `.item()` method
  - Handles all numpy scalar types for JSON compatibility
- **Page Refresh After Deletion** - Deleted records now disappear immediately without manual refresh
  - Clears editor session state (`edit_policies_editor`) after deletion
  - Forces proper UI update with st.rerun()
- **Deletion History Restore Errors** - Fixed multiple issues:
  - "invalid input syntax for type integer" - converts float values like "184.0" to int
  - "Could not find 'customer_name' column" - excludes metadata columns from restore
  - Properly handles data type conversions during restoration

### Enhanced
- Added `st.column_config.NumberColumn` with `format="%.2f"` across all data displays
- Improved error handling for numpy type conversions
- Better session state management for data editors
- Cleaner restoration process that only restores actual policy data fields

## [3.0.1] - 2025-07-03

### Fixed
- **KeyError: 'st.session_state has no key "edit_policies_editor"'** - Added proper session state initialization in Edit Policies page
- **New rows disappearing when saving in Edit Policies** - Implemented manual "Add New Transaction" button as workaround for Streamlit data_editor limitation
- **Edit creating duplicates instead of updating original transactions** - Fixed UPDATE logic to properly modify existing records
- **Delete functionality selecting wrong rows** - Rewrote delete logic to use checkbox selection instead of row indices
- **Transaction ID auto-generation** - Now generates IDs only on save, not when clicking "+"
- **Duplicate Transaction IDs issue** - Ensured unique ID generation with validation
- **Number formatting** - All currency fields now consistently show 2 decimal places
- **Client ID consistency** - All new transactions under a client now receive the same Client ID in Edit Policies

### Added
- **Deletion History with Restore Capability** - New tab in Admin Panel to view, restore, or permanently delete archived records
- **Manual Commission Entries Table** - Created `manual_commission_entries` table for reconciliation tracking
- **Double-Entry Accounting Documentation** - Updated APP_ARCHITECTURE.md with comprehensive accounting system explanation

### Changed
- **Database Column Update** - Changed column name from "(AZ)" to "(CRM)" throughout the application
- **Project Organization** - Reorganized files into dedicated folders:
  - `app_backups/` - All timestamped backups
  - `sql_scripts/` - SQL schemas and migrations
  - `migration_scripts/` - Database migration tools
  - `utility_scripts/` - Fix scripts and utilities
  - `archive/` - Old versions and deprecated files
  - `config_files/` - Configuration files
  - `logs_and_temp/` - Log and temporary files

### Enhanced
- **Add New Policy Transaction Page** - Redesigned with specific field order and improved UX
- **Error Handling** - Better user feedback for database operations
- **Performance** - Optimized queries and caching for faster response times

## [3.0.0] - 2025-07-03

### Added
- **Supabase Cloud Migration** - Complete migration from SQLite to PostgreSQL
- **Cloud Infrastructure** - 24/7 online availability with automated backups
- **Enhanced Security** - Proper credential management with environment variables
- **Deletion Archive System** - Soft delete functionality with recovery options

### Changed
- **Database Engine** - From SQLAlchemy/SQLite to Supabase API/PostgreSQL
- **Data Operations** - All SQL operations converted to Supabase API calls
- **Configuration** - Added `.env` support for secure credential storage

### Fixed
- **Syntax Errors** - Resolved all 263+ syntax and indentation issues
- **Navigation System** - Fixed duplicate menu entries
- **Import Statements** - Added missing UUID import
- **Cache Management** - Proper cache clearing after database operations

## [2.1.1] - 2025-01-28

### Added
- **Automatic Database Backups** - Timestamped backup creation
- **Backup Logging** - JSON log file to track backup operations

### Fixed
- **Navigation Conflicts** - Resolved Streamlit auto-navigation issues
- **Import Errors** - Fixed missing import statements

## [2.1.0] - 2025-07-02

### Added
- **Excel Import/Export** - Complete Excel support alongside CSV
- **Multi-Sheet Workbooks** - Export with metadata and summary sheets
- **File Type Detection** - Automatic detection of CSV, XLSX, and XLS
- **Import Validation** - Comprehensive data validation before import

### Enhanced
- **Export Formatting** - Professional Excel formatting with headers and styling
- **Preview Feature** - 10-row preview before import
- **Error Reporting** - Detailed validation messages

## [2.0.0] - 2025-07-02

### Changed
- **Architecture** - Complete transformation from monolithic to modular
- **Code Organization** - Reduced from 6000+ to 2700 clean lines
- **File Structure** - Organized into pages/ and utils/ directories

### Added
- **13 Complete Pages** - All features fully functional
- **Performance Optimization** - Caching system implementation
- **Error Handling** - Comprehensive error management
- **Security Enhancements** - Parameterized queries and input validation

### Fixed
- **Code Duplication** - Removed all duplicate blocks
- **Scope Issues** - Fixed all variable scope problems
- **DateTime Errors** - Resolved export timestamp issues

## [1.0.0] - 2025-06-28

### Initial Release
- Basic commission tracking functionality
- SQLite database storage
- Streamlit web interface
- Core CRUD operations
- Basic reporting capabilities

---

*For detailed technical information about fixes and implementations, see APP_ISSUES_AND_FIXES.md*