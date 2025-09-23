"""
Test to ensure user_preferences and user_policy_types tables are properly separated.
This will help identify where the column error is coming from.
"""

def test_table_separation():
    """Test that tables are properly separated."""
    
    print("Testing Table Separation")
    print("=" * 60)
    
    # Check user_preferences_db.py
    print("\n1. Checking user_preferences_db.py...")
    try:
        from user_preferences_db import UserPreferences
        
        # Check what data is being inserted
        up = UserPreferences()
        
        # Check the _create_user_preferences method
        import inspect
        source = inspect.getsource(up._create_user_preferences)
        
        print("   _create_user_preferences method:")
        if 'policy_types' in source or 'default_type' in source:
            print("   ⚠️  WARNING: Found policy-related fields in user preferences creation!")
            print("   This could be the source of the error.")
        else:
            print("   ✅ No policy-related fields found in creation method")
        
        # Check what fields are in the data dict
        lines = source.split('\n')
        data_lines = [l for l in lines if 'data = {' in l or 'data[' in l]
        if data_lines:
            print("   Data fields being set:")
            for line in data_lines:
                print(f"     {line.strip()}")
                
    except Exception as e:
        print(f"   Error checking user_preferences_db: {e}")
    
    # Check user_policy_types_db.py
    print("\n2. Checking user_policy_types_db.py...")
    try:
        from user_policy_types_db import UserPolicyTypes
        
        # Check what data is being inserted
        upt = UserPolicyTypes()
        
        # Check the _create_user_types method
        import inspect
        source = inspect.getsource(upt._create_user_types)
        
        print("   _create_user_types method:")
        if 'color_theme' in source:
            print("   ⚠️  WARNING: Found preferences-related fields in policy types creation!")
            print("   This could indicate table confusion.")
        else:
            print("   ✅ No preferences-related fields found in creation method")
        
        # Check what fields are in the data dict
        lines = source.split('\n')
        data_lines = [l for l in lines if 'data = {' in l or 'data[' in l]
        if data_lines:
            print("   Data fields being set:")
            for line in data_lines[:10]:  # First 10 lines
                print(f"     {line.strip()}")
                
    except Exception as e:
        print(f"   Error checking user_policy_types_db: {e}")
    
    # Check for any cross-contamination
    print("\n3. Checking for cross-contamination...")
    
    files_to_check = ['user_preferences_db.py', 'user_policy_types_db.py']
    
    for file in files_to_check:
        try:
            with open(file, 'r') as f:
                content = f.read()
            
            # Check for wrong table references
            if file == 'user_preferences_db.py':
                if 'user_policy_types' in content:
                    print(f"   ⚠️  {file} references user_policy_types table!")
                    # Find the lines
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'user_policy_types' in line:
                            print(f"      Line {i+1}: {line.strip()}")
                            
            elif file == 'user_policy_types_db.py':
                if "table('user_preferences')" in content:
                    print(f"   ⚠️  {file} references user_preferences table!")
                    # Find the lines
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if "table('user_preferences')" in line:
                            print(f"      Line {i+1}: {line.strip()}")
                            
        except Exception as e:
            print(f"   Error checking {file}: {e}")
    
    print("\n" + "=" * 60)
    print("DIAGNOSIS")
    print("=" * 60)
    
    print("\nThe error 'column \"default_type\" does not exist' suggests:")
    print("1. Something is trying to INSERT or UPDATE user_preferences with 'default_type'")
    print("2. The 'default_type' column belongs to user_policy_types, not user_preferences")
    print("\nPossible causes:")
    print("- Mixed up table names in an INSERT/UPDATE statement")
    print("- Copy-paste error where policy code was used for preferences")
    print("- Database migration script with wrong table reference")
    
    print("\nTo fix:")
    print("1. Run the emergency fix SQL: sql_scripts/emergency_fix_user_preferences.sql")
    print("2. Check any recent code changes that might mix these tables")
    print("3. Ensure initialization code uses the correct table for each data type")

if __name__ == "__main__":
    test_table_separation()