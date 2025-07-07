#!/usr/bin/env python3
"""
Remove orphaned markdown content from commission_app.py
"""

def remove_orphaned_markdown():
    with open('commission_app.py', 'r') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    skip = False
    
    for i, line in enumerate(lines):
        # Start skipping when we hit the orphaned markdown
        if line.strip().startswith("**Below are the formulas"):
            skip = True
            continue
        
        # Stop skipping when we find a line that starts a proper code section
        if skip and (line.strip().startswith("# --- Ensure") or 
                    line.strip().startswith("with engine.begin()") or
                    line.strip().startswith("def ") or
                    line.strip().startswith("if ") or
                    line.strip().startswith("elif ") or
                    line.strip().startswith("st.")):
            skip = False
        
        if not skip:
            cleaned_lines.append(line)
    
    # Write cleaned content
    with open('commission_app.py', 'w') as f:
        f.writelines(cleaned_lines)
    
    print("Orphaned markdown removed!")

if __name__ == "__main__":
    remove_orphaned_markdown()