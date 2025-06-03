import pandas as pd
import sqlalchemy

# 1. Set your Excel file path and sheet name
excel_path = r"C:\Users\Patri\OneDrive\STABELL DOCUMENTS\STABELL FILES\Employment\Patrick\SWFL Insurance\COMMISSION HISTORY\ALL COMMISSIONS (AUTOMATED).xlsx"
sheet_name = "PENDING"  # <-- Use the correct sheet name

# 2. Read the Excel file
df = pd.read_excel(excel_path, sheet_name=sheet_name)
print("Excel file loaded. First few rows:")
print(df.head())

# 3. Clean column names (optional but recommended)
df.columns = df.columns.str.strip()

# 4. Connect to SQLite database (creates commissions.db in your project folder)
engine = sqlalchemy.create_engine('sqlite:///commissions.db')

# 5. Write DataFrame to the database (table name: 'policies')
df.to_sql('policies', engine, if_exists='replace', index=False)
print("Excel data imported to SQLite database!")