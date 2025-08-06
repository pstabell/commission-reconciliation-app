#!/bin/bash

# Supabase credentials
SUPABASE_URL="https://ddiahkzvmymacejqlnvc.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkaWFoa3p2bXltYWNlanFsbnZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExNjU2MTUsImV4cCI6MjA2Njc0MTYxNX0.KgBeoRKsQO6WsQ0TzlC772fY8gAoXJonuS4M1Mi3BLs"

echo "Checking policy types in the 'policies' table..."
echo "================================================"

# First, let's get a sample to see the structure
echo -e "\nSample record to see available columns:"
curl -s -X GET "${SUPABASE_URL}/rest/v1/policies?limit=1" \
     -H "apikey: ${SUPABASE_ANON_KEY}" \
     -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
     -H "Content-Type: application/json" | python3 -m json.tool

echo -e "\n\nFetching all policies to count policy types..."
echo "=============================================="

# Get all policies - first check what policy type column is called
curl -s -X GET "${SUPABASE_URL}/rest/v1/policies?select=*&limit=1" \
     -H "apikey: ${SUPABASE_ANON_KEY}" \
     -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
     -H "Content-Type: application/json" > /tmp/sample_policy.json

# Check column names
echo "Available columns in policies table:"
python3 -c "
import json
with open('/tmp/sample_policy.json') as f:
    data = json.load(f)
    if data and len(data) > 0:
        print('Columns:', list(data[0].keys()))
"

# Now get all policy type data - looking for columns that might contain policy type
curl -s -X GET "${SUPABASE_URL}/rest/v1/policies" \
     -H "apikey: ${SUPABASE_ANON_KEY}" \
     -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
     -H "Content-Type: application/json" > /tmp/all_policies.json

# Analyze the data
if [ -s /tmp/all_policies.json ]; then
    echo -e "\nAnalyzing policy data..."
    
    python3 -c "
import json
from collections import Counter

with open('/tmp/all_policies.json') as f:
    data = json.load(f)

print(f'Total policies in database: {len(data)}')

# Check for various possible column names for policy type
possible_columns = ['policy_type', 'Policy Type', 'PolicyType', 'Type', 'type', 'Product', 'product']
found_column = None

if data and len(data) > 0:
    for col in possible_columns:
        if col in data[0]:
            found_column = col
            break
    
    if not found_column:
        print('\\nCould not find policy type column. Available columns:')
        print(list(data[0].keys())[:10])  # Show first 10 columns
    else:
        print(f'\\nFound policy type column: {found_column}')
        
        # Extract policy types
        policy_types = [item.get(found_column) for item in data]
        
        # Count occurrences
        counts = Counter(policy_types)
        
        print('\\n=== POLICY TYPE COUNTS ===')
        for policy_type, count in sorted(counts.items()):
            if policy_type is None:
                print(f'NULL/None: {count}')
            elif policy_type == '':
                print(f'Empty string: {count}')
            else:
                print(f'{policy_type}: {count}')
        
        # Check specifically for HOME and AUTO
        print('\\n=== SPECIFIC CHECKS ===')
        home_count = sum(1 for pt in policy_types if pt == 'HOME')
        auto_count = sum(1 for pt in policy_types if pt == 'AUTO')
        print(f'HOME count: {home_count}')
        print(f'AUTO count: {auto_count}')
        
        # Case-insensitive check
        home_case_insensitive = sum(1 for pt in policy_types if pt and 'home' in str(pt).lower())
        auto_case_insensitive = sum(1 for pt in policy_types if pt and 'auto' in str(pt).lower())
        print(f'\\nCase-insensitive HOME count: {home_case_insensitive}')
        print(f'Case-insensitive AUTO count: {auto_case_insensitive}')
        
        # Show all unique values
        print('\\n=== ALL UNIQUE POLICY TYPES ===')
        unique_types = set(policy_types)
        for pt in sorted(unique_types, key=lambda x: (x is None, x == '', str(x))):
            if pt is None:
                print('None (null)')
            elif pt == '':
                print('\"\" (empty string)')
            else:
                print(f'\"{pt}\"')
"
    
    # Clean up
    rm /tmp/all_policies.json /tmp/sample_policy.json
else
    echo "No data received or error occurred."
fi