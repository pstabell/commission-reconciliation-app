"""
Analyze void transactions to understand batch relationships
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()

# Initialize Supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

def analyze_void_batches():
    """Analyze void transactions and their batch relationships"""
    
    print("Fetching void transactions...")
    
    # Fetch all void transactions with their reconciliation_id
    result = supabase.table('policies').select('*').like('Transaction ID', '%-VOID-%').execute()
    void_transactions = result.data
    
    print(f"Found {len(void_transactions)} void transactions\n")
    
    # Group by reconciliation_id (batch)
    batches = defaultdict(list)
    for trans in void_transactions:
        batch_id = trans.get('reconciliation_id', 'NO_BATCH')
        batches[batch_id].append(trans)
    
    print(f"Found {len(batches)} unique batch IDs:\n")
    
    # Analyze each batch
    for batch_id, transactions in sorted(batches.items()):
        print(f"Batch: {batch_id}")
        print(f"  Transactions: {len(transactions)}")
        
        # Extract date from batch ID if it matches VOID-IMPORT pattern
        if batch_id.startswith('VOID-IMPORT-'):
            # Format: VOID-IMPORT-YYYYMMDD-XXXXXXXX
            parts = batch_id.split('-')
            if len(parts) >= 3:
                date_str = parts[2]  # YYYYMMDD
                try:
                    year = int(date_str[0:4])
                    month = int(date_str[4:6])
                    day = int(date_str[6:8])
                    correct_date = f"{month:02d}/{day:02d}/{year}"
                    print(f"  Correct STMT DATE should be: {correct_date}")
                except:
                    print(f"  Could not parse date from batch ID")
        
        # Show sample transactions
        print("  Sample transactions:")
        for trans in transactions[:3]:
            trans_id = trans.get('Transaction ID')
            stmt_date = trans.get('STMT DATE')
            customer = trans.get('Customer')
            print(f"    {trans_id} | {stmt_date} | {customer}")
        
        if len(transactions) > 3:
            print(f"    ... and {len(transactions) - 3} more")
        
        print()
    
    # Look for any patterns in NOTES field
    print("\nChecking NOTES field for batch information...")
    sample_notes = set()
    for trans in void_transactions[:20]:
        note = trans.get('NOTES', '')
        if note and 'VOID' in note:
            sample_notes.add(note)
    
    if sample_notes:
        print("Sample NOTES entries:")
        for note in list(sample_notes)[:5]:
            print(f"  {note}")

if __name__ == "__main__":
    analyze_void_batches()