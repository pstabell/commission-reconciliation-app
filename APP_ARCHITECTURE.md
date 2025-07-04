# Application Architecture Overview

This document provides a high-level overview of the Sales Commission Tracker application's architecture, key components, and data flow. It serves as a master plan to maintain clarity and understanding of the system's design.

## Current Architecture (Monolithic)

The application currently uses a monolithic structure with all functionality contained in a single file. This approach provides simplicity and ease of deployment while maintaining full functionality.

### Main Components:

*   **Frontend (UI):** Built with Streamlit (Python web framework).
    *   **Navigation:** Sidebar-based radio buttons for page selection.
    *   **Styling:** Custom CSS for consistent look and feel (yellow highlights for inputs, fixed sidebar).
    *   **Interactive Elements:** Data editors, text inputs, number inputs, date pickers, selectboxes, buttons.
    *   **Sortable Tables:** Utilizes `streamlit_sortables` for column reordering.

*   **Backend (Data & Logic):**
    *   **Database:** SQLite (`commissions.db`) for persistent storage.
    *   **ORM/DB Interaction:** SQLAlchemy for database operations (creating tables, inserting, updating, deleting data).
    *   **Data Processing:** Pandas for data manipulation, filtering, aggregation, and calculations.
    *   **File Handling:** `pdfplumber` for PDF parsing, `pandas` for Excel/CSV reading/writing.
    *   **Logging:** Standard Python `logging` module for application events and errors.

*   **Core Logic & Utilities:**
    *   **Column Mapping (`column_mapping_config.py`):** Centralized system to map UI field names to actual database column names, ensuring flexibility and consistency. Includes functions for getting mapped names, checking calculated fields, and validating mappings.
    *   **Commission Calculation:** Functions to calculate agent commissions based on transaction type and other policy details.
    *   **ID Generation:** Helper functions for generating unique Client IDs and Transaction IDs.
    *   **Date & Currency Formatting:** Functions to standardize data display.
    *   **Pending Renewals Logic:** Functions to identify and prepare policies for renewal.

*   **Basic Database Management:**
    *   **Manual Backup/Restore:** Basic database download and upload functionality in Admin Panel.
    *   **File-based Backups:** Simple backup creation with timestamp naming.
    *   **Database Download:** Ability to download current database file for external backup.
    *   **Database Upload:** Ability to replace current database with uploaded file (with user confirmation).

### Key UI Pages / Modules:

*   **Dashboard:** Overview of data, client search, quick edit for client data.
*   **Add New Policy Transaction:** Form for entering new policy data, with client ID lookup and premium calculator.
*   **Reports:** Customizable reports with column selection, date/customer/balance filters, and export options.
*   **All Policies in Database:** Displays all raw policy data.
*   **Edit Policies in Database:** Allows bulk editing of policies with column reordering and formula protection.
*   **Search & Filter:** Advanced search capabilities across columns with balance due filtering.
*   **Admin Panel:** Central hub for column mapping, adding/deleting/renaming columns, and basic database backup/restore.
*   **Accounting:** Commission statement reconciliation (manual entry or file upload), payment history, and audit trail.
    *   **Important Design Decision:** Reconciliation adds NEW transactions rather than updating existing ones. This creates a proper double-entry accounting system where:
        - Original transactions = Credits (what you're owed)
        - Reconciliation transactions = Debits (what you've been paid)
        - Every transaction is preserved for complete audit trail
        - Multiple transactions per policy number are intentional (e.g., NEW, RWL, reconciliation payments)
        - This design enables tracking of commission lifecycle: earned → billed → paid
*   **Policy Revenue Ledger:** Detailed transaction-level view for individual policies, with editable ledger and running totals.
*   **Policy Revenue Ledger Reports:** Advanced reporting with policy aggregation, templates, pagination, and enhanced export.
*   **Pending Policy Renewals:** Identifies and manages policies due for renewal with date calculations and export functionality.
*   **Help:** Comprehensive documentation, troubleshooting, formulas, FAQ, data protection details, and development roadmap.

### Data Flow:

*   **Data Ingestion:** Manual entry via forms, file uploads (CSV, Excel, PDF) for policies and statements.
*   **Data Storage:** All primary application data resides in `commissions.db`.
*   **Data Processing:** Pandas DataFrames are used extensively for in-memory manipulation, filtering, and calculations before data is written back to the database.
*   **Data Output:** Reports (CSV, Excel), PDF printouts, and on-screen dataframes.
*   **Backup/Restore:** Basic database file copying for backups, with manual restore capability from Admin Panel.

### Key Design Principles:

*   **Data Integrity & Safety:** Basic data validation and standard database operations to maintain data consistency.
*   **Immutable Transaction History:** Original transactions are never modified. All updates (payments, reconciliations) create new transactions, preserving complete audit trail.
*   **Double-Entry Accounting:** System follows accounting principles where earned commissions (credits) and payments received (debits) are separate transactions.
*   **User Control:** Provides users with control over data, column mapping, and basic backup/restore options.
*   **Modularity:** Functions and components are organized (e.g., `column_mapping_config.py`) to promote reusability and maintainability.
*   **Clarity & Usability:** UI elements are designed for ease of use, with clear instructions and visual cues (e.g., yellow highlights).
*   **Simplicity:** Streamlined architecture focused on core functionality without complex protection systems.

---

## Future Enhancement: Bulletproof Modular Architecture

To improve maintainability, error isolation, and enable parallel development, the application can be refactored into a modular architecture where each page is completely isolated.

### Proposed Structure:

```
commission_app.py          # Main entry point (lightweight router)
pages/
  ├── __init__.py         # Package initialization
  ├── dashboard.py        # Dashboard page (isolated)
  ├── reports.py          # Reports page (isolated)
  ├── all_policies.py     # All Policies page (isolated)
  ├── add_policy.py       # Add New Policy page (isolated)
  ├── edit_policies.py    # Edit Policies page (isolated)
  ├── search_filter.py    # Search & Filter page (isolated)
  ├── admin_panel.py      # Admin Panel page (isolated)
  ├── accounting.py       # Accounting page (isolated)
  ├── help.py            # Help page (isolated)
  ├── policy_ledger.py    # Policy Revenue Ledger (isolated)
  ├── ledger_reports.py   # Policy Revenue Reports (isolated)
  └── renewals.py         # Pending Renewals (isolated)
utils/
  ├── __init__.py
  ├── database.py         # Database operations
  ├── formatting.py       # Data formatting functions
  ├── calculations.py     # Commission calculations
  └── validators.py       # Input validation
```

### Benefits of Modular Architecture:

#### **Error Isolation**
- **Bulletproof Design:** Failure in one page cannot crash other pages
- **Contained Errors:** Syntax errors, runtime exceptions, or logic issues are isolated to specific modules
- **Graceful Degradation:** App continues to function even if individual pages have issues

#### **Development Advantages**
- **Parallel Development:** Multiple developers can work on different pages simultaneously
- **Independent Testing:** Each page can be tested in isolation without affecting others
- **Easy Debugging:** Issues can be pinpointed to specific files immediately
- **Version Control Friendly:** Changes to one page don't create merge conflicts with other pages

#### **Maintainability**
- **Single Responsibility:** Each file has one clear purpose and function
- **Easy Navigation:** Developers can quickly find and modify specific functionality
- **Reduced Complexity:** Smaller files are easier to understand and maintain
- **Modular Updates:** Features can be updated independently without risk to other functionality

#### **Scalability**
- **Easy Feature Addition:** New pages can be added without modifying existing code
- **Component Reusability:** Shared utilities can be imported across pages
- **Performance Optimization:** Only required modules are loaded for each page
- **Team Scaling:** Multiple developers can work efficiently without stepping on each other

### Implementation Strategy:

1. **Phase 1: Extract Shared Utilities**
   - Move database functions to `utils/database.py`
   - Move formatting functions to `utils/formatting.py`
   - Move calculations to `utils/calculations.py`

2. **Phase 2: Create Page Modules**
   - Extract each page's logic into separate files
   - Standardize page function signatures: `def show_[page_name](all_data, engine)`
   - Implement error handling in each module

3. **Phase 3: Update Main Router**
   - Modify `commission_app.py` to import and call page modules
   - Implement error containment for page loading
   - Add fallback mechanisms for failed page loads

4. **Phase 4: Testing & Validation**
   - Test each page module independently
   - Verify error isolation works as expected
   - Confirm all functionality is preserved

### Current vs. Modular Comparison:

| Aspect | Current (Monolithic) | Proposed (Modular) |
|--------|---------------------|-------------------|
| File Structure | Single 2,700-line file | 18 organized modules |
| Error Isolation | ❌ One error affects all | ✅ Isolated failures |
| Maintainability | ⚠️ Large file to navigate | ✅ Easy to find/fix issues |
| Development | ⚠️ Merge conflicts likely | ✅ Parallel development |
| Testing | ❌ Must test entire app | ✅ Test individual pages |
| Debugging | ❌ Search through large file | ✅ Pinpoint exact location |
| Deployment | ✅ Single file simplicity | ⚠️ Multiple files to manage |
| Performance | ✅ All code pre-loaded | ✅ Load only needed code |

### Migration Considerations:

- **Backward Compatibility:** Ensure existing database and data remain unchanged
- **Feature Parity:** All current functionality must be preserved
- **User Experience:** No changes to user interface or workflow
- **Deployment:** Consider impact on deployment process and file management

---

## Recent Architecture Updates (July 2025)

### Cloud Migration
The application has been successfully migrated from local SQLite to Supabase PostgreSQL cloud database:
- **Database Engine:** Supabase PostgreSQL (replaced SQLite)
- **API Integration:** Supabase client API (replaced SQLAlchemy)
- **Connection Management:** Environment variables for secure credentials
- **Performance:** Improved with cloud infrastructure and caching

### Enhanced Data Management

#### Deletion Archive System
- **Soft Deletes:** Records moved to `deleted_policies` table instead of permanent deletion
- **Recovery Options:** Restore accidentally deleted records from Admin Panel
- **Audit Trail:** Complete history of deletions with timestamps
- **Cleanup Options:** Permanent deletion available when needed

#### Manual Commission Entries
- **New Table:** `manual_commission_entries` for reconciliation tracking
- **Separation of Concerns:** Original transactions remain untouched
- **Payment Tracking:** Records when commissions are actually paid
- **Reconciliation Support:** Enables matching earned vs paid commissions

### Transaction ID Management
- **Auto-Generation:** IDs created only on save (not on row creation)
- **Uniqueness Validation:** Checks against existing records
- **Format:** 7-character alphanumeric (A-Z, 0-9)
- **Client ID Consistency:** New rows inherit client's ID automatically

### UI/UX Improvements

#### Edit Policies Enhancement
- **Manual Add Button:** Replaces buggy Streamlit "+" button
- **Checkbox Selection:** For delete operations
- **Preview Changes:** Shows what will be saved/deleted
- **Bulk Operations:** Handle multiple records efficiently

#### Number Formatting
- **Currency Display:** Consistent 2 decimal places
- **Data Validation:** Ensures numeric fields are properly formatted
- **User Feedback:** Clear messages for all operations

### Project Structure Organization
```
SALES COMMISSIONS APP/
├── commission_app.py          # Main application
├── column_mapping_config.py   # Column configuration
├── .env                       # Environment variables (not in git)
├── requirements.txt           # Python dependencies
├── app_backups/              # All timestamped backups
├── sql_scripts/              # SQL schemas and migrations
│   ├── create_deleted_policies_table.sql
│   ├── create_manual_commission_entries.sql
│   └── [other SQL files]
├── migration_scripts/        # Database migration tools
├── utility_scripts/          # Fix scripts and utilities
├── archive/                  # Old versions and deprecated files
├── config_files/             # Configuration files
├── logs_and_temp/            # Log files and temporary files
└── help_content/             # Help documentation
```

### Security Enhancements
- **Environment Variables:** All sensitive data in `.env` file
- **Secure API Calls:** Using Supabase's built-in security
- **Input Validation:** Prevents SQL injection and data corruption
- **Access Control:** Ready for Row Level Security implementation

---

*Last Updated: July 3, 2025*