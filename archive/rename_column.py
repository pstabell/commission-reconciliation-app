#!/usr/bin/env python3
"""
Script to rename 'Paid Amount' column to 'Agent Paid Amount (STMT)' in the database
"""

import sqlite3
import os
from datetime import datetime

def backup_database(db_path):
    """Create a backup before making changes"""
    backup_path = f"commissions_BACKUP_BEFORE_COLUMN_RENAME_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    
    # Copy the database file
    import shutil
    shutil.copy2(db_path, backup_path)
    print(f"✅ Database backed up to: {backup_path}")
    return backup_path

def rename_column_in_database(db_path, table_name, old_column, new_column):
    """Rename a column in SQLite database"""
    
    # Step 1: Create backup
    backup_path = backup_database(db_path)
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Step 2: Check if old column exists
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if old_column not in column_names:
            print(f"❌ Column '{old_column}' not found in table '{table_name}'")
            print(f"Available columns: {column_names}")
            return False
            
        if new_column in column_names:
            print(f"❌ Column '{new_column}' already exists in table '{table_name}'")
            return False
        
        print(f"🔄 Renaming column '{old_column}' to '{new_column}' in table '{table_name}'...")
        
        # Step 3: Create new table with renamed column
        # Get table schema
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        create_sql = cursor.fetchone()[0]
        
        # Replace old column name with new column name in CREATE statement
        new_create_sql = create_sql.replace(f'"{old_column}"', f'"{new_column}"')
        new_create_sql = new_create_sql.replace(f'`{old_column}`', f'`{new_column}`')
        new_create_sql = new_create_sql.replace(f'[{old_column}]', f'[{new_column}]')
        
        # If no brackets/quotes, replace the column name directly
        if old_column in new_create_sql and new_column not in new_create_sql:
            new_create_sql = new_create_sql.replace(old_column, new_column)
        
        # Create temporary table
        temp_table = f"{table_name}_temp"
        new_create_sql = new_create_sql.replace(f"CREATE TABLE {table_name}", f"CREATE TABLE {temp_table}")
        
        cursor.execute(new_create_sql)
        
        # Step 4: Copy data to new table
        # Get all column names for the copy operation
        old_columns = ", ".join([f'"{col[1]}"' for col in columns])
        new_columns = old_columns.replace(f'"{old_column}"', f'"{new_column}"')
        
        cursor.execute(f"INSERT INTO {temp_table} SELECT {old_columns} FROM {table_name}")
        
        # Step 5: Drop old table and rename new table
        cursor.execute(f"DROP TABLE {table_name}")
        cursor.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name}")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print(f"✅ Successfully renamed column '{old_column}' to '{new_column}' in table '{table_name}'")
        return True
        
    except Exception as e:
        print(f"❌ Error renaming column: {e}")
        # Restore backup
        import shutil
        shutil.copy2(backup_path, db_path)
        print(f"🔄 Database restored from backup: {backup_path}")
        return False

def main():
    """Main function to rename the column"""
    db_path = "commissions.db"
    table_name = "policies"
    old_column = "Paid Amount"
    new_column = "Agent Paid Amount (STMT)"
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return
    
    print("🚀 Starting column rename operation...")
    print(f"Database: {db_path}")
    print(f"Table: {table_name}")
    print(f"Renaming: '{old_column}' → '{new_column}'")
    print()
    
    success = rename_column_in_database(db_path, table_name, old_column, new_column)
    
    if success:
        print()
        print("🎉 Column rename completed successfully!")
        print("The 'Invalid database column: Agent Paid Amount (STMT)' error should now be resolved.")
    else:
        print()
        print("❌ Column rename failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
