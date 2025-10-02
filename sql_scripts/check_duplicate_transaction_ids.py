#!/usr/bin/env python3
"""
Check for duplicate Transaction IDs in the database.
Run this before adding UNIQUE constraint to identify and fix duplicates.

Usage:
    python3 sql_scripts/check_duplicate_transaction_ids.py
"""

import os
import sys
from supabase import create_client, Client

def check_duplicates():
    """Check for duplicate Transaction IDs in the policies table."""

    # Get Supabase credentials from environment
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables must be set")
        sys.exit(1)

    # Create Supabase client
    supabase: Client = create_client(supabase_url, supabase_key)

    print("Checking for duplicate Transaction IDs...")
    print("=" * 80)

    try:
        # Query to find duplicates
        # Note: Supabase doesn't support GROUP BY with HAVING in select(),
        # so we fetch all and process in Python
        response = supabase.table('policies').select('"Transaction ID", _id').execute()

        if not response.data:
            print("No data found in policies table")
            return

        # Count occurrences of each Transaction ID
        transaction_id_counts = {}
        transaction_id_records = {}

        for record in response.data:
            transaction_id = record.get('Transaction ID')
            record_id = record.get('_id')

            if transaction_id:
                if transaction_id not in transaction_id_counts:
                    transaction_id_counts[transaction_id] = 0
                    transaction_id_records[transaction_id] = []

                transaction_id_counts[transaction_id] += 1
                transaction_id_records[transaction_id].append(record_id)

        # Find duplicates (Transaction IDs that appear more than once)
        duplicates = {tid: count for tid, count in transaction_id_counts.items() if count > 1}

        if not duplicates:
            print("✅ No duplicate Transaction IDs found!")
            print(f"\nTotal unique Transaction IDs: {len(transaction_id_counts)}")
            print("Database is ready for UNIQUE constraint.")
        else:
            print(f"⚠️  Found {len(duplicates)} duplicate Transaction IDs:")
            print()

            for transaction_id, count in sorted(duplicates.items(), key=lambda x: x[1], reverse=True):
                print(f"  Transaction ID: {transaction_id}")
                print(f"    Occurrences: {count}")
                print(f"    Record IDs: {transaction_id_records[transaction_id]}")
                print()

            print("=" * 80)
            print("NEXT STEPS:")
            print("1. Review the duplicate records above")
            print("2. Decide which records to keep and which to delete/merge")
            print("3. Manually fix duplicates before adding UNIQUE constraint")
            print("\nSuggested SQL to view duplicates:")
            print(f"  SELECT * FROM policies WHERE \"Transaction ID\" IN ({', '.join([f\"'{tid}'\" for tid in duplicates.keys()])})")
            print("\n⚠️  DO NOT add UNIQUE constraint until duplicates are resolved!")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_duplicates()
