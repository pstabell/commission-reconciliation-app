"""
Script to audit all pages in commission_app.py for empty data handling
"""

import re

# Pages that need empty data handling
PAGES_TO_AUDIT = [
    "Dashboard",
    "Add New Policy Transaction", 
    "Edit Policy Transactions",
    "All Policy Transactions",
    "Reports",
    "Reconciliation",
    "Admin Panel",
    "Tools",
    "Search"
]

# Common patterns that indicate data access without validation
RISKY_PATTERNS = [
    r"all_data\[.*?\]",  # Direct column access
    r"\.str\.",  # String operations on columns
    r"\.groupby\(",  # Groupby operations
    r"\.merge\(",  # Merge operations
    r"\.loc\[",  # Loc access
    r"\.iloc\[",  # Iloc access
    r"len\(all_data\)",  # Length checks that might fail
    r"for.*in.*all_data",  # Iterations over data
]

def audit_page(content: str, page_name: str):
    """Audit a specific page for empty data handling issues."""
    print(f"\n{'='*60}")
    print(f"AUDITING: {page_name}")
    print(f"{'='*60}")
    
    # Find the page section
    page_pattern = f'page == "{page_name}"'
    page_match = re.search(page_pattern, content)
    
    if not page_match:
        print(f"⚠️  Page '{page_name}' not found in code")
        return
    
    # Extract the page section (rough approximation)
    start_pos = page_match.start()
    # Find next 'elif page ==' or end of main()
    next_page_match = re.search(r'elif page ==|def \w+\(', content[start_pos + 100:])
    if next_page_match:
        end_pos = start_pos + 100 + next_page_match.start()
    else:
        end_pos = len(content)
    
    page_content = content[start_pos:end_pos]
    
    # Check for empty data handling
    has_empty_check = bool(re.search(r'if.*all_data\.empty|if.*\.empty\(\)|No data found', page_content))
    
    if has_empty_check:
        print("✅ Has some empty data handling")
    else:
        print("❌ No empty data handling found")
    
    # Find risky patterns
    issues_found = []
    for pattern in RISKY_PATTERNS:
        matches = re.findall(pattern, page_content)
        if matches:
            issues_found.append(f"  - Found {len(matches)} instances of: {pattern}")
    
    if issues_found:
        print("\n⚠️  Potential issues without data validation:")
        for issue in issues_found[:5]:  # Show first 5 issues
            print(issue)
    
    # Check if page loads data
    loads_data = bool(re.search(r'load_policies_data\(\)', page_content))
    if loads_data:
        print(f"\n📊 Page loads data via load_policies_data()")

if __name__ == "__main__":
    # Read the commission_app.py file
    with open('commission_app.py', 'r') as f:
        content = f.read()
    
    print("COMMISSION APP - EMPTY DATA HANDLING AUDIT")
    print("=" * 60)
    
    for page in PAGES_TO_AUDIT:
        audit_page(content, page)
    
    print("\n\nSUMMARY")
    print("=" * 60)
    print("Most pages directly access data without checking if it's empty.")
    print("This causes errors when new users have no data.")
    print("\nRECOMMENDATION: Import and use data_validation_utils.py")