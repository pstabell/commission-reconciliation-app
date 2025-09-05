#!/bin/bash

# Supabase credentials
SUPABASE_URL="https://ddiahkzvmymacejqlnvc.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkaWFoa3p2bXltYWNlanFsbnZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExNjU2MTUsImV4cCI6MjA2Njc0MTYxNX0.KgBeoRKsQO6WsQ0TzlC772fY8gAoXJonuS4M1Mi3BLs"

echo "Fetching all transactions from Supabase..."
echo "====================================="

# First, let's get a sample of transactions to see the structure
curl -s -X GET "${SUPABASE_URL}/rest/v1/transactions?limit=5" \
     -H "apikey: ${SUPABASE_ANON_KEY}" \
     -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
     -H "Content-Type: application/json" | python3 -m json.tool

echo -e "\n\nNow fetching all transactions to count policy types..."
echo "====================================="

# Get all transactions and extract policy_type field
curl -s -X GET "${SUPABASE_URL}/rest/v1/transactions?select=policy_type" \
     -H "apikey: ${SUPABASE_ANON_KEY}" \
     -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
     -H "Content-Type: application/json" > /tmp/policy_types.json

# Check if we got data
if [ -s /tmp/policy_types.json ]; then
    echo "Data received. Analyzing policy types..."
    
    # Count total records
    total_count=$(python3 -c "import json; data = json.load(open('/tmp/policy_types.json')); print(len(data))")
    echo "Total transactions: $total_count"
    
    # Count policy types
    echo -e "\nPolicy Type Counts:"
    python3 -c "
import json
from collections import Counter

with open('/tmp/policy_types.json') as f:
    data = json.load(f)

# Extract policy types
policy_types = [item.get('policy_type') for item in data]

# Count occurrences
counts = Counter(policy_types)

# Display counts
for policy_type, count in sorted(counts.items()):
    if policy_type is None:
        print(f'NULL/None: {count}')
    else:
        print(f'{policy_type}: {count}')

# Check specifically for HOME and AUTO
print('\n=== SPECIFIC CHECKS ===')
home_count = sum(1 for pt in policy_types if pt == 'HOME')
auto_count = sum(1 for pt in policy_types if pt == 'AUTO')
print(f'HOME count: {home_count}')
print(f'AUTO count: {auto_count}')

# Case-insensitive check
home_case_insensitive = sum(1 for pt in policy_types if pt and 'home' in pt.lower())
auto_case_insensitive = sum(1 for pt in policy_types if pt and 'auto' in pt.lower())
print(f'\\nCase-insensitive HOME count: {home_case_insensitive}')
print(f'Case-insensitive AUTO count: {auto_case_insensitive}')
"
    
    # Clean up
    rm /tmp/policy_types.json
else
    echo "No data received or error occurred."
fi