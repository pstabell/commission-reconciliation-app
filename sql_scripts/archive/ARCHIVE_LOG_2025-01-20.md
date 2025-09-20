# SQL Scripts Archive Log - January 20, 2025

## Summary
Organized SQL scripts by moving temporary, debug, and specialized scripts into appropriate archive folders, keeping only essential schema and migration scripts in the main sql_scripts directory.

## Files Moved from Root Directory to Archive

### To `/archive/duplicate_fixes/`
- analyze_all_duplicates.sql
- analyze_carefully.sql
- analyze_duplicates_fixed.sql
- check_creation_dates.sql
- check_dates_fixed.sql
- check_duplicate_timing.sql
- check_timing_fixed.sql
- clean_duplicates_now.sql
- clean_lee_hopper_duplicates.sql
- final_cleanup_to_425.sql
- find_true_duplicates.sql
- remove_exact_id_duplicates.sql
- remove_recent_duplicates_only.sql
- safe_duplicate_removal.sql
- verify_all_edits.sql
- remove_duplicates_sql.txt

### To `/archive/temp_scripts/`
- execute_duplicate_removal.py
- export_private_contacts.py
- minimal_webhook.py
- simple_webhook.py
- simple_webhook_debug.py

## Files Moved from sql_scripts to Archive

### To `/archive/temp_debug/`
- consolidate_demo_emails.sql
- consolidate_demo_emails_fixed.sql
- diagnose_demo_duplication.sql
- final_debug_carriers.sql
- investigate_110_extra_records.sql
- investigate_edit_bug.sql
- investigate_missing_41.sql
- investigate_missing_41_fixed.sql
- 0_check_*.sql files
- check_deleted_policies*.sql
- check_user_id_status.sql
- check_current_structure.sql
- generate_batch_update_commands.sql

### To `/archive/duplicate_fixes/`
- clean_katie_duplicates.sql
- clean_pinnacle_duplicates.sql
- deep_duplicate_cleanup.sql
- find_duplicate_policies.sql
- find_duplicate_policies_final.sql
- find_duplicate_policies_fixed.sql
- find_recent_duplicates.sql
- find_remaining_duplicates.sql
- remove_all_duplicates_safely.sql
- remove_duplicate_transactions.sql
- remove_true_duplicates.sql

### To `/archive/data_analysis/`
- analyze_425_policies.sql
- analyze_537_transactions.sql
- analyze_duplicates_fixed.sql
- check_duplication_pattern.sql
- check_email_cases_now.sql
- diagnose_app_query_issue.sql
- find_missing_41_transactions.sql
- find_missing_transactions_detailed.sql
- search_missing_41_final.sql
- verify_425_final.sql
- verify_all_policies_count.sql

### To `/archive/schemas/`
- schema_postgresql.sql
- schema_postgresql_debug.sql
- schema_postgresql_exact_match.sql
- schema_postgresql_safe.sql
- schema_postgresql_safe_corrected.sql

### To `/archive/tests/`
- test_*.sql files

### To `/archive/old_migrations/`
- 00_EXECUTE_THIS_*.sql files
- 6_reconciliation_system_migration.sql
- 8_check_transaction_id_constraints*.sql
- cleanup_and_simple_rename.sql
- rename_agency_gross_comm_column.sql
- update_column_az_to_crm.sql

### To `/archive/exports/`
- commissions_export.sql
- commissions_postgresql_data.sql
- simple_export_all_tables.sql
- supabase_import_steps.sql
- import_sqlite_to_postgresql.sql

### To `/archive/carrier_mga_fixes/`
- add_missing_burlington_burns*.sql
- add_missing_carrier_rules.sql
- also_add_burns_wilcox.sql
- insert_carriers_mgas_now.sql
- list_all_mgas_in_database.sql
- show_carriers_mgas_data.sql

### To `/archive/backups_and_checks/`
- backup_commission_structure.sql
- explore_deleted_policies.sql
- final_count_verification.sql
- find_all_policies_by_email.sql
- safe_check_data_exists.sql
- inspect_table_structures.sql
- verify_*.sql files

### To `/archive/security/`
- fortify_*.sql
- secure_all_operations.sql

### To `/archive/demo_fixes/`
- FINAL_DEMO_IMPORT_FROM_PRIVATE.sql

### To `/archive/docs/`
- clear_demo_session_cache_instructions.md

## Result
The main sql_scripts directory now contains 24 essential SQL files:
- Core schema files
- Table creation scripts
- Active migration scripts
- Column addition scripts

All temporary, debug, and specialized scripts are organized in clearly labeled archive subdirectories for reference.