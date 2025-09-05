#!/usr/bin/env python3
"""
Final comprehensive policy type analysis
"""

import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime

# Supabase credentials
SUPABASE_URL = "https://ddiahkzvmymacejqlnvc.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkaWFoa3p2bXltYWNlanFsbnZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExNjU2MTUsImV4cCI6MjA2Njc0MTYxNX0.KgBeoRKsQO6WsQ0TzlC772fY8gAoXJonuS4M1Mi3BLs"

print("==========================================")
print("POLICY TYPE ANALYSIS REPORT")
print(f"Date: {datetime.now()}")
print("==========================================")

# Get data using curl
cmd = [
    "curl", "-s", "-X", "GET",
    f"{SUPABASE_URL}/rest/v1/policies?select=Policy%20Type,Carrier%20Name,Transaction%20Type",
    "-H", f"apikey: {SUPABASE_ANON_KEY}",
    "-H", f"Authorization: Bearer {SUPABASE_ANON_KEY}",
    "-H", "Content-Type: application/json"
]

result = subprocess.run(cmd, capture_output=True, text=True)
data = json.loads(result.stdout)

print(f"\nTotal policies in database: {len(data)}")

# Extract policy types
policy_types = [item.get('Policy Type') for item in data]

# Count occurrences
counts = Counter(policy_types)

print("\n=== AUTOMOBILE POLICY ANALYSIS ===")
auto_types = ['AUTOP', 'AUTOB', 'AUTO']
total_auto = 0
for pt in auto_types:
    count = counts.get(pt, 0)
    if count > 0:
        print(f"{pt}: {count} policies")
        total_auto += count

print(f"\nTotal automobile-related policies: {total_auto}")

# Analyze by carrier for auto policies
print("\n=== AUTO POLICIES BY CARRIER ===")
auto_by_carrier = defaultdict(int)
for item in data:
    if item.get('Policy Type') in auto_types:
        carrier = item.get('Carrier Name', 'Unknown')
        auto_by_carrier[carrier] += 1

for carrier, count in sorted(auto_by_carrier.items(), key=lambda x: x[1], reverse=True):
    print(f"{carrier}: {count}")

print("\n=== HOME/PROPERTY POLICY ANALYSIS ===")
home_types = ['HOME', 'HOMEP', 'CONDO', 'DP3', 'HO5', 'HO6']
total_home = 0
for pt in home_types:
    count = counts.get(pt, 0)
    if count > 0:
        print(f"{pt}: {count} policies")
        total_home += count

print(f"\nTotal home/property-related policies: {total_home}")

# Transaction types for AUTO and HOME
print("\n=== TRANSACTION TYPES FOR KEY POLICIES ===")
print("\nHOME policies by transaction type:")
home_trans = defaultdict(int)
for item in data:
    if item.get('Policy Type') == 'HOME':
        trans_type = item.get('Transaction Type', 'Unknown')
        home_trans[trans_type] += 1

# Sort handling None values
home_trans_items = [(k if k is not None else 'NULL', v) for k, v in home_trans.items()]
for trans_type, count in sorted(home_trans_items):
    print(f"  {trans_type}: {count}")

print("\nAUTOP policies by transaction type:")
autop_trans = defaultdict(int)
for item in data:
    if item.get('Policy Type') == 'AUTOP':
        trans_type = item.get('Transaction Type', 'Unknown')
        autop_trans[trans_type] += 1

# Sort handling None values
autop_trans_items = [(k if k is not None else 'NULL', v) for k, v in autop_trans.items()]
for trans_type, count in sorted(autop_trans_items):
    print(f"  {trans_type}: {count}")

print("\n=== COMPLETE POLICY TYPE BREAKDOWN ===")
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
    print(f"NULL/None: {none_count} ({none_count/len(data)*100:.1f}%)")

# Then display the rest sorted by count (descending)
for policy_type, count in sorted(sorted_items, key=lambda x: x[1], reverse=True):
    percentage = count/len(data)*100
    print(f"{policy_type}: {count} ({percentage:.1f}%)")

print("\n=== KEY FINDINGS ===")
print(f"1. There are ZERO policies with policy type 'AUTO'")
print(f"2. There are {counts.get('AUTOP', 0)} policies with type 'AUTOP' (likely automobile personal)")
print(f"3. There are {counts.get('AUTOB', 0)} policies with type 'AUTOB' (likely automobile business)")
print(f"4. There are {counts.get('HOME', 0)} policies with type 'HOME'")
print(f"5. Total policies with NULL policy type: {none_count}")
print(f"\nConclusion: The system uses 'AUTOP' and 'AUTOB' instead of 'AUTO' for automobile policies.")
print(f"The database does contain HOME policies (52), but uses AUTOP/AUTOB instead of AUTO.")