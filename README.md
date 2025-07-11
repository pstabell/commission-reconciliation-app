# Sales Commission App

A comprehensive commission tracking and reconciliation system built with Python and Streamlit.

**Version**: 3.5.13  
**Last Updated**: July 11, 2025

## Overview

The Sales Commission App is a powerful tool designed to track insurance policy commissions, automate calculations, and provide detailed reconciliation capabilities. It features a user-friendly interface, automated commission calculations, and comprehensive reporting.

## Key Features

### 🔄 Policy Renewal Tracking (v3.5.0)
- Complete audit trail with Prior Policy Number tracking
- Handles policy number changes (common in commercial surplus lines)
- Preserves original policy inception dates through renewals
- Automatic population of renewal data

### 📊 Automated Commission Calculations
- Formula-driven calculations for agency and agent commissions
- Support for different transaction types (NEW, RWL, END, etc.)
- Broker fee and tax calculations
- Real-time calculation updates

### 🔍 Advanced Reconciliation System
- Double-entry reconciliation with -STMT- transactions
- Protected reconciliation entries
- Detailed reconciliation reporting
- Statement import capabilities

### 📈 Comprehensive Reporting
- Policy Revenue Ledger with custom column selection
- Export to CSV and Excel
- Customizable report templates
- Financial summaries and analytics

### 🛡️ Security & Data Integrity
- Password-protected access
- Secure cloud database (Supabase)
- Automatic backups
- Transaction audit trails

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Environment-based password protection
- **State Management**: Streamlit session state

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pstabell/commission-reconciliation-app.git
cd commission-reconciliation-app
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file with:
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
APP_PASSWORD=your_app_password
```

5. Run database migrations:
```bash
# See migration_scripts/ directory for schema setup
```

6. Launch the application:
```bash
streamlit run commission_app.py
```

## Recent Updates (v3.5.13)

### Debug Mode & Enhanced Matching
- **Debug Mode**: New expandable section shows why transactions aren't available for matching
- **Balance Transparency**: Displays credit, debit, and balance calculations for each transaction
- **Improved Matching**: Enhanced fuzzy customer name matching handles variations better
- **Word-Based Matching**: "Adam Gomes" now matches "Gomes, Adam" or "Adam J. Gomes"

### Previous Updates (v3.5.12)
- **Void Screen Fix**: Corrected amounts display to show Agent commissions instead of Agency
- **Consistency**: All reconciliation screens now show the same commission amounts
- **Clarity**: Prevents confusion about which amounts are being voided

### Previous Updates (v3.5.11)
- **Error Handling**: Fixed KeyError for missing effective_date during reconciliation
- **Robustness**: System handles incomplete statement data gracefully

### Previous Updates (v3.5.10)
- **Manual Match Fixes**: Resolved KeyErrors when manually matching transactions
- **Endorsement Reminder**: Added helpful caption for creating new transactions

### Previous Updates (v3.5.9)
- **Manual Matching**: Added checkbox to force matches despite name mismatches
- **Repository Cleanup**: Organized all files into proper folder structure

### Previous Updates (v3.5.8)
- **Void Balance Fix**: Voided transactions now properly show as unreconciled
- **-VOID- Entry Support**: Balance calculation includes void reversals

### Previous Updates (v3.5.7)
- **Import Function Fix**: Resolved "all_data not defined" error during reconciliation

### Previous Updates (v3.5.6)

### Customer Name Consistency Fix
- **Fixed Reconciliation Import Issue**: Consistent customer naming when creating new transactions
- **Smart Name Matching**: Uses existing customer format instead of statement format
- **Prevents Duplicates**: No more "Ghosh, Susmit" vs "Susmit K. Ghosh" entries
- **Data Integrity**: Maintains consistent customer names across all transactions

### Previous Updates (v3.5.5)
- **Duplicate Transaction Fix**: Resolved duplicate creation when editing newly added transactions
- **Enhanced Modal Save Logic**: Now checks database for existing records before INSERT/UPDATE
- **Improved Data Integrity**: Prevents duplicates regardless of session state
- **Seamless Workflow**: Add inline → Edit immediately without creating duplicates

### Previous Updates (v3.5.4)
- **Void Visibility Enhancement**: Complete reconciliation status tracking
- **Enhanced History Views**: Added Status, Void ID, and Void Date columns
- **Visual Indicators**: Color coding for voided batches and void entries
- **Fixed Void Transaction Filter**: Now includes both -STMT- and -VOID- transactions

### Previous Updates (v3.5.3)
- **Critical Fix**: Resolved StreamlitDuplicateElementKey error
- **Code Consolidation**: Removed 657 lines of duplicate form code
- **Improved Stability**: Added field tracking to prevent conflicts

### Previous Updates (v3.5.2)
- Complete Cancel/Rewrite workflow implementation
- Enhanced UI with blue Calculate buttons and info reminders
- Prior Policy Number field in Add New Policy form
- Comprehensive Cancel/Rewrite documentation in Help page

### Previous Updates (v3.5.1)
- Policy renewal tracking with Prior Policy Number
- Complete audit trails for policy chains
- Enhanced UI field ordering
- Column renaming for consistency

## Documentation

Comprehensive documentation is available in the `/docs` directory:

- **[Project History](docs/core/PROJECT_HISTORY.md)** - Complete development timeline
- **[Architecture](docs/core/APP_ARCHITECTURE.md)** - Technical architecture details
- **[Next Steps](docs/core/NEXT_STEPS.md)** - Current status and roadmap
- **[Formula System](docs/features/FORMULA_SYSTEM.md)** - Commission calculation logic
- **[Reconciliation](docs/features/RECONCILIATION_SYSTEM.md)** - Reconciliation features

## Quick Start Guide

1. **Login**: Enter the application password
2. **Dashboard**: View commission summaries and recent activity
3. **Add Policy**: Use "Add New Policy Transaction" for new entries
4. **Edit Policies**: Search and edit existing policies
5. **Reconciliation**: Import statements and reconcile commissions
6. **Reports**: Generate various reports and exports

## Support

- **Issues**: Report bugs via [GitHub Issues](https://github.com/pstabell/commission-reconciliation-app/issues)
- **Documentation**: See `/docs` directory
- **AI Development**: See [CLAUDE.md](CLAUDE.md) for AI assistant guidelines

## License

Proprietary - All rights reserved

## Contributors

- **Patrick Stabell** - Primary Developer
- **Claude (Anthropic)** - Development Assistant

---

*For detailed technical documentation, see the `/docs` directory.*