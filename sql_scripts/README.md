# SQL Scripts Organization

This directory contains essential SQL scripts for the Sales Commissions App database.

## Main Directory Contents

### Schema Files
- `schema.sql` - Current database schema
- `schema_export.sql` - Schema export format

### Table Creation Scripts
- `create_users_table.sql` - User management table
- `create_commission_structure_tables.sql` - Commission rules and structure
- `create_deleted_policies_table_v2.sql` - Soft delete functionality
- `create_manual_commission_entries_table.sql` - Manual commission entries
- `create_password_reset_tokens.sql` - Password reset functionality
- `create_simple_commission_payments.sql` - Commission payment tracking

### Migration Scripts
- `FINAL_migrate_to_user_id_system.sql` - User ID system migration
- `migrate_to_user_id_system.sql` - Base migration script
- `migration_step1_create_users.sql` through `migration_step5_create_indexes.sql` - Step-by-step migration
- `migration_helper.sql` - Migration utilities

### Column Addition Scripts
- `add_mga_name_column.sql` - MGA name column
- `add_policy_term_column.sql` - Policy term tracking
- `add_commission_integration_columns.sql` - Commission integration fields
- `add_effective_dates_to_commission_rules.sql` - Date-based commission rules
- `add_missing_commission_payments_columns.sql` - Additional payment fields
- `add_subscription_tiers.sql` - Subscription tier support

### Utilities
- `generate_batch_update_commands.sql` - Batch update generator
- `update_policy_term_constraint_for_custom.sql` - Policy term constraint updates

## Archive Directory Structure

### `/archive/duplicate_fixes/`
Contains all duplicate removal and cleanup scripts from January 2025

### `/archive/temp_debug/`
Temporary debugging and investigation scripts

### `/archive/data_analysis/`
Data analysis and verification scripts

### `/archive/old_migrations/`
Previous migration scripts and column renames

### `/archive/schemas/`
Previous versions of schema files

### `/archive/exports/`
Export and import related scripts

### `/archive/tests/`
Test SQL scripts

### `/archive/carrier_mga_fixes/`
Carrier and MGA relationship fixes

### `/archive/backups_and_checks/`
Backup and verification scripts

### `/archive/security/`
Security and RLS (Row Level Security) related scripts

### `/archive/demo_fixes/`
Demo environment specific fixes

### `/archive/rls_fixes/`
Row Level Security policy fixes

### `/archive/migration/`
Older migration scripts

### `/archive/debug/`
Various debugging scripts

### `/archive/docs/`
SQL-related documentation

## Usage Guidelines

1. **Production Scripts**: Only scripts in the main directory should be used for production
2. **Archive Access**: Archive scripts are for reference only - verify before using
3. **Naming Convention**: New scripts should follow the pattern: `action_target_description.sql`
4. **Documentation**: Update this README when adding new categories or important scripts