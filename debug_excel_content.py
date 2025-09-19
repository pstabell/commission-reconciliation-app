#!/usr/bin/env python3
"""Debug the Excel content more thoroughly."""

from zipfile import ZipFile
import xml.etree.ElementTree as ET

excel_file = './PRIVATE mode contacts_export_20250919_134134.xlsx'

# First, let's check shared strings for Johnson
with ZipFile(excel_file, 'r') as zip_file:
    # Read shared strings
    shared_strings = []
    try:
        with zip_file.open('xl/sharedStrings.xml') as f:
            content = f.read().decode('utf-8')
            # Look for Johnson in the content
            if 'Johnson' in content:
                print("Found 'Johnson' in shared strings!")
                
            tree = ET.parse(f)
            root = tree.getroot()
            for si in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
                t = si.find('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                if t is not None and t.text:
                    shared_strings.append(t.text)
                    if 'Johnson' in t.text or 'Great Lakes' in t.text:
                        print(f"Found in shared strings: '{t.text}'")
    except Exception as e:
        print(f"Error reading shared strings: {e}")
    
    print(f"\nTotal shared strings: {len(shared_strings)}")
    
    # Show all MGAs and carriers containing Johnson or the 5 carriers
    print("\nRelevant entries in shared strings:")
    for i, s in enumerate(shared_strings):
        if 'Johnson' in s or s in ['Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston']:
            print(f"  Index {i}: '{s}'")