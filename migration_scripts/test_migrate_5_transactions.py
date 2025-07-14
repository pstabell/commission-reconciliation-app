"""
Test migration script for 5 specific transaction IDs
Created: July 14, 2025

This tests the migration on these specific IDs:
- D5D19K7
- 0POM131
- 5XVX2F0
- S98EB28
- XRZ581P
"""

import os
import sys
from datetime import datetime

# Add parent directory to path to import from commission_app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required functions
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

def get_supabase_client():
    """Get Supabase client instance."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        raise Exception("Missing Supabase credentials. Please check your .env file.")
    return create_client(url, key)

def test_migration_on_5_transactions():
    """Test migration on 5 specific transactions."""
    
    # Specific transaction IDs to test
    test_ids = ['D5D19K7', '0POM131', '5XVX2F0', 'S98EB28', 'XRZ581P']
    
    supabase = get_supabase_client()
    
    print("TEST MIGRATION - 5 Specific Transactions")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print(f"Testing IDs: {', '.join(test_ids)}")
    print("-" * 50)
    
    # First, let's check the current state
    print("\nCURRENT STATE:")
    print("-" * 30)
    
    import_count = 0
    
    for tid in test_ids:
        try:
            response = supabase.table('policies').select('Transaction ID', 'Customer', 'NOTES').eq('Transaction ID', tid).execute()
            
            if response.data:
                transaction = response.data[0]
                customer = transaction.get('Customer', 'Unknown')
                notes = transaction.get('NOTES', '')
                is_import = 'Created from statement import' in str(notes)
                
                print(f"\n{tid}:")
                print(f"  Customer: {customer}")
                print(f"  Import transaction: {'YES' if is_import else 'NO'}")
                if is_import:
                    import_count += 1
                    print(f"  Notes: {notes[:60]}...")
            else:
                print(f"\n{tid}: NOT FOUND IN DATABASE")
                
        except Exception as e:
            print(f"\n{tid}: ERROR - {str(e)}")
    
    print(f"\n\nFound {import_count} import transactions out of {len(test_ids)} IDs checked.")
    
    if import_count == 0:
        print("\nNo import transactions found. Nothing to migrate.")
        return
    
    # Ask for confirmation
    print("\n" + "=" * 50)
    print("MIGRATION PREVIEW")
    print("=" * 50)
    print(f"This will update {import_count} transaction ID(s) to add -IMPORT suffix")
    print("Example: D5D19K7 -> D5D19K7-IMPORT")
    
    confirm = input("\nProceed with migration? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("\nMigration cancelled.")
        return
    
    # Perform migration
    print("\n" + "=" * 50)
    print("PERFORMING MIGRATION")
    print("=" * 50)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for tid in test_ids:
        try:
            # Get full transaction data
            response = supabase.table('policies').select('*').eq('Transaction ID', tid).execute()
            
            if not response.data:
                print(f"\n{tid}: SKIPPED - Not found")
                skip_count += 1
                continue
            
            transaction = response.data[0]
            notes = transaction.get('NOTES', '')
            
            # Check if it's an import transaction
            if 'Created from statement import' not in str(notes):
                print(f"\n{tid}: SKIPPED - Not an import transaction")
                skip_count += 1
                continue
            
            # Check if already migrated
            if '-IMPORT' in tid:
                print(f"\n{tid}: SKIPPED - Already has -IMPORT suffix")
                skip_count += 1
                continue
            
            # Generate new ID
            new_id = f"{tid}-IMPORT"
            
            # Check if new ID already exists
            check_response = supabase.table('policies').select('Transaction ID').eq('Transaction ID', new_id).execute()
            if check_response.data:
                print(f"\n{tid}: SKIPPED - {new_id} already exists")
                skip_count += 1
                continue
            
            # Perform update
            update_response = supabase.table('policies').update({
                'Transaction ID': new_id
            }).eq('Transaction ID', tid).execute()
            
            if update_response.data:
                print(f"\n{tid}: SUCCESS - Updated to {new_id}")
                success_count += 1
            else:
                print(f"\n{tid}: ERROR - Update failed")
                error_count += 1
                
        except Exception as e:
            print(f"\n{tid}: ERROR - {str(e)}")
            error_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("MIGRATION SUMMARY")
    print("=" * 50)
    print(f"Total processed: {len(test_ids)}")
    print(f"✓ Successfully migrated: {success_count}")
    print(f"⚠ Skipped: {skip_count}")
    print(f"✗ Errors: {error_count}")
    
    if success_count > 0:
        print("\nMigrated transaction IDs:")
        print("Check your application to verify these now show as -IMPORT transactions")
    
    print(f"\nCompleted at: {datetime.now()}")

if __name__ == "__main__":
    print("TEST MIGRATION SCRIPT - 5 Specific Transactions")
    print("This will update transaction IDs to add -IMPORT suffix")
    print("for import-created transactions only.")
    print()
    
    test_migration_on_5_transactions()