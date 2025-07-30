#!/usr/bin/env python3
"""
Manual analysis script - run the commission app and use this to analyze the data.
Copy the results from the data editor and analyze them.
"""

import os
from datetime import datetime
from collections import defaultdict

# Instructions for manual analysis
print("=" * 80)
print("MANUAL ANALYSIS INSTRUCTIONS FOR -IMPORT TRANSACTIONS")
print("=" * 80)
print()
print("1. Open the Sales Commission App")
print("2. Go to the Policy Ledger page")
print("3. In the search box, type: -IMPORT")
print("4. This will filter to show only transactions with '-IMPORT' in the Transaction ID")
print()
print("5. Look for transactions where BOTH of these columns have values:")
print("   - 'Agent Estimated Comm $'")
print("   - 'Agent Paid Amount (STMT)'")
print()
print("6. You can export the filtered data to Excel for easier analysis:")
print("   - Click the 'Export to Excel' button")
print("   - Open the Excel file")
print("   - Sort/filter to find double entries")
print()
print("7. Things to check:")
print("   a) Total count of -IMPORT transactions")
print("   b) Count of transactions with values in BOTH commission fields")
print("   c) Are the amounts usually the same or different?")
print("   d) Do they occur on specific dates?")
print("   e) Are they concentrated on specific customers?")
print()
print("SQL Query to use if you have database access:")
print("-" * 80)
print("""
SELECT 
    "Transaction ID",
    "Customer",
    "Agent Estimated Comm $",
    "Agent Paid Amount (STMT)",
    "Stmt Paid Date",
    "X Date"
FROM policies
WHERE "Transaction ID" LIKE '%-IMPORT'
  AND "Agent Estimated Comm $" IS NOT NULL 
  AND "Agent Estimated Comm $" != 0
  AND "Agent Paid Amount (STMT)" IS NOT NULL 
  AND "Agent Paid Amount (STMT)" != 0
ORDER BY "Customer", "Stmt Paid Date";
""")
print("-" * 80)
print()
print("This query will find all -IMPORT transactions with double entries.")
print("=" * 80)