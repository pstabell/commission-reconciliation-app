import sqlite3
import json
import urllib.request
import urllib.error

def load_env():
    env_vars = {}
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
    return env_vars

def supabase_insert(url, api_key, table, data):
    """Insert data into Supabase table"""
    try:
        table_url = f"{url}/rest/v1/{table}"
        req = urllib.request.Request(table_url)
        req.add_header('apikey', api_key)
        req.add_header('Authorization', f'Bearer {api_key}')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Prefer', 'return=representation')
        req.get_method = lambda: 'POST'
        
        json_data = json.dumps(data).encode('utf-8')
        response = urllib.request.urlopen(req, json_data)
        return True, json.loads(response.read().decode('utf-8'))
        
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return False, f"HTTP Error {e.code}: {error_body}"
    except Exception as e:
        return False, str(e)

def migrate_policies():
    print("🚀 Migrating SQLite data to Supabase...")
    
    # Load credentials
    env = load_env()
    SUPABASE_URL = env.get('SUPABASE_URL')
    SUPABASE_KEY = env.get('SUPABASE_ANON_KEY')
    
    # Connect to SQLite
    conn = sqlite3.connect('commissions.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Test connection to Supabase first
    print("🔍 Testing Supabase connection...")
    test_url = f"{SUPABASE_URL}/rest/v1/policies?select=*&limit=1"
    try:
        req = urllib.request.Request(test_url)
        req.add_header('apikey', SUPABASE_KEY)
        req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
        response = urllib.request.urlopen(req)
        print("✅ Supabase connection successful")
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        print("⚠️  Make sure you've run the schema_postgresql_debug.sql script in Supabase first!")
        return
    
    # Get all policies
    cursor.execute("SELECT * FROM policies")
    policies = cursor.fetchall()
    print(f"📊 Found {len(policies)} policies to migrate")
    
    # Convert and migrate in batches
    batch_size = 10  # Smaller batches for better error handling
    success_count = 0
    error_count = 0
    
    for i in range(0, len(policies), batch_size):
        batch = policies[i:i+batch_size]
        batch_data = []
        
        for row in batch:
            # Convert SQLite row to dictionary with exact column names
            policy_dict = {}
            for key in row.keys():
                value = row[key]
                policy_dict[key] = value  # Keep exact values, including None
            
            batch_data.append(policy_dict)
        
        # Insert batch
        success, result = supabase_insert(SUPABASE_URL, SUPABASE_KEY, 'policies', batch_data)
        
        if success:
            success_count += len(batch)
            print(f"  ✅ Batch {i//batch_size + 1}: Inserted {len(batch)} policies")
        else:
            error_count += len(batch)
            print(f"  ❌ Batch {i//batch_size + 1}: {result}")
            # Try individual inserts for this batch
            for j, policy in enumerate(batch_data):
                individual_success, individual_result = supabase_insert(SUPABASE_URL, SUPABASE_KEY, 'policies', [policy])
                if individual_success:
                    success_count += 1
                    error_count -= 1
                else:
                    print(f"    ❌ Individual policy {i+j+1}: {individual_result}")
    
    print(f"\n📊 Migration Results:")
    print(f"  ✅ Successful: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    
    # Migrate manual_commission_entries
    print("\n📊 Migrating manual commission entries...")
    cursor.execute("SELECT * FROM manual_commission_entries")
    entries = cursor.fetchall()
    
    if entries:
        entries_data = []
        for row in entries:
            entry_dict = {}
            for key in row.keys():
                if key != 'id':  # Skip SQLite auto-increment ID
                    entry_dict[key] = row[key]
            entries_data.append(entry_dict)
        
        success, result = supabase_insert(SUPABASE_URL, SUPABASE_KEY, 'manual_commission_entries', entries_data)
        if success:
            print(f"  ✅ Inserted {len(entries)} manual commission entries")
        else:
            print(f"  ❌ Error: {result}")
    
    conn.close()
    
    # Verify final counts
    print("\n🔍 Verifying migration...")
    try:
        verify_url = f"{SUPABASE_URL}/rest/v1/policies?select=*"
        req = urllib.request.Request(verify_url)
        req.add_header('apikey', SUPABASE_KEY)
        req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
        req.add_header('Prefer', 'count=exact')
        
        response = urllib.request.urlopen(req)
        content_range = response.headers.get('Content-Range', '')
        if content_range:
            count = content_range.split('/')[-1]
            print(f"  📊 Supabase policies table now has {count} records")
        
    except Exception as e:
        print(f"  ❌ Verification error: {e}")
    
    print("\n✅ Migration complete!")

if __name__ == "__main__":
    migrate_policies()