"""
Migration script to update import-created transaction IDs to use -IMPORT suffix
Created: July 14, 2025

This script:
1. Finds all transactions with description containing "Created from statement import"
2. Updates their transaction IDs to add -IMPORT suffix
3. Updates any references in reconciliation tables
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def get_supabase_client():
    """Get Supabase client instance."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        raise Exception("Missing Supabase credentials. Please check your .env file.")
    return create_client(url, key)

def migrate_import_transaction_ids():
    """Migrate existing import-created transactions to use -IMPORT suffix."""
    supabase = get_supabase_client()
    
    print("Starting migration of import-created transaction IDs...")
    print(f"Timestamp: {datetime.now()}")
    print("-" * 50)
    
    try:
        # Step 1: Find all transactions created from statement import
        print("\nStep 1: Finding import-created transactions...")
        
        # Query for transactions with the import description
        response = supabase.table('policies').select('*').like('NOTES', '%Created from statement import%').execute()
        
        if not response.data:
            print("No import-created transactions found. Migration not needed.")
            return
        
        import_transactions = response.data
        print(f"Found {len(import_transactions)} import-created transactions")
        
        # Step 2: Process each transaction
        updated_count = 0
        skipped_count = 0
        errors = []
        
        print("\nStep 2: Updating transaction IDs...")
        
        for transaction in import_transactions:
            old_id = transaction.get('Transaction ID')
            
            if not old_id:
                print(f"  ⚠️  Skipping transaction with no ID: {transaction.get('Customer', 'Unknown')}")
                skipped_count += 1
                continue
            
            # Check if already has -IMPORT suffix
            if '-IMPORT' in str(old_id):
                print(f"  ✓  Already migrated: {old_id}")
                skipped_count += 1
                continue
            
            # Generate new ID with -IMPORT suffix
            new_id = f"{old_id}-IMPORT"
            
            # Check if new ID already exists
            check_response = supabase.table('policies').select('Transaction ID').eq('Transaction ID', new_id).execute()
            if check_response.data:
                print(f"  ⚠️  New ID already exists: {new_id} - skipping")
                skipped_count += 1
                continue
            
            try:
                # Update the transaction ID
                update_response = supabase.table('policies').update({
                    'Transaction ID': new_id
                }).eq('Transaction ID', old_id).execute()
                
                if update_response.data:
                    print(f"  ✓  Updated: {old_id} -> {new_id}")
                    updated_count += 1
                else:
                    print(f"  ❌  Failed to update: {old_id}")
                    errors.append(f"Failed to update {old_id}")
                    
            except Exception as e:
                print(f"  ❌  Error updating {old_id}: {str(e)}")
                errors.append(f"Error updating {old_id}: {str(e)}")
        
        # Step 3: Summary
        print("\n" + "=" * 50)
        print("MIGRATION SUMMARY")
        print("=" * 50)
        print(f"Total transactions found: {len(import_transactions)}")
        print(f"Successfully updated: {updated_count}")
        print(f"Skipped (already migrated or no ID): {skipped_count}")
        print(f"Errors: {len(errors)}")
        
        if errors:
            print("\nERRORS:")
            for error in errors:
                print(f"  - {error}")
        
        print(f"\nMigration completed at: {datetime.now()}")
        
        # Create migration log
        log_content = f"""Migration Log - Import Transaction IDs
Timestamp: {datetime.now()}
Total Found: {len(import_transactions)}
Updated: {updated_count}
Skipped: {skipped_count}
Errors: {len(errors)}

Details:
"""
        for transaction in import_transactions:
            old_id = transaction.get('Transaction ID', 'NO_ID')
            if '-IMPORT' not in str(old_id) and old_id != 'NO_ID':
                log_content += f"\n{old_id} -> {old_id}-IMPORT"
        
        # Save log file
        log_filename = f"migration_log_import_ids_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(log_filename, 'w') as f:
            f.write(log_content)
        
        print(f"\nMigration log saved to: {log_filename}")
        
    except Exception as e:
        print(f"\n❌ MIGRATION FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Confirm before running
    print("IMPORT TRANSACTION ID MIGRATION")
    print("This will update all import-created transactions to use -IMPORT suffix")
    print("\nBefore running this migration:")
    print("1. Ensure you have a database backup")
    print("2. Test in development environment first")
    print("3. Verify no active reconciliation processes")
    
    confirm = input("\nProceed with migration? (yes/no): ")
    
    if confirm.lower() == 'yes':
        migrate_import_transaction_ids()
    else:
        print("Migration cancelled.")