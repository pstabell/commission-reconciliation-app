"""
Analyze the user_preferences column error without database connection.
"""

import os
import re

def analyze_code_issues():
    """Analyze code for potential table confusion issues."""
    print("Analyzing code for user_preferences column issues...")
    print("=" * 60)
    
    # Files to analyze
    files_to_check = {
        'user_preferences_db.py': 'User Preferences DB Module',
        'user_policy_types_db.py': 'User Policy Types DB Module',
        'commission_app.py': 'Main Commission App',
        'database_utils.py': 'Database Utilities'
    }
    
    issues = []
    
    for file_path, description in files_to_check.items():
        if not os.path.exists(file_path):
            print(f"\n❌ {description} ({file_path}) not found")
            continue
            
        print(f"\n📄 Analyzing {description} ({file_path})...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Check for problematic patterns
        for i, line in enumerate(lines):
            line_num = i + 1
            
            # Pattern 1: user_preferences table with policy-related columns
            if 'user_preferences' in line and any(col in line for col in ['default_type', 'policy_types', 'categories', 'version']):
                issues.append({
                    'file': file_path,
                    'line': line_num,
                    'issue': 'user_preferences table referenced with policy-related columns',
                    'content': line.strip()
                })
            
            # Pattern 2: INSERT into user_preferences with wrong columns
            if re.search(r'(insert|INSERT).*user_preferences', line) and any(col in line for col in ['default_type', 'policy_types']):
                issues.append({
                    'file': file_path,
                    'line': line_num,
                    'issue': 'INSERT into user_preferences with policy columns',
                    'content': line.strip()
                })
            
            # Pattern 3: Confused table references
            if 'table(\'user_preferences\')' in line and 'policy_types' in lines[max(0, i-5):min(len(lines), i+5)]:
                # Check context around this line
                context_start = max(0, i-5)
                context_end = min(len(lines), i+5)
                context = '\n'.join(lines[context_start:context_end])
                
                if 'policy_types' in context or 'default_type' in context:
                    issues.append({
                        'file': file_path,
                        'line': line_num,
                        'issue': 'Possible table confusion in context',
                        'content': line.strip(),
                        'context': context
                    })
    
    # Report findings
    print("\n" + "=" * 60)
    print("ANALYSIS RESULTS")
    print("=" * 60)
    
    if issues:
        print(f"\n⚠️  Found {len(issues)} potential issues:\n")
        for idx, issue in enumerate(issues, 1):
            print(f"{idx}. {issue['file']}:{issue['line']}")
            print(f"   Issue: {issue['issue']}")
            print(f"   Code: {issue['content']}")
            if 'context' in issue:
                print(f"   Context:\n{issue['context']}")
            print()
    else:
        print("\n✅ No obvious code issues found!")
    
    # Check table schemas in SQL files
    print("\n" + "=" * 60)
    print("CHECKING SQL SCHEMA FILES")
    print("=" * 60)
    
    sql_files = [
        'sql_scripts/create_user_settings_tables.sql',
        'sql_scripts/migrate_settings_to_user_specific.sql'
    ]
    
    for sql_file in sql_files:
        if os.path.exists(sql_file):
            print(f"\n📄 {sql_file}:")
            with open(sql_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find user_preferences table definition
            if 'CREATE TABLE' in content and 'user_preferences' in content:
                # Extract the table definition
                start = content.find('CREATE TABLE IF NOT EXISTS user_preferences')
                if start == -1:
                    start = content.find('CREATE TABLE user_preferences')
                
                if start != -1:
                    end = content.find(');', start)
                    if end != -1:
                        table_def = content[start:end+2]
                        print("   user_preferences table schema:")
                        print("   " + "\n   ".join(table_def.split('\n')[:10]))  # First 10 lines
            
            # Check for INSERTs into user_preferences
            insert_matches = re.findall(r'INSERT INTO user_preferences.*?;', content, re.DOTALL)
            if insert_matches:
                for match in insert_matches:
                    if 'default_type' in match or 'policy_types' in match:
                        print(f"\n   ⚠️  Found INSERT with policy columns:")
                        print("   " + match[:200] + "..." if len(match) > 200 else "   " + match)
    
    # Provide recommendations
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    print("\n1. The user_preferences table should only have these columns:")
    print("   - id (UUID)")
    print("   - user_id (UUID)")
    print("   - user_email (TEXT)")
    print("   - color_theme (TEXT)")
    print("   - other_preferences (JSONB)")
    print("   - created_at, updated_at (TIMESTAMP)")
    
    print("\n2. The user_policy_types table should have:")
    print("   - id (UUID)")
    print("   - user_id (UUID)")
    print("   - user_email (TEXT)")
    print("   - policy_types (JSONB) - array of policy type objects")
    print("   - default_type (TEXT) - the default policy type code")
    print("   - categories (JSONB) - array of category names")
    print("   - version (TEXT)")
    print("   - created_at, updated_at (TIMESTAMP)")
    
    print("\n3. To fix the issue:")
    print("   a) Check if any code is trying to insert 'default_type' into user_preferences")
    print("   b) Ensure user_preferences only deals with color_theme and other_preferences")
    print("   c) All policy-related data should go to user_policy_types table")
    
    return len(issues) == 0

if __name__ == "__main__":
    analyze_code_issues()