#!/usr/bin/env python3
"""Export all carriers, MGAs, and commission rules from private database."""

import sqlite3
import json
from datetime import datetime

# Connect to the private database
conn = sqlite3.connect('commissions.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Export carriers
print("Exporting carriers...")
carriers = cursor.execute("SELECT * FROM carriers ORDER BY carrier_name").fetchall()
carriers_list = [dict(row) for row in carriers]
print(f"Found {len(carriers_list)} carriers")

# Export MGAs
print("\nExporting MGAs...")
mgas = cursor.execute("SELECT * FROM mgas ORDER BY mga_name").fetchall()
mgas_list = [dict(row) for row in mgas]
print(f"Found {len(mgas_list)} MGAs")

# Export commission rules
print("\nExporting commission rules...")
rules = cursor.execute("""
    SELECT cr.*, c.carrier_name, m.mga_name 
    FROM commission_rules cr
    LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
    LEFT JOIN mgas m ON cr.mga_id = m.mga_id
    WHERE cr.is_active = 1
    ORDER BY c.carrier_name, m.mga_name
""").fetchall()
rules_list = [dict(row) for row in rules]
print(f"Found {len(rules_list)} active commission rules")

# Save to JSON file
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'private_contacts_export_{timestamp}.json'

export_data = {
    'export_date': datetime.now().isoformat(),
    'carriers': carriers_list,
    'mgas': mgas_list,
    'commission_rules': rules_list
}

with open(filename, 'w') as f:
    json.dump(export_data, f, indent=2, default=str)

print(f"\nExport complete! Saved to {filename}")

# Show summary including missing ones we discussed
print("\n=== SUMMARY ===")
print(f"Total Carriers: {len(carriers_list)}")
print(f"Total MGAs: {len(mgas_list)}")
print(f"Total Active Commission Rules: {len(rules_list)}")

# Check for specific ones
print("\nChecking for specific carriers/MGAs:")
burlington = any(c['carrier_name'] == 'Burlington' for c in carriers_list)
burns = any(m['mga_name'] == 'Burns & Wilcox' for m in mgas_list)
johnson = any(m['mga_name'] == 'Johnson and Johnson' for m in mgas_list)

print(f"Burlington carrier: {'FOUND' if burlington else 'NOT FOUND'}")
print(f"Burns & Wilcox MGA: {'FOUND' if burns else 'NOT FOUND'}")  
print(f"Johnson and Johnson MGA: {'FOUND' if johnson else 'NOT FOUND'}")

# Close connection
conn.close()