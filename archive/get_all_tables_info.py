import sqlite3

conn = sqlite3.connect('commissions.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence' ORDER BY name")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    print(f"\n=== {table_name} ===")
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = cursor.fetchall()
    print('cid|name|type|notnull|dflt_value|pk')
    for col in columns:
        print('|'.join(str(x) for x in col))

conn.close()