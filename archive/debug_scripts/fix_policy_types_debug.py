"""
Add debug logging to user_policy_types_db.py to trace the issue
"""

import os

# Read the current file
file_path = 'user_policy_types_db.py'
with open(file_path, 'r') as f:
    content = f.read()

# Add debug logging after line 39 where it checks response.data
debug_code = """
            if response.data and len(response.data) > 0:
                types_data = response.data[0]
                # DEBUG: Print what we got from database
                print(f"DEBUG get_user_policy_types: Found data for {user_email}")
                print(f"DEBUG: policy_types type = {type(types_data.get('policy_types'))}")
                print(f"DEBUG: policy_types value = {types_data.get('policy_types')}")
                
                # Build result with only existing columns
                result = {
                    'policy_types': types_data.get('policy_types', [])
                }
"""

# Find the location to insert
import_index = content.find("if response.data and len(response.data) > 0:")
if import_index != -1:
    # Find the end of the line
    line_end = content.find('\n', import_index)
    next_line_start = line_end + 1
    
    # Find the next line that starts with "types_data = response.data[0]"
    types_data_index = content.find("types_data = response.data[0]", next_line_start)
    if types_data_index != -1:
        # Replace the section
        end_of_section = content.find("result = {", types_data_index)
        if end_of_section != -1:
            # Find the closing brace of the result dict
            closing_brace = content.find("}", end_of_section)
            if closing_brace != -1:
                # Replace this section with our debug version
                new_content = (
                    content[:import_index] + 
                    debug_code.strip() + 
                    content[closing_brace + 1:]
                )
                
                # Write back
                with open(file_path + '.debug', 'w') as f:
                    f.write(new_content)
                print("Created debug version at user_policy_types_db.py.debug")
                print("To apply: cp user_policy_types_db.py.debug user_policy_types_db.py")
            else:
                print("Could not find closing brace")
        else:
            print("Could not find result = {")
    else:
        print("Could not find types_data line")
else:
    print("Could not find response.data check")