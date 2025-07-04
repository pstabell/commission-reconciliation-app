import sqlite3
import json

def analyze_database_detailed(db_path):
    """Analyze SQLite database structure in detail"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    schema_info = {}
    
    for table in tables:
        table_name = table[0]
        if table_name == 'sqlite_sequence':
            continue
            
        print(f"\n=== Table: {table_name} ===")
        
        # Get exact column information
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        schema_info[table_name] = []
        
        print("\nColumns (exact names):")
        for col in columns:
            cid, name, dtype, notnull, dflt_value, pk = col
            col_info = {
                'name': name,
                'type': dtype,
                'not_null': bool(notnull),
                'default': dflt_value,
                'primary_key': bool(pk)
            }
            schema_info[table_name].append(col_info)
            print(f"  '{name}' - {dtype} {'NOT NULL' if notnull else 'NULL'} {'PRIMARY KEY' if pk else ''} {f'DEFAULT {dflt_value}' if dflt_value else ''}")
        
        # Get sample data to understand actual content
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        sample_data = cursor.fetchall()
        
        if sample_data:
            print(f"\nSample data ({len(sample_data)} rows):")
            # Get column names
            col_names = [desc[0] for desc in cursor.description]
            for i, row in enumerate(sample_data):
                print(f"\nRow {i+1}:")
                for j, (col_name, value) in enumerate(zip(col_names, row)):
                    if value is not None and value != '':
                        print(f"  {col_name}: {repr(value)}")
    
    # Save schema info as JSON for reference
    with open('schema_info.json', 'w') as f:
        json.dump(schema_info, f, indent=2)
    
    conn.close()
    
    print("\n\nSchema information saved to: schema_info.json")
    return schema_info

# Run the analysis
if __name__ == "__main__":
    schema = analyze_database_detailed("commissions.db")