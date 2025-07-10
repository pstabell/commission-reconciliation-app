# Changelog

All notable changes to the Sales Commission App will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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