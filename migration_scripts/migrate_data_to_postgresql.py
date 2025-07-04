"""
SQLite to PostgreSQL Data Migration Script
This script converts SQLite data export to PostgreSQL-compatible format
"""

import re
from datetime import datetime

def convert_sqlite_to_postgresql(input_file='commissions_export.sql', output_file='commissions_postgresql_data.sql'):
    """Convert SQLite dump to PostgreSQL format"""
    
    with open(input_file, 'r') as f:
        sqlite_dump = f.read()
    
    # Start PostgreSQL script
    postgresql_script = []
    postgresql_script.append("-- PostgreSQL data migration from SQLite")
    postgresql_script.append("-- Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    postgresql_script.append("")
    postgresql_script.append("-- Disable foreign key checks during import")
    postgresql_script.append("SET session_replication_role = 'replica';")
    postgresql_script.append("")
    
    # Extract and convert INSERT statements for policies table
    policies_pattern = r"INSERT INTO policies VALUES\((.*?)\);"
    policies_matches = re.findall(policies_pattern, sqlite_dump, re.DOTALL)
    
    if policies_matches:
        postgresql_script.append("-- Insert policies data")
        postgresql_script.append("INSERT INTO policies (")
        postgresql_script.append("    client_id, transaction_id, customer, carrier_name, policy_type,")
        postgresql_script.append("    policy_number, transaction_type, agent_comm_rate,")
        postgresql_script.append("    policy_origination_date, effective_date, expiration_date,")
        postgresql_script.append("    new_biz_checklist_complete, premium_sold, policy_gross_comm_percent,")
        postgresql_script.append("    stmt_date, agency_estimated_comm_revenue, agency_gross_comm_received,")
        postgresql_script.append("    agent_estimated_comm, paid_amount, payment_type, notes")
        postgresql_script.append(") VALUES")
        
        values_list = []
        for match in policies_matches:
            # Parse values carefully
            values = match.strip()
            # Convert SQLite NULL to PostgreSQL NULL
            values = values.replace("'NULL'", "NULL")
            values = values.replace('""', "NULL")
            
            # Parse and reconstruct values in correct order
            # This is a simplified version - you may need to adjust based on actual data
            values_list.append(f"({values})")
        
        postgresql_script.append(",\n".join(values_list) + ";")
        postgresql_script.append("")
    
    # Extract and convert manual_commission_entries
    manual_pattern = r"INSERT INTO manual_commission_entries VALUES\((.*?)\);"
    manual_matches = re.findall(manual_pattern, sqlite_dump)
    
    if manual_matches:
        postgresql_script.append("-- Insert manual commission entries")
        postgresql_script.append("INSERT INTO manual_commission_entries (")
        postgresql_script.append("    customer, policy_type, policy_number, effective_date,")
        postgresql_script.append("    transaction_type, commission_paid, agency_commission_received,")
        postgresql_script.append("    statement_date, client_id, transaction_id")
        postgresql_script.append(") VALUES")
        
        values_list = []
        for match in manual_matches:
            # Skip the auto-increment ID (first value)
            values = match.strip()
            # Remove the first value (ID) from SQLite
            values_parts = values.split(',', 1)
            if len(values_parts) > 1:
                values = values_parts[1]
                values = values.replace("'NULL'", "NULL")
                values_list.append(f"({values})")
        
        postgresql_script.append(",\n".join(values_list) + ";")
        postgresql_script.append("")
    
    # Re-enable foreign key checks
    postgresql_script.append("-- Re-enable foreign key checks")
    postgresql_script.append("SET session_replication_role = 'origin';")
    postgresql_script.append("")
    
    # Update sequences
    postgresql_script.append("-- Update foreign key relationships")
    postgresql_script.append("-- This requires matching policy_id based on policy_number")
    postgresql_script.append("UPDATE commission_payments cp")
    postgresql_script.append("SET policy_id = p.id")
    postgresql_script.append("FROM policies p")
    postgresql_script.append("WHERE cp.policy_number = p.policy_number;")
    postgresql_script.append("")
    
    postgresql_script.append("-- Update renewal history foreign keys")
    postgresql_script.append("UPDATE renewal_history rh")
    postgresql_script.append("SET original_policy_id = p1.id,")
    postgresql_script.append("    new_policy_id = p2.id")
    postgresql_script.append("FROM policies p1, policies p2")
    postgresql_script.append("WHERE rh.original_transaction_id = p1.transaction_id")
    postgresql_script.append("AND rh.new_transaction_id = p2.transaction_id;")
    
    # Write output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(postgresql_script))
    
    print(f"PostgreSQL migration script created: {output_file}")
    print("\nNOTE: This is a basic conversion. You should:")
    print("1. Review the generated SQL for data type conversions")
    print("2. Handle date format conversions (mm/dd/yyyy to yyyy-mm-dd)")
    print("3. Map column names properly")
    print("4. Test with a small dataset first")

if __name__ == "__main__":
    convert_sqlite_to_postgresql()