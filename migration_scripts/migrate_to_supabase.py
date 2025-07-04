import sqlite3
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

# Load .env file manually
def load_env():
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
        return env_vars
    except Exception as e:
        print(f"Error reading .env file: {e}")
        return None

# Function to make Supabase API request
def supabase_request(url, api_key, method='GET', data=None):
    req = urllib.request.Request(url)
    req.add_header('apikey', api_key)
    req.add_header('Authorization', f'Bearer {api_key}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Prefer', 'return=representation')
    
    if method != 'GET':
        req.get_method = lambda: method
    
    if data:
        data = json.dumps(data).encode('utf-8')
        req.add_header('Content-Length', str(len(data)))
    
    try:
        response = urllib.request.urlopen(req, data)
        return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"Request error: {e}")
        return None

def migrate_data():
    print("🚀 Starting SQLite to Supabase migration...")
    
    # Load environment variables
    env = load_env()
    if not env:
        return
    
    SUPABASE_URL = env.get('SUPABASE_URL')
    SUPABASE_KEY = env.get('SUPABASE_ANON_KEY')
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: Missing Supabase credentials in .env file")
        return
    
    # Connect to SQLite
    try:
        conn = sqlite3.connect('commissions.db')
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()
        print("✅ Connected to SQLite database")
    except Exception as e:
        print(f"❌ Error connecting to SQLite: {e}")
        return
    
    # Migrate policies table
    print("\n📊 Migrating policies table...")
    try:
        cursor.execute("SELECT * FROM policies")
        policies = cursor.fetchall()
        
        print(f"Found {len(policies)} policies to migrate")
        
        # Process in batches to avoid API limits
        batch_size = 50
        success_count = 0
        error_count = 0
        
        for i in range(0, len(policies), batch_size):
            batch = policies[i:i+batch_size]
            batch_data = []
            
            for row in batch:
                # Convert Row to dictionary with exact column names
                policy_dict = {}
                for key in row.keys():
                    value = row[key]
                    # Handle None values
                    if value is None:
                        policy_dict[key] = None
                    # Keep numbers as numbers
                    elif isinstance(value, (int, float)):
                        policy_dict[key] = value
                    # Everything else as string
                    else:
                        policy_dict[key] = str(value) if value else None
                
                batch_data.append(policy_dict)
            
            # Send batch to Supabase
            url = f"{SUPABASE_URL}/rest/v1/policies"
            result = supabase_request(url, SUPABASE_KEY, 'POST', batch_data)
            
            if result:
                success_count += len(batch)
                print(f"  ✅ Batch {i//batch_size + 1}: Inserted {len(batch)} records")
            else:
                error_count += len(batch)
                print(f"  ❌ Batch {i//batch_size + 1}: Failed to insert {len(batch)} records")
        
        print(f"\nPolicies migration complete: {success_count} successful, {error_count} errors")
        
    except Exception as e:
        print(f"❌ Error migrating policies: {e}")
        import traceback
        traceback.print_exc()
    
    # Migrate manual_commission_entries table
    print("\n📊 Migrating manual_commission_entries table...")
    try:
        cursor.execute("SELECT * FROM manual_commission_entries")
        entries = cursor.fetchall()
        
        print(f"Found {len(entries)} manual commission entries to migrate")
        
        if entries:
            entries_data = []
            for row in entries:
                entry_dict = {}
                for key in row.keys():
                    if key != 'id':  # Skip the SQLite ID
                        value = row[key]
                        if value is None:
                            entry_dict[key] = None
                        elif isinstance(value, (int, float)):
                            entry_dict[key] = value
                        else:
                            entry_dict[key] = str(value) if value else None
                entries_data.append(entry_dict)
            
            url = f"{SUPABASE_URL}/rest/v1/manual_commission_entries"
            result = supabase_request(url, SUPABASE_KEY, 'POST', entries_data)
            
            if result:
                print(f"  ✅ Inserted {len(entries)} manual commission entries")
            else:
                print(f"  ❌ Failed to insert manual commission entries")
    
    except Exception as e:
        print(f"❌ Error migrating manual_commission_entries: {e}")
    
    # Migrate commission_payments table
    print("\n📊 Migrating commission_payments table...")
    try:
        cursor.execute("SELECT * FROM commission_payments")
        payments = cursor.fetchall()
        
        print(f"Found {len(payments)} commission payments to migrate")
        
        if payments:
            payments_data = []
            for row in payments:
                payment_dict = {}
                for key in row.keys():
                    if key != 'id':  # Skip the SQLite ID
                        value = row[key]
                        if value is None:
                            payment_dict[key] = None
                        elif isinstance(value, (int, float)):
                            payment_dict[key] = value
                        else:
                            payment_dict[key] = str(value) if value else None
                payments_data.append(payment_dict)
            
            url = f"{SUPABASE_URL}/rest/v1/commission_payments"
            result = supabase_request(url, SUPABASE_KEY, 'POST', payments_data)
            
            if result:
                print(f"  ✅ Inserted {len(payments)} commission payments")
            else:
                print(f"  ❌ Failed to insert commission payments")
    
    except Exception as e:
        print(f"❌ Error migrating commission_payments: {e}")
    
    # Migrate renewal_history table
    print("\n📊 Migrating renewal_history table...")
    try:
        cursor.execute("SELECT * FROM renewal_history")
        renewals = cursor.fetchall()
        
        print(f"Found {len(renewals)} renewal history records to migrate")
        
        if renewals:
            renewals_data = []
            for row in renewals:
                renewal_dict = {}
                for key in row.keys():
                    if key != 'id':  # Skip the SQLite ID
                        value = row[key]
                        if value is None:
                            renewal_dict[key] = None
                        elif isinstance(value, (int, float)):
                            renewal_dict[key] = value
                        else:
                            renewal_dict[key] = str(value) if value else None
                renewals_data.append(renewal_dict)
            
            url = f"{SUPABASE_URL}/rest/v1/renewal_history"
            result = supabase_request(url, SUPABASE_KEY, 'POST', renewals_data)
            
            if result:
                print(f"  ✅ Inserted {len(renewals)} renewal history records")
            else:
                print(f"  ❌ Failed to insert renewal history records")
    
    except Exception as e:
        print(f"❌ Error migrating renewal_history: {e}")
    
    # Close SQLite connection
    conn.close()
    
    # Verify migration
    print("\n🔍 Verifying migration...")
    tables = ['policies', 'commission_payments', 'manual_commission_entries', 'renewal_history']
    
    for table in tables:
        try:
            url = f"{SUPABASE_URL}/rest/v1/{table}?select=*"
            req = urllib.request.Request(url)
            req.add_header('apikey', SUPABASE_KEY)
            req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
            req.add_header('Prefer', 'count=exact')
            
            response = urllib.request.urlopen(req)
            data = json.loads(response.read())
            
            # Get count from header
            content_range = response.headers.get('Content-Range', '')
            if content_range:
                count = content_range.split('/')[-1]
            else:
                count = len(data)
            
            print(f"  {table}: {count} records")
            
        except Exception as e:
            print(f"  {table}: Error getting count - {e}")
    
    print("\n✅ Migration complete!")
    print("\n📝 Next steps:")
    print("1. Verify the data in your Supabase dashboard")
    print("2. Update your commission_app.py to use Supabase instead of SQLite")
    print("3. Test all functionality with the new database")

if __name__ == "__main__":
    migrate_data()