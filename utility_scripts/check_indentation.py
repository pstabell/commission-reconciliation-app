#!/usr/bin/env python3
import sys

def check_indentation(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    in_elif_block = False
    elif_indent = 0
    block_start = 0
    issues = []
    
    for i, line in enumerate(lines):
        if line.strip().startswith('elif page =='):
            in_elif_block = True
            elif_indent = len(line) - len(line.lstrip())
            block_start = i + 1
        elif line.strip().startswith('if page ==') or (line.strip() and not line[0].isspace()):
            in_elif_block = False
        
        if in_elif_block and line.strip():
            current_indent = len(line) - len(line.lstrip())
            
            # Check if indentation is not a multiple of 4 spaces from the base
            if current_indent > elif_indent:
                indent_diff = current_indent - elif_indent
                if indent_diff % 4 != 0 or current_indent == elif_indent + 9:  # 9 spaces is a common error
                    issues.append({
                        'line': i + 1,
                        'indent': current_indent,
                        'expected': elif_indent + (((indent_diff - 1) // 4 + 1) * 4),
                        'content': line.rstrip()[:80]
                    })
    
    return issues

if __name__ == "__main__":
    issues = check_indentation('commission_app.py')
    
    print(f"Found {len(issues)} indentation issues:\n")
    
    for issue in issues[:50]:  # Show first 50 issues
        print(f"Line {issue['line']}: Has {issue['indent']} spaces, expected {issue['expected']}")
        print(f"  Content: {repr(issue['content'])}")
        print()