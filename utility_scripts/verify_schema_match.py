import sqlite3
import urllib.request
import json

def get_sqlite_columns():
    """Get columns from SQLite database"""
    conn = sqlite3.connect('commissions.db')
    cursor = conn.cursor()
    
    tables = {}
    
    # Get column info for each table
    for table_name in ['policies', 'commission_payments', 'manual_commission_entries', 'renewal_history']:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        tables[table_name] = [col[1] for col in columns]  # col[1] is the column name
    
    conn.close()
    return tables

def get_supabase_columns():
    """Get columns from Supabase"""
    # Load env
    env_vars = {}
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
    
    url = env_vars.get('SUPABASE_URL')
    key = env_vars.get('SUPABASE_ANON_KEY')
    
    tables = {}
    
    for table_name in ['policies', 'commission_payments', 'manual_commission_entries', 'renewal_history']:
        try:
            table_url = f'{url}/rest/v1/{table_name}?select=*&limit=1'
            req = urllib.request.Request(table_url)
            req.add_header('apikey', key)
            req.add_header('Authorization', f'Bearer {key}')
            
            response = urllib.request.urlopen(req)
            data = json.loads(response.read())
            
            if data:
                tables[table_name] = list(data[0].keys())
            else:
                # If no data, we can't get columns this way
                tables[table_name] = []
                
        except Exception as e:
            tables[table_name] = f"Error: {e}"
    
    return tables

def compare():
    """Compare SQLite and Supabase schemas"""
    sqlite_tables = get_sqlite_columns()
    supabase_tables = get_supabase_columns()
    
    print("=" * 80)
    print("SCHEMA VERIFICATION: SQLite vs Supabase (Actual)")
    print("=" * 80)
    
    for table_name in ['policies', 'commission_payments', 'manual_commission_entries', 'renewal_history']:
        print(f"\n📊 Table: {table_name}")
        print("-" * 60)
        
        sqlite_cols = set(sqlite_tables.get(table_name, []))
        supabase_cols = set(supabase_tables.get(table_name, []))
        
        if isinstance(supabase_tables.get(table_name), str):
            print(f"  ❌ Supabase error: {supabase_tables[table_name]}")
            continue
        
        # Remove auto-generated columns for comparison
        if table_name == 'policies':
            supabase_cols.discard('_id')  # PostgreSQL auto-added ID
        elif table_name in ['commission_payments', 'manual_commission_entries', 'renewal_history']:
            sqlite_cols.discard('id')  # SQLite auto-increment
            supabase_cols.discard('id')  # PostgreSQL SERIAL
        
        # Find differences
        missing_in_supabase = sqlite_cols - supabase_cols
        extra_in_supabase = supabase_cols - sqlite_cols
        
        if missing_in_supabase:
            print("  ❌ Missing in Supabase:")
            for col in sorted(missing_in_supabase):
                print(f"     - {col}")
        
        if extra_in_supabase:
            print("  ❌ Extra in Supabase:")
            for col in sorted(extra_in_supabase):
                print(f"     - {col}")
        
        if not missing_in_supabase and not extra_in_supabase:
            print("  ✅ All columns match perfectly!")
    
    # Data count comparison
    print("\n📊 Data Count Comparison")
    print("-" * 60)
    
    # SQLite counts
    conn = sqlite3.connect('commissions.db')
    cursor = conn.cursor()
    
    for table_name in ['policies', 'manual_commission_entries', 'commission_payments', 'renewal_history']:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        sqlite_count = cursor.fetchone()[0]
        
        # Supabase count
        try:
            table_url = f'{url}/rest/v1/{table_name}?select=*'
            req = urllib.request.Request(table_url)
            req.add_header('apikey', key)
            req.add_header('Authorization', f'Bearer {key}')
            req.add_header('Prefer', 'count=exact')
            
            response = urllib.request.urlopen(req)
            content_range = response.headers.get('Content-Range', '')
            if content_range:
                supabase_count = int(content_range.split('/')[-1])
            else:
                data = json.loads(response.read())
                supabase_count = len(data)
            
            match = "✅" if sqlite_count == supabase_count else "❌"
            print(f"  {match} {table_name}: SQLite={sqlite_count}, Supabase={supabase_count}")
            
        except Exception as e:
            print(f"  ❌ {table_name}: SQLite={sqlite_count}, Supabase=Error")
    
    conn.close()

if __name__ == "__main__":
    compare()