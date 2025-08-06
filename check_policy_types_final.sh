#!/bin/bash

# Supabase credentials
SUPABASE_URL="https://ddiahkzvmymacejqlnvc.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkaWFoa3p2bXltYWNlanFsbnZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExNjU2MTUsImV4cCI6MjA2Njc0MTYxNX0.KgBeoRKsQO6WsQ0TzlC772fY8gAoXJonuS4M1Mi3BLs"

echo "Checking policy types in the 'policies' table..."
echo "================================================"

# Get all policies
curl -s -X GET "${SUPABASE_URL}/rest/v1/policies?select=Policy%20Type" \
     -H "apikey: ${SUPABASE_ANON_KEY}" \
     -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
     -H "Content-Type: application/json" > /tmp/policy_types_only.json

# Analyze the data
if [ -s /tmp/policy_types_only.json ]; then
    python3 -c "
import json
from collections import Counter

with open('/tmp/policy_types_only.json') as f:
    data = json.load(f)

print(f'Total policies in database: {len(data)}')

# Extract policy types
policy_types = [item.get('Policy Type') for item in data]

# Count occurrences
counts = Counter(policy_types)

print('\\n=== POLICY TYPE COUNTS ===')
# Sort with None values first
sorted_items = []
none_count = 0
for policy_type, count in counts.items():
    if policy_type is None:
        none_count = count
    else:
        sorted_items.append((policy_type, count))

# Display None first if it exists
if none_count > 0:
    print(f'NULL/None: {none_count}')

# Then display the rest sorted
for policy_type, count in sorted(sorted_items):
    if policy_type == '':
        print(f'Empty string: {count}')
    else:
        print(f'{policy_type}: {count}')

# Check specifically for HOME and AUTO
print('\\n=== SPECIFIC CHECKS FOR HOME AND AUTO ===')
home_count = sum(1 for pt in policy_types if pt == 'HOME')
auto_count = sum(1 for pt in policy_types if pt == 'AUTO')
print(f'Exact match HOME: {home_count}')
print(f'Exact match AUTO: {auto_count}')

# Case-insensitive check
home_case_insensitive = sum(1 for pt in policy_types if pt and 'home' in str(pt).lower())
auto_case_insensitive = sum(1 for pt in policy_types if pt and 'auto' in str(pt).lower())
print(f'\\nContains \"home\" (case-insensitive): {home_case_insensitive}')
print(f'Contains \"auto\" (case-insensitive): {auto_case_insensitive}')

# Check for specific variations
autop_count = sum(1 for pt in policy_types if pt == 'AUTOP')
homep_count = sum(1 for pt in policy_types if pt == 'HOMEP')
print(f'\\nAUTOP count: {autop_count}')
print(f'HOMEP count: {homep_count}')

# Show all unique values
print('\\n=== ALL UNIQUE POLICY TYPES ===')
unique_types = set(policy_types)
sorted_unique = []
has_none = False
has_empty = False

for pt in unique_types:
    if pt is None:
        has_none = True
    elif pt == '':
        has_empty = True
    else:
        sorted_unique.append(pt)

if has_none:
    print('None (null)')
if has_empty:
    print('\"\" (empty string)')
for pt in sorted(sorted_unique):
    print(f'\"{pt}\"')

# Summary
print('\\n=== SUMMARY ===')
print(f'Total unique policy types: {len(unique_types)}')
print(f'Total policies: {len(data)}')
print(f'Policies with NULL policy type: {none_count}')
print(f'\\nThe database has {home_count} HOME and {auto_count} AUTO policy types.')
print(f'However, there are {autop_count} AUTOP policies which might be automobile policies.')
"
    
    # Clean up
    rm /tmp/policy_types_only.json
else
    echo "No data received or error occurred."
fi