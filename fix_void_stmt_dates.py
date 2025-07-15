"""
Fix STMT DATE for void transactions to match the date in their Transaction ID
"""

import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

def extract_date_from_void_id(transaction_id):
    """Extract date from void transaction ID format: XXXXXXX-VOID-YYYYMMDD"""
    try:
        if '-VOID-' in transaction_id:
            date_part = transaction_id.split('-VOID-')[1]
            # Parse YYYYMMDD format
            year = int(date_part[0:4])
            month = int(date_part[4:6])
            day = int(date_part[6:8])
            # Return in MM/DD/YYYY format
            return f"{month:02d}/{day:02d}/{year}"
    except:
        return None

def fix_void_stmt_dates():
    """Update STMT DATE for all void transactions to match their Transaction ID date"""
    
    print("Fetching void transactions...")
    
    # Fetch all void transactions
    result = supabase.table('policies').select('*').like('Transaction ID', '%-VOID-%').execute()
    void_transactions = result.data
    
    print(f"Found {len(void_transactions)} void transactions")
    
    updates_needed = []
    
    for trans in void_transactions:
        trans_id = trans.get('Transaction ID')
        current_stmt_date = trans.get('STMT DATE')
        
        # Extract the correct date from transaction ID
        correct_date = extract_date_from_void_id(trans_id)
        
        if correct_date and correct_date != current_stmt_date:
            updates_needed.append({
                'trans_id': trans_id,
                'current_date': current_stmt_date,
                'correct_date': correct_date
            })
    
    print(f"\nFound {len(updates_needed)} transactions needing date corrections")
    
    if updates_needed:
        print("\nTransactions to update:")
        for update in updates_needed[:10]:  # Show first 10
            print(f"  {update['trans_id']}: {update['current_date']} → {update['correct_date']}")
        
        if len(updates_needed) > 10:
            print(f"  ... and {len(updates_needed) - 10} more")
        
        # Ask for confirmation
        confirm = input("\nProceed with updates? (yes/no): ")
        
        if confirm.lower() == 'yes':
            success_count = 0
            error_count = 0
            
            for update in updates_needed:
                try:
                    # Update the STMT DATE
                    result = supabase.table('policies').update({
                        'STMT DATE': update['correct_date']
                    }).eq('Transaction ID', update['trans_id']).execute()
                    
                    success_count += 1
                    print(f"✓ Updated {update['trans_id']}")
                    
                except Exception as e:
                    error_count += 1
                    print(f"✗ Error updating {update['trans_id']}: {e}")
            
            print(f"\nUpdate complete!")
            print(f"  Successfully updated: {success_count}")
            print(f"  Errors: {error_count}")
        else:
            print("Update cancelled")
    else:
        print("All void transactions already have correct STMT DATE values")

if __name__ == "__main__":
    fix_void_stmt_dates()