# Sales Commission App

A comprehensive commission tracking and reconciliation system built with Python and Streamlit.

**Version**: 3.5.1  
**Last Updated**: July 10, 2025

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

## Recent Updates (v3.5.1)

### New Features
- Enhanced Pending Renewals filtering - renewed policies auto-hide
- Page-specific data loading for fresh information
- Improved data synchronization between pages

### Bug Fixes
- Fixed NEW transactions displaying as "RWL" in Pending Renewals
- Resolved stale data issues after edits
- Corrected multiple syntax errors and indentation problems
- Fixed empty dataset handling

### Previous Updates (v3.5.0)
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