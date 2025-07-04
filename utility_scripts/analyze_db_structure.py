import sqlite3

def analyze_database_structure(db_path):
    """Analyze SQLite database structure and export schema"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print("=== DATABASE STRUCTURE ANALYSIS ===\n")
    print(f"Database: {db_path}")
    print(f"Tables found: {len(tables)}\n")
    
    schema_export = []
    
    for table in tables:
        table_name = table[0]
        print(f"\n--- Table: {table_name} ---")
        
        # Get table schema
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        create_statement = cursor.fetchone()[0]
        print(f"CREATE statement:\n{create_statement}\n")
        schema_export.append(create_statement + ";\n")
        
        # Get column information
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print("Columns:")
        for col in columns:
            cid, name, dtype, notnull, dflt_value, pk = col
            print(f"  - {name}: {dtype} {'NOT NULL' if notnull else 'NULL'} {'PRIMARY KEY' if pk else ''} {f'DEFAULT {dflt_value}' if dflt_value else ''}")
        
        # Get indexes
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='{table_name}'")
        indexes = cursor.fetchall()
        if indexes:
            print("\nIndexes:")
            for idx in indexes:
                if idx[0]:  # Skip auto-created indexes (None)
                    print(f"  {idx[0]}")
                    schema_export.append(idx[0] + ";\n")
        
        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        fks = cursor.fetchall()
        if fks:
            print("\nForeign Keys:")
            for fk in fks:
                print(f"  - {fk[3]} -> {fk[2]}.{fk[4]}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"\nRow count: {count}")
    
    # Export schema
    with open('schema_export.sql', 'w') as f:
        f.writelines(schema_export)
    
    print("\n\n=== RELATIONSHIPS AND CONSTRAINTS ===")
    
    # Analyze relationships based on column names
    print("\nPotential relationships (based on column names):")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        for col in columns:
            col_name = col[1]
            if col_name.endswith('_id') or col_name.endswith('_ID'):
                print(f"  - {table_name}.{col_name} (possible foreign key)")
    
    conn.close()
    
    print("\n\nSchema exported to: schema_export.sql")
    return schema_export

# Run the analysis
if __name__ == "__main__":
    analyze_database_structure("commissions.db")