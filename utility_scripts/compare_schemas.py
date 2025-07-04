import sqlite3
import re

def get_sqlite_schema():
    """Get the actual schema from SQLite database"""
    conn = sqlite3.connect('commissions.db')
    cursor = conn.cursor()
    
    schema = {}
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        schema[table_name] = []
        for col in columns:
            cid, name, dtype, notnull, dflt_value, pk = col
            schema[table_name].append({
                'name': name,
                'type': dtype,
                'not_null': bool(notnull),
                'primary_key': bool(pk)
            })
    
    conn.close()
    return schema

def parse_postgresql_schema():
    """Parse the PostgreSQL schema from our SQL file"""
    with open('supabase_import_steps.sql', 'r') as f:
        content = f.read()
    
    schema = {}
    
    # Find CREATE TABLE statements
    table_pattern = r'CREATE TABLE IF NOT EXISTS (\w+)\s*\((.*?)\);'
    matches = re.findall(table_pattern, content, re.DOTALL | re.IGNORECASE)
    
    for table_name, columns_def in matches:
        schema[table_name] = []
        
        # Parse columns - handle multi-line definitions
        lines = columns_def.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('--'):
                continue
                
            # Match column definitions (name type constraints)
            col_match = re.match(r'"?([^"\s]+)"?\s+(\w+)', line)
            if col_match:
                col_name = col_match.group(1)
                col_type = col_match.group(2)
                
                # Skip special columns and constraints
                if col_name.upper() in ['PRIMARY', 'FOREIGN', 'UNIQUE', 'CHECK', 'CONSTRAINT']:
                    continue
                    
                schema[table_name].append({
                    'name': col_name,
                    'type': col_type
                })
    
    return schema

def compare_schemas():
    """Compare SQLite and PostgreSQL schemas"""
    sqlite_schema = get_sqlite_schema()
    pg_schema = parse_postgresql_schema()
    
    print("=" * 80)
    print("SCHEMA COMPARISON: SQLite vs PostgreSQL")
    print("=" * 80)
    
    # Compare each table
    all_tables = set(sqlite_schema.keys()) | set(pg_schema.keys())
    
    for table in sorted(all_tables):
        print(f"\n📊 Table: {table}")
        print("-" * 60)
        
        if table not in sqlite_schema:
            print("  ❌ Missing in SQLite")
            continue
        elif table not in pg_schema:
            print("  ❌ Missing in PostgreSQL")
            continue
        
        sqlite_cols = {col['name']: col for col in sqlite_schema[table]}
        pg_cols = {col['name']: col for col in pg_schema[table]}
        
        # Find differences
        all_cols = set(sqlite_cols.keys()) | set(pg_cols.keys())
        
        mismatches = []
        
        for col in sorted(all_cols):
            if col in sqlite_cols and col not in pg_cols:
                mismatches.append(f"  ❌ Column '{col}' exists in SQLite but NOT in PostgreSQL")
            elif col not in sqlite_cols and col in pg_cols:
                mismatches.append(f"  ❌ Column '{col}' exists in PostgreSQL but NOT in SQLite")
            elif col in sqlite_cols and col in pg_cols:
                sqlite_type = sqlite_cols[col]['type']
                pg_type = pg_cols[col]['type']
                
                # Check for potential type mismatches
                type_ok = False
                if sqlite_type == 'TEXT' and pg_type == 'TEXT':
                    type_ok = True
                elif sqlite_type == 'INTEGER' and pg_type in ['SERIAL', 'INTEGER', 'UUID']:
                    type_ok = True
                elif sqlite_type == 'REAL' and pg_type in ['REAL', 'DECIMAL']:
                    type_ok = True
                elif sqlite_type == 'FLOAT' and pg_type in ['DOUBLE', 'DECIMAL', 'FLOAT']:
                    type_ok = True
                
                if not type_ok:
                    mismatches.append(f"  ⚠️  Column '{col}': SQLite={sqlite_type}, PostgreSQL={pg_type}")
        
        if mismatches:
            for mismatch in mismatches:
                print(mismatch)
        else:
            print("  ✅ All columns match!")
    
    # Special check for policies table columns with spaces
    print("\n📋 Special Check: Policies Table Column Names")
    print("-" * 60)
    if 'policies' in sqlite_schema:
        for col in sqlite_schema['policies']:
            col_name = col['name']
            if ' ' in col_name or '(' in col_name or '/' in col_name:
                print(f"  Column with special characters: '{col_name}'")
                # Check if it's properly quoted in PostgreSQL
                if 'policies' in pg_schema:
                    pg_col_names = [c['name'] for c in pg_schema['policies']]
                    if col_name not in pg_col_names:
                        print(f"    ❌ NOT FOUND in PostgreSQL schema!")
                    else:
                        print(f"    ✅ Found in PostgreSQL schema")

if __name__ == "__main__":
    compare_schemas()