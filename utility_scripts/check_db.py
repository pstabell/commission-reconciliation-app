import sqlite3
import os

# Check if database file exists
db_path = "commissions.db"
if os.path.exists(db_path):
    print(f"Database file found: {db_path}")
    print(f"File size: {os.path.getsize(db_path)} bytes")
else:
    print(f"Database file NOT found: {db_path}")

try:
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"\nTables in database:")
    if tables:
        for table in tables:
            table_name = table[0]
            print(f"  - {table_name}")
            
            # Get row count for each table
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"    Rows: {count}")
            except Exception as e:
                print(f"    Error counting rows: {e}")
    else:
        print("  No tables found in database")
    
    conn.close()
    
except Exception as e:
    print(f"Error accessing database: {e}")
