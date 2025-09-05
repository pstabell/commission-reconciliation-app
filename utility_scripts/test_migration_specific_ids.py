"""
Test migration script for specific transaction IDs
Created: July 14, 2025

This script tests the migration on 5 specific transaction IDs.
"""

import streamlit as st
from commission_app import get_supabase_client
from datetime import datetime

def test_migration_specific_ids():
    """Test migration on specific transaction IDs."""
    
    # Test transaction IDs
    test_ids = ['D5D19K7', '0POM131', '5XVX2F0', 'S98EB28', 'XRZ581P']
    
    print("Testing migration on specific transaction IDs...")
    print(f"Timestamp: {datetime.now()}")
    print("-" * 50)
    
    try:
        supabase = get_supabase_client()
        
        # Step 1: Check each transaction
        print("\nStep 1: Checking transactions...")
        print("-" * 50)
        
        for tid in test_ids:
            print(f"\nChecking {tid}:")
            
            # Get transaction details
            response = supabase.table('policies').select('*').eq('Transaction ID', tid).execute()
            
            if not response.data:
                print(f"  ❌ NOT FOUND")
                continue
            
            transaction = response.data[0]
            customer = transaction.get('Customer', 'Unknown')
            notes = transaction.get('NOTES', '')
            is_import = 'Created from statement import' in str(notes)
            
            print(f"  Customer: {customer}")
            print(f"  Is Import Transaction: {'Yes' if is_import else 'No'}")
            
            if not is_import:
                print(f"  ⚠️  Not an import transaction - skipping")
                continue
            
            # Check if already migrated
            if '-IMPORT' in tid:
                print(f"  ✓  Already migrated")
                continue
            
            # Generate new ID
            new_id = f"{tid}-IMPORT"
            
            # Check if new ID exists
            check_response = supabase.table('policies').select('Transaction ID').eq('Transaction ID', new_id).execute()
            if check_response.data:
                print(f"  ⚠️  New ID {new_id} already exists - skipping")
                continue
            
            print(f"  🔄 Would migrate: {tid} -> {new_id}")
        
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        
        # Step 2: Ask for confirmation
        confirm = input("\nProceed with actual migration of these transactions? (yes/no): ")
        
        if confirm.lower() != 'yes':
            print("Migration cancelled.")
            return
        
        # Step 3: Perform actual migration
        print("\nStep 3: Performing migration...")
        print("-" * 50)
        
        migrated_count = 0
        errors = []
        
        for tid in test_ids:
            # Get transaction again
            response = supabase.table('policies').select('*').eq('Transaction ID', tid).execute()
            
            if not response.data:
                continue
            
            transaction = response.data[0]
            notes = transaction.get('NOTES', '')
            
            # Skip non-import transactions
            if 'Created from statement import' not in str(notes):
                continue
            
            # Skip already migrated
            if '-IMPORT' in tid:
                continue
            
            new_id = f"{tid}-IMPORT"
            
            # Check if new ID exists
            check_response = supabase.table('policies').select('Transaction ID').eq('Transaction ID', new_id).execute()
            if check_response.data:
                continue
            
            try:
                # Update the transaction ID
                update_response = supabase.table('policies').update({
                    'Transaction ID': new_id
                }).eq('Transaction ID', tid).execute()
                
                if update_response.data:
                    print(f"  ✓  Migrated: {tid} -> {new_id}")
                    migrated_count += 1
                else:
                    print(f"  ❌  Failed to update: {tid}")
                    errors.append(f"Failed to update {tid}")
                    
            except Exception as e:
                print(f"  ❌  Error updating {tid}: {str(e)}")
                errors.append(f"Error updating {tid}: {str(e)}")
        
        print("\n" + "=" * 50)
        print("MIGRATION COMPLETE")
        print("=" * 50)
        print(f"Successfully migrated: {migrated_count}")
        print(f"Errors: {len(errors)}")
        
        if errors:
            print("\nERRORS:")
            for error in errors:
                print(f"  - {error}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_migration_specific_ids()