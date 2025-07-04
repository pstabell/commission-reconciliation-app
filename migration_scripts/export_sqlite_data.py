import sqlite3
import os

def export_sqlite_database(db_path):
    """Export SQLite database schema and data"""
    conn = sqlite3.connect(db_path)
    
    # Export full database dump
    with open('commissions_export.sql', 'w') as f:
        for line in conn.iterdump():
            f.write(f'{line}\n')
    
    print(f"Full database dump exported to: commissions_export.sql")
    
    # Get file sizes
    dump_size = os.path.getsize('commissions_export.sql')
    schema_size = os.path.getsize('schema_export.sql')
    
    print(f"Export file size: {dump_size:,} bytes")
    print(f"Schema file size: {schema_size:,} bytes")
    
    conn.close()

if __name__ == "__main__":
    export_sqlite_database("commissions.db")