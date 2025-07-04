#!/usr/bin/env python3
"""
Fix orphaned code blocks in commission_app.py
"""

def fix_orphaned_code():
    with open('commission_app.py', 'r') as f:
        lines = f.readlines()
    
    # Find the orphaned code block starting at line 418 (0-indexed: 417)
    # This appears to be code that should be inside a function but is at the wrong indentation
    cleaned_lines = []
    skip = False
    
    for i, line in enumerate(lines):
        # Start skipping at the orphaned code
        if i == 417 and line.strip().startswith("if df is not None:"):
            skip = True
            continue
        
        # Stop skipping when we find a line that's not indented (new section)
        if skip and not line.startswith(' ') and line.strip() != '':
            skip = False
        
        if not skip:
            cleaned_lines.append(line)
    
    # Write cleaned content
    with open('commission_app.py', 'w') as f:
        f.writelines(cleaned_lines)
    
    print("Orphaned code removed!")

if __name__ == "__main__":
    fix_orphaned_code()