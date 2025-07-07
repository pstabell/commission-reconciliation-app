#!/usr/bin/env python3
"""
Remove remaining security references from commission_app.py
"""

import re

def remove_remaining_security():
    with open('commission_app.py', 'r') as f:
        lines = f.readlines()
    
    # Remove specific line ranges that contain security code
    security_ranges = []
    in_security_block = False
    start_line = 0
    
    for i, line in enumerate(lines):
        # Look for security-related blocks
        if any(keyword in line for keyword in [
            "protection lock", "fingerprint", "recovery", "freeze",
            "Protection Status", "Recovery Center", "get_database_fingerprint",
            "show_recovery_options", "verify_database_integrity",
            "database_protection.lock", "CRITICAL:", "unauthorized"
        ]):
            if not in_security_block:
                start_line = i
                in_security_block = True
        elif in_security_block and (line.strip() == '' or not line.startswith(' ' * 8)):
            # End of indented block
            security_ranges.append((start_line, i))
            in_security_block = False
    
    # Remove lines in reverse order to maintain indices
    for start, end in reversed(security_ranges):
        del lines[start:end]
    
    # Additional cleanup - remove specific patterns
    cleaned_lines = []
    skip_next = False
    
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
            
        # Skip lines with security keywords
        if any(keyword in line for keyword in [
            "with backup protection", "protection lock", "fingerprint",
            "recovery_options", "Protection Status", "Recovery Center",
            "database_protection.lock", "show_recovery_options()"
        ]):
            # Check if it's part of a success message we can clean
            if "with backup protection" in line:
                line = line.replace(" safely with backup protection", "")
                line = line.replace(" with backup protection", "")
            elif "show_recovery_options()" in line:
                continue
            else:
                continue
        
        cleaned_lines.append(line)
    
    # Write cleaned content
    with open('commission_app.py', 'w') as f:
        f.writelines(cleaned_lines)
    
    print("Remaining security features removed!")

if __name__ == "__main__":
    remove_remaining_security()