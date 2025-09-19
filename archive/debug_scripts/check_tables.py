import sqlite3

# Connect to the database
conn = sqlite3.connect('commissions.db')
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print("Tables in commissions.db:")
for table in tables:
    print(f"  - {table[0]}")

conn.close()