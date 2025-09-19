#!/usr/bin/env python3
"""Check the exported Excel file to see Johnson & Johnson associations."""

import pandas as pd

# Read the exported file
file_path = "./PRIVATE mode contacts_export_20250919_134134.xlsx"

# Read all sheets
all_sheets = pd.read_excel(file_path, sheet_name=None)

print("=== EXCEL FILE CONTENTS ===\n")

# Check carriers
if 'Carriers' in all_sheets:
    carriers_df = all_sheets['Carriers']
    print(f"Carriers sheet: {len(carriers_df)} rows")
    # Look for J&J carriers
    jj_carriers = ['Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston']
    found_carriers = carriers_df[carriers_df['carrier_name'].isin(jj_carriers)]
    print(f"\nJohnson & Johnson carriers found: {len(found_carriers)}")
    if len(found_carriers) > 0:
        print(found_carriers[['carrier_name', 'status']])

# Check MGAs
if 'MGAs' in all_sheets:
    mgas_df = all_sheets['MGAs']
    print(f"\n\nMGAs sheet: {len(mgas_df)} rows")
    # Look for Johnson & Johnson
    jj_mga = mgas_df[mgas_df['mga_name'].str.contains('Johnson', na=False)]
    print(f"\nJohnson & Johnson MGA found: {len(jj_mga)}")
    if len(jj_mga) > 0:
        print(jj_mga[['mga_name', 'status']])

# Check commission rules
if 'Commission Rules' in all_sheets:
    rules_df = all_sheets['Commission Rules']
    print(f"\n\nCommission Rules sheet: {len(rules_df)} rows")
    
    # Look for rules with Johnson & Johnson
    jj_rules = rules_df[rules_df['mga_name'].str.contains('Johnson', na=False)]
    print(f"\nRules with Johnson & Johnson MGA: {len(jj_rules)}")
    if len(jj_rules) > 0:
        print("\nCarriers associated with Johnson & Johnson:")
        print(jj_rules[['carrier_name', 'mga_name', 'policy_type', 'commission_rate']].to_string())
    
    # Also check if those carriers have rules without J&J
    print("\n\nChecking all rules for J&J carriers:")
    jj_carrier_rules = rules_df[rules_df['carrier_name'].isin(jj_carriers)]
    print(f"Total rules for J&J carriers: {len(jj_carrier_rules)}")
    
    # Group by carrier and MGA
    if len(jj_carrier_rules) > 0:
        summary = jj_carrier_rules.groupby(['carrier_name', 'mga_name']).size().reset_index(name='rule_count')
        print("\nSummary of rules by carrier and MGA:")
        print(summary.to_string())