import sqlite3
import json
import urllib.request
import urllib.parse
import urllib.error
import time

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

def execute_sql_in_supabase(sql_query, supabase_url, api_key):
    """Execute SQL directly in Supabase using the SQL endpoint"""
    try:
        # Use the SQL API endpoint
        sql_url = f"{supabase_url}/rest/v1/rpc/sql"
        
        data = {
            "query": sql_query
        }
        
        req = urllib.request.Request(sql_url)
        req.add_header('apikey', api_key)
        req.add_header('Authorization', f'Bearer {api_key}')
        req.add_header('Content-Type', 'application/json')
        req.get_method = lambda: 'POST'
        
        json_data = json.dumps(data).encode('utf-8')
        
        response = urllib.request.urlopen(req, json_data)
        result = json.loads(response.read().decode('utf-8'))
        return True, result
        
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return False, f"HTTP Error {e.code}: {error_body}"
    except Exception as e:
        return False, str(e)

def main():
    print("🔄 Recreating Supabase schema and migrating data...")
    
    # Load environment variables
    env = load_env()
    if not env:
        return
    
    SUPABASE_URL = env.get('SUPABASE_URL')
    SUPABASE_KEY = env.get('SUPABASE_ANON_KEY')
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: Missing Supabase credentials in .env file")
        return
    
    print("⚠️  WARNING: This will drop existing tables and recreate them!")
    print("📋 You should run the schema_postgresql_debug.sql in Supabase SQL Editor instead.")
    print("📋 Steps to migrate:")
    print("1. Go to your Supabase project dashboard")
    print("2. Open SQL Editor")
    print("3. Run the schema_postgresql_debug.sql script")
    print("4. Then run this migration script again")
    print("")
    
    # For now, let's just try the migration assuming schema exists
    print("🔄 Attempting migration with current schema...")
    
    # Connect to SQLite
    try:
        conn = sqlite3.connect('commissions.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        print("✅ Connected to SQLite database")
    except Exception as e:
        print(f"❌ Error connecting to SQLite: {e}")
        return
    
    # Get a sample record to see the exact structure
    cursor.execute("SELECT * FROM policies LIMIT 1")
    sample = cursor.fetchone()
    
    if sample:
        print("📋 SQLite policies table structure:")
        for key in sample.keys():
            print(f"  - '{key}': {type(sample[key]).__name__}")
    
    print("\n📝 To complete the migration:")
    print("1. Copy and run schema_postgresql_debug.sql in Supabase SQL Editor")
    print("2. Verify tables are created with correct column names")
    print("3. Run the migration script again")
    
    conn.close()

if __name__ == "__main__":
    main()