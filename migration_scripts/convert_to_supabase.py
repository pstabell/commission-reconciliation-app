#!/usr/bin/env python3
"""
Convert commission_app.py from SQLite to Supabase
"""

import re

# Read the original file
with open('commission_app.py', 'r') as f:
    content = f.read()

# 1. Replace imports
old_imports = """import sqlalchemy"""
new_imports = """from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()"""

content = content.replace(old_imports, new_imports)

# 2. Replace get_database_engine function
old_engine = """@st.cache_resource
def get_database_engine():
    \"\"\"Get cached database engine for better performance.\"\"\"
    return sqlalchemy.create_engine(
        'sqlite:///commissions.db',
        pool_pre_ping=True,
        pool_recycle=3600
    )"""

new_engine = """@st.cache_resource
def get_supabase_client():
    \"\"\"Get cached Supabase client.\"\"\"
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        st.error("Missing Supabase credentials. Please check your .env file.")
        st.stop()
    return create_client(url, key)"""

content = content.replace(old_engine, new_engine)

# 3. Replace load_policies_data function
old_load = """@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_policies_data():
    \"\"\"Load policies data with caching for better performance.\"\"\"
    try:
        engine = get_database_engine()
        return pd.read_sql('SELECT * FROM policies', engine)
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return pd.DataFrame()"""

new_load = """@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_policies_data():
    \"\"\"Load policies data from Supabase with caching.\"\"\"
    try:
        supabase = get_supabase_client()
        response = supabase.table('policies').select("*").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            # Ensure numeric columns are properly typed
            if 'Agent Estimated Comm $' in df.columns:
                df['Agent Estimated Comm $'] = pd.to_numeric(df['Agent Estimated Comm $'], errors='coerce')
            if 'BALANCE DUE' in df.columns:
                df['BALANCE DUE'] = pd.to_numeric(df['BALANCE DUE'], errors='coerce')
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data from Supabase: {e}")
        return pd.DataFrame()"""

content = content.replace(old_load, new_load)

# 4. Add clear cache function
clear_cache_func = """
def clear_policies_cache():
    \"\"\"Clear the policies data cache.\"\"\"
    load_policies_data.clear()
"""

# Insert after load_policies_data function
content = content.replace("return pd.DataFrame()", "return pd.DataFrame()" + clear_cache_func, 1)

# 5. Replace all engine = get_database_engine() with supabase = get_supabase_client()
content = content.replace("engine = get_database_engine()", "supabase = get_supabase_client()")

# 6. Replace pd.read_sql calls
content = re.sub(
    r"pd\.read_sql\('SELECT \* FROM manual_commission_entries', engine\)",
    """supabase.table('manual_commission_entries').select("*").execute().data or []""",
    content
)

content = re.sub(
    r"pd\.read_sql\('SELECT \* FROM commission_payments[^']*', engine\)",
    """supabase.table('commission_payments').select("*").order('payment_timestamp', desc=True).execute().data or []""",
    content
)

# 7. Replace DELETE operations
content = re.sub(
    r'conn\.execute\(sqlalchemy\.text\("DELETE FROM manual_commission_entries WHERE transaction_id = :tid"\), \{"tid": [^}]+\}\)',
    'supabase.table("manual_commission_entries").delete().eq("transaction_id", selected_entry["transaction_id"]).execute()',
    content
)

content = re.sub(
    r'conn\.execute\(sqlalchemy\.text\("DELETE FROM commission_payments WHERE id = :id"\), \{"id": [^}]+\}\)',
    'supabase.table("commission_payments").delete().eq("id", st.session_state["pending_delete_history_id"]).execute()',
    content
)

# 8. Replace INSERT operations for policies
content = re.sub(
    r'engine\.execute\(text\(.*?INSERT INTO policies.*?\), new_policy_dict\)',
    'supabase.table("policies").insert(new_policy_dict).execute()',
    content,
    flags=re.DOTALL
)

# 9. Replace UPDATE operations
content = re.sub(
    r'conn\.execute\(text\(update_query\), update_data\)',
    '''# Convert update_data to dict and update via Supabase
                                    policy_id = selected_policies.iloc[0]['_id']
                                    update_dict = dict(update_data)
                                    if '_id' in update_dict:
                                        del update_dict['_id']
                                    supabase.table('policies').update(update_dict).eq('_id', policy_id).execute()''',
    content
)

# 10. Add connection context replacement
content = re.sub(
    r'with engine\.connect\(\) as conn:',
    '# Supabase operations',
    content
)

content = re.sub(
    r'with engine\.begin\(\) as conn:',
    '# Supabase transaction',
    content
)

# 11. Replace all conn.commit() and conn.rollback()
content = content.replace('conn.commit()', '# Transaction auto-committed in Supabase')
content = content.replace('conn.rollback()', '# Handle error')

# 12. Replace df.to_sql
content = re.sub(
    r'renewed_df\.to_sql\([^)]+\)',
    '''# Save renewed policies to Supabase
                                    for _, row in renewed_df.iterrows():
                                        policy_data = row.to_dict()
                                        if '_id' in policy_data:
                                            del policy_data['_id']
                                        supabase.table('policies').insert(policy_data).execute()''',
    content
)

# 13. Add cache clearing after operations
content = re.sub(
    r'st\.success\("Policy added successfully!"\)',
    '''st.success("Policy added successfully!")
                            clear_policies_cache()''',
    content
)

content = re.sub(
    r'st\.success\("Selected policies updated successfully!"\)',
    '''st.success("Selected policies updated successfully!")
                                        clear_policies_cache()''',
    content
)

# 14. Handle sqlalchemy.text removal
content = content.replace('from sqlalchemy import text', '')
content = content.replace('sqlalchemy.text(', '')
content = content.replace('text(', '')

# Write the converted file
with open('commission_app.py', 'w') as f:
    f.write(content)

print("Conversion complete! commission_app.py has been updated to use Supabase.")