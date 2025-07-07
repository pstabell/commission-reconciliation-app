#!/usr/bin/env python3
"""
Fix indentation for Dashboard section in commission_app.py
"""

def fix_dashboard_indentation():
    # Read the file
    with open('commission_app.py', 'r') as f:
        lines = f.readlines()
    
    # Fix indentation for lines 604-706 (0-indexed: 603-705)
    # We need to add 4 spaces to lines that need proper Dashboard indentation
    
    start_line = 603  # 0-indexed line 604
    end_line = 705    # 0-indexed line 706
    
    for i in range(start_line, min(end_line + 1, len(lines))):
        line = lines[i]
        if line.strip():  # Only modify non-empty lines
            # Count current indentation
            current_indent = len(line) - len(line.lstrip())
            # Add 4 spaces for proper Dashboard block indentation
            lines[i] = '    ' + line
        else:
            # Empty lines stay empty
            lines[i] = line
    
    # Write back to file
    with open('commission_app.py', 'w') as f:
        f.writelines(lines)
    
    print(f"Fixed indentation for lines {start_line + 1} to {end_line + 1}")

if __name__ == "__main__":
    fix_dashboard_indentation()