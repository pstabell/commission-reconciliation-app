#!/usr/bin/env python3
"""
Remove all security features from commission_app.py
"""

import re

def remove_security_features():
    with open('commission_app.py', 'r') as f:
        content = f.read()
    
    # Remove entire security function definitions
    security_functions = [
        'get_database_fingerprint',
        'create_protection_lock', 
        'verify_database_integrity',
        'emergency_database_freeze',
        'protect_backup_metadata',
        'restore_backup_metadata',
        'reconstruct_backup_history',
        'monitor_schema_changes',
        'show_recovery_options',
        'show_protection_status'
    ]
    
    # Remove function definitions
    for func in security_functions:
        # Match function definition and its entire body
        pattern = rf'(\n    def {func}\(.*?\):.*?)(?=\n    (?:def|\w|#|$))'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Remove security-related comments and sections
    security_sections = [
        r'\n    # ======\n    # BULLETPROOF DATABASE PROTECTION.*?# ======',
        r'\n    # ======\n    # ENHANCED BACKUP METADATA PROTECTION.*?# ======',
        r'\n    # ======\n    # PHASE \d+:.*?# ======',
        r'\n    # ======\n    # END PHASE \d+:.*?# ======',
        r'\n    # DATABASE PROTECTION & RECOVERY CENTER.*?\n',
        r'# Configure logging for database protection system.*?\n'
    ]
    
    for pattern in security_sections:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Remove integrity check calls and critical messages
    integrity_checks = [
        r'# Check database integrity first.*?st\.stop\(\).*?\n',
        r'if not verify_database_integrity\(\):.*?st\.stop\(\).*?\n',
        r'# Verify database integrity.*?st\.session_state\["integrity_verified"\] = True.*?\n',
        r'if "integrity_verified" not in st\.session_state:.*?st\.stop\(\).*?\n',
        r'st\.error\("🚨 CRITICAL:.*?"\).*?\n',
        r'st\.error\("Please check.*?"\).*?\n',
        r'emergency_backup = emergency_database_freeze\(\).*?\n',
        r'monitor_schema_changes\(\).*?\n',
        r'show_protection_status\(\).*?\n',
        r'protect_backup_metadata\(\).*?\n',
        r'create_protection_lock\(\).*?\n'
    ]
    
    for pattern in integrity_checks:
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.MULTILINE)
    
    # Remove security UI sections
    ui_sections = [
        r'# --- Database Protection & Recovery Center ---.*?(?=# ---|\n    elif|\n    if|\Z)',
        r'st\.markdown\("### 🛡️ Database Protection Status"\).*?(?=\n    st\.|\n    # ---|\n    elif|\n    if|\Z)',
        r'with st\.expander\("🚨 Database Recovery Center.*?"\):.*?(?=\n    # ---|\n    elif|\n    if|\Z)',
        r'# Show recovery options UI.*?\n',
        r'# Show the recovery options UI in the sidebar.*?\n'
    ]
    
    for pattern in ui_sections:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Remove logging configuration for database protection
    content = re.sub(
        r'# Configure logging for database protection system\nlogging\.basicConfig\(.*?\)\n',
        '', 
        content, 
        flags=re.DOTALL
    )
    
    # Clean up extra blank lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Write cleaned content
    with open('commission_app.py', 'w') as f:
        f.write(content)
    
    print("Security features removed successfully!")

if __name__ == "__main__":
    remove_security_features()