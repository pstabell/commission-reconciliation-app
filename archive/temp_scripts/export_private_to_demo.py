"""
Export carriers, MGAs, and commission rules from private SQLite database
and generate SQL insert statements for demo account in production.
"""
import sqlite3
import os
from datetime import datetime

# Path to your private database
DB_PATH = "commissions.db"

def export_private_data():
    """Export data from private SQLite database as SQL insert statements."""
    
    if not os.path.exists(DB_PATH):
        print(f"Error: Database {DB_PATH} not found!")
        return
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"demo_data_import_{timestamp}.sql"
    
    with open(output_file, 'w') as f:
        # Header
        f.write("-- IMPORT DATA FOR DEMO ACCOUNT\n")
        f.write(f"-- Generated from private database on {datetime.now()}\n")
        f.write("-- Run this in Supabase SQL Editor\n\n")
        
        # Delete existing demo data
        f.write("-- Step 1: Delete existing demo data\n")
        f.write("DELETE FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com';\n")
        f.write("DELETE FROM carrier_mga_relationships WHERE user_email = 'Demo@AgentCommissionTracker.com';\n")
        f.write("DELETE FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com';\n")
        f.write("DELETE FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com';\n\n")
        
        # Export carriers
        f.write("-- Step 2: Insert carriers\n")
        cursor.execute("SELECT * FROM carriers ORDER BY carrier_name")
        carriers = cursor.fetchall()
        
        for carrier in carriers:
            carrier_name = carrier['carrier_name'].replace("'", "''")
            naic_code = f"'{carrier['naic_code'].replace("'", "''")}'" if carrier['naic_code'] else 'NULL'
            producer_code = f"'{carrier['producer_code'].replace("'", "''")}'" if carrier['producer_code'] else 'NULL'
            status = carrier['status'] or 'Active'
            notes = f"'{carrier['notes'].replace("'", "''")}'" if carrier['notes'] else 'NULL'
            
            f.write(f"INSERT INTO carriers (carrier_name, naic_code, producer_code, status, notes, user_email) VALUES ('{carrier_name}', {naic_code}, {producer_code}, '{status}', {notes}, 'Demo@AgentCommissionTracker.com');\n")
        
        f.write(f"\n-- Total carriers: {len(carriers)}\n\n")
        
        # Export MGAs
        f.write("-- Step 3: Insert MGAs\n")
        cursor.execute("SELECT * FROM mgas ORDER BY mga_name")
        mgas = cursor.fetchall()
        
        for mga in mgas:
            mga_name = mga['mga_name'].replace("'", "''")
            status = mga['status'] or 'Active'
            notes = f"'{mga['notes'].replace("'", "''")}'" if mga['notes'] else 'NULL'
            
            f.write(f"INSERT INTO mgas (mga_name, status, notes, user_email) VALUES ('{mga_name}', '{status}', {notes}, 'Demo@AgentCommissionTracker.com');\n")
        
        f.write(f"\n-- Total MGAs: {len(mgas)}\n\n")
        
        # Create a mapping for commission rules
        f.write("-- Step 4: Insert commission rules (using name lookups)\n")
        cursor.execute("""
            SELECT 
                cr.*,
                c.carrier_name,
                m.mga_name
            FROM commission_rules cr
            JOIN carriers c ON cr.carrier_id = c.carrier_id
            LEFT JOIN mgas m ON cr.mga_id = m.mga_id
            ORDER BY c.carrier_name, m.mga_name
        """)
        rules = cursor.fetchall()
        
        for rule in rules:
            carrier_lookup = f"(SELECT carrier_id FROM carriers WHERE carrier_name = '{rule['carrier_name'].replace("'", "''")}' AND user_email = 'Demo@AgentCommissionTracker.com')"
            mga_lookup = f"(SELECT mga_id FROM mgas WHERE mga_name = '{rule['mga_name'].replace("'", "''")}' AND user_email = 'Demo@AgentCommissionTracker.com')" if rule['mga_name'] else 'NULL'
            policy_type = f"'{rule['policy_type']}'" if rule['policy_type'] else 'NULL'
            payment_terms = f"'{rule['payment_terms']}'" if rule['payment_terms'] else 'NULL'
            rule_desc = f"'{rule['rule_description'].replace("'", "''")}'" if rule['rule_description'] else 'NULL'
            renewal_rate = rule['renewal_rate'] if rule['renewal_rate'] is not None else 'NULL'
            
            f.write(f"INSERT INTO commission_rules (carrier_id, mga_id, policy_type, new_rate, renewal_rate, payment_terms, rule_description, user_email) VALUES ({carrier_lookup}, {mga_lookup}, {policy_type}, {rule['new_rate']}, {renewal_rate}, {payment_terms}, {rule_desc}, 'Demo@AgentCommissionTracker.com');\n")
        
        f.write(f"\n-- Total commission rules: {len(rules)}\n\n")
        
        # Final verification
        f.write("-- Step 5: Verify import\n")
        f.write("SELECT 'Import complete!' as status;\n")
        f.write("SELECT 'Carriers: ' || COUNT(*) as imported FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com'\n")
        f.write("UNION ALL\n")
        f.write("SELECT 'MGAs: ' || COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com'\n")
        f.write("UNION ALL\n")
        f.write("SELECT 'Commission Rules: ' || COUNT(*) FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com';\n")
    
    conn.close()
    print(f"✅ Export complete! SQL file created: {output_file}")
    print(f"📋 Copy the contents of {output_file} and run in Supabase SQL Editor")

if __name__ == "__main__":
    export_private_data()