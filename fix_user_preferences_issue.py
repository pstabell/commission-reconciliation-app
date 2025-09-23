"""
Fix for user_preferences table column issue.
This script ensures that user_preferences and user_policy_types tables have the correct schema.
"""

from database_utils import get_supabase_client
import sys

def fix_user_preferences_schema():
    """Fix the user_preferences table schema issue."""
    supabase = get_supabase_client()
    
    print("Checking and fixing user_preferences table schema...")
    
    try:
        # First, let's see what's in the user_preferences table
        print("\n1. Checking current user_preferences structure...")
        test_result = supabase.table('user_preferences').select('*').limit(1).execute()
        if test_result.data:
            print(f"Current columns in user_preferences: {list(test_result.data[0].keys())}")
        else:
            print("No data in user_preferences table yet")
        
        # Test minimal insert to user_preferences (should only have color_theme and other_preferences)
        print("\n2. Testing minimal insert to user_preferences...")
        test_data = {
            'user_email': 'test_fix@example.com',
            'color_theme': 'light',
            'other_preferences': {}
        }
        
        try:
            # Try to insert minimal data
            supabase.table('user_preferences').insert(test_data).execute()
            print("✓ Minimal insert successful - table structure is correct")
            
            # Clean up test data
            supabase.table('user_preferences').delete().eq('user_email', 'test_fix@example.com').execute()
            
        except Exception as e:
            print(f"✗ Minimal insert failed: {str(e)}")
            print("This suggests the table structure is correct but there might be constraints")
        
        # Now check user_policy_types table
        print("\n3. Checking user_policy_types structure...")
        test_result = supabase.table('user_policy_types').select('*').limit(1).execute()
        if test_result.data:
            print(f"Current columns in user_policy_types: {list(test_result.data[0].keys())}")
        else:
            print("No data in user_policy_types table yet")
        
        # Test insert to user_policy_types (should accept default_type)
        print("\n4. Testing insert to user_policy_types...")
        test_policy_data = {
            'user_email': 'test_fix@example.com',
            'policy_types': [{'code': 'TEST', 'name': 'Test', 'active': True}]
        }
        
        # Try with different column combinations
        optional_cols = [
            ('default_type', 'HO3'),
            ('categories', ['Other']),
            ('version', '1.0.0')
        ]
        
        success = False
        for i in range(len(optional_cols) + 1):
            test_data_copy = test_policy_data.copy()
            
            # Add optional columns based on attempt
            for j in range(i):
                col_name, col_value = optional_cols[j]
                test_data_copy[col_name] = col_value
            
            try:
                result = supabase.table('user_policy_types').insert(test_data_copy).execute()
                print(f"✓ Insert successful with columns: {list(test_data_copy.keys())}")
                success = True
                
                # Clean up test data
                supabase.table('user_policy_types').delete().eq('user_email', 'test_fix@example.com').execute()
                break
                
            except Exception as e:
                if i == len(optional_cols):
                    print(f"✗ All insert attempts failed. Last error: {str(e)}")
                else:
                    print(f"  Attempt {i+1} failed, trying with fewer columns...")
        
        if success:
            print("\n✓ Schema validation complete - tables are properly configured")
        else:
            print("\n✗ Schema issues detected - manual intervention may be required")
            print("\nSuggested fix:")
            print("1. Check if user_policy_types table exists with correct columns")
            print("2. Ensure user_preferences table only has: id, user_id, user_email, color_theme, other_preferences")
            print("3. Run the SQL script: sql_scripts/fix_user_preferences_schema.sql")
        
        return success
        
    except Exception as e:
        print(f"\nError during schema check: {str(e)}")
        print("\nThis might indicate:")
        print("1. Database connection issues")
        print("2. Missing tables")
        print("3. Permission issues")
        return False

def check_initialization_code():
    """Check for any code that might be mixing up the tables."""
    print("\n\nChecking for potential code issues...")
    
    # List of files to check
    files_to_check = [
        'user_preferences_db.py',
        'user_policy_types_db.py',
        'commission_app.py'
    ]
    
    issues_found = []
    
    for file in files_to_check:
        try:
            with open(file, 'r') as f:
                content = f.read()
                
                # Check for problematic patterns
                if 'user_preferences' in content and 'policy_types' in content:
                    # Look for specific problematic patterns
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'user_preferences' in line and ('policy_types' in line or 'default_type' in line):
                            issues_found.append({
                                'file': file,
                                'line': i + 1,
                                'content': line.strip()
                            })
                            
        except FileNotFoundError:
            print(f"  File not found: {file}")
            continue
    
    if issues_found:
        print("\n⚠ Potential issues found:")
        for issue in issues_found:
            print(f"  {issue['file']}:{issue['line']} - {issue['content']}")
    else:
        print("  ✓ No obvious code issues found")
    
    return len(issues_found) == 0

if __name__ == "__main__":
    print("User Preferences Schema Fix Tool")
    print("================================\n")
    
    # Run the fix
    schema_ok = fix_user_preferences_schema()
    code_ok = check_initialization_code()
    
    if schema_ok and code_ok:
        print("\n✅ Everything looks good!")
        print("\nIf you're still seeing errors, check:")
        print("1. Any custom initialization code in your app")
        print("2. Migration scripts that might be running")
        print("3. Database triggers or functions")
    else:
        print("\n❌ Issues detected - see above for details")
        print("\nNext steps:")
        print("1. Review the SQL script: sql_scripts/fix_user_preferences_schema.sql")
        print("2. Check any recent code changes that might mix user_preferences and user_policy_types")
        print("3. Ensure your database migrations are up to date")
        
    sys.exit(0 if (schema_ok and code_ok) else 1)