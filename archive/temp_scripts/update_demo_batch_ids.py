#!/usr/bin/env python3
"""
Script to update demo reconciliation data with batch IDs based on statement dates
extracted from transaction IDs.

Transaction ID format: XXXXXXX-STMT-YYYYMMDD
Batch ID format: DEMO-RECON-YYYYMMDD
"""

import streamlit as st
import os
import re
from datetime import datetime

# This script should be run from within the Streamlit app
# It will use the existing Supabase connection from session state

def extract_date_from_transaction_id(transaction_id):
    """Extract date from transaction ID format: XXXXXXX-STMT-YYYYMMDD"""
    if not transaction_id:
        return None
    
    # Match pattern ending with 8 digits (YYYYMMDD)
    match = re.search(r'-STMT-(\d{8})$', str(transaction_id))
    if match:
        date_str = match.group(1)
        try:
            # Validate it's a real date
            datetime.strptime(date_str, '%Y%m%d')
            return date_str
        except ValueError:
            return None
    return None

def update_demo_batch_ids():
    """Update reconciliation records with batch IDs for demo organization"""
    
    print("Fetching demo reconciliation data...")
    
    # Fetch all reconciliation data for demo organization
    response = supabase.table('reconciliation').select('*').eq('organization', 'DEMO-550e8400-e29b-41d4-a716-446655440000').execute()
    
    if not response.data:
        print("No reconciliation data found for demo organization")
        return
    
    records = response.data
    print(f"Found {len(records)} reconciliation records")
    
    # Group records by statement date
    date_groups = {}
    no_date_count = 0
    
    for record in records:
        transaction_id = record.get('transaction_id')
        date_str = extract_date_from_transaction_id(transaction_id)
        
        if date_str:
            if date_str not in date_groups:
                date_groups[date_str] = []
            date_groups[date_str].append(record)
        else:
            no_date_count += 1
            print(f"Could not extract date from transaction ID: {transaction_id}")
    
    print(f"\nFound {len(date_groups)} unique statement dates")
    print(f"Records without valid dates: {no_date_count}")
    
    # Update records with batch IDs
    updates_made = 0
    
    for date_str, group_records in sorted(date_groups.items()):
        batch_id = f"DEMO-RECON-{date_str}"
        print(f"\nProcessing date {date_str}: {len(group_records)} records -> Batch ID: {batch_id}")
        
        # Update each record in this date group
        for record in group_records:
            try:
                # Only update if reconciliation_id is null or empty
                if not record.get('reconciliation_id'):
                    response = supabase.table('reconciliation').update({
                        'reconciliation_id': batch_id
                    }).eq('id', record['id']).execute()
                    
                    if response.data:
                        updates_made += 1
                        print(f"  Updated record {record['transaction_id']}")
                else:
                    print(f"  Skipping {record['transaction_id']} - already has batch ID: {record['reconciliation_id']}")
                    
            except Exception as e:
                print(f"  Error updating record {record['transaction_id']}: {str(e)}")
    
    print(f"\n✅ Update complete! Updated {updates_made} records with batch IDs")
    
    # Show summary of batches created
    if date_groups:
        print("\nBatch summary:")
        for date_str in sorted(date_groups.keys()):
            batch_id = f"DEMO-RECON-{date_str}"
            count = len(date_groups[date_str])
            # Convert date for display
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            formatted_date = date_obj.strftime('%B %d, %Y')
            print(f"  {batch_id}: {count} transactions (Statement Date: {formatted_date})")

if __name__ == "__main__":
    update_demo_batch_ids()