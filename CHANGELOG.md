# Sales Commission Management Application - CHANGELOG

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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