#!/usr/bin/env python3
"""Check Johnson and Johnson in the Excel export file."""

import sys
import csv
from zipfile import ZipFile
import xml.etree.ElementTree as ET

def extract_sheet_data(zip_file, sheet_name):
    """Extract data from an Excel sheet using raw XML parsing."""
    # Read shared strings
    shared_strings = []
    try:
        with zip_file.open('xl/sharedStrings.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            for si in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
                t = si.find('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                if t is not None and t.text:
                    shared_strings.append(t.text)
    except:
        pass
    
    # Map sheet names to sheet files
    sheet_map = {}
    try:
        with zip_file.open('xl/workbook.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            sheets = root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet')
            for i, sheet in enumerate(sheets):
                name = sheet.get('name')
                sheet_map[name] = f'xl/worksheets/sheet{i+1}.xml'
    except:
        pass
    
    if sheet_name not in sheet_map:
        return None
    
    # Read the sheet data
    rows = []
    try:
        with zip_file.open(sheet_map[sheet_name]) as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            # Find all rows
            for row in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
                row_data = []
                for cell in row.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                    v = cell.find('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                    if v is not None and v.text:
                        # Check if it's a shared string
                        if cell.get('t') == 's':
                            idx = int(v.text)
                            if idx < len(shared_strings):
                                row_data.append(shared_strings[idx])
                            else:
                                row_data.append('')
                        else:
                            row_data.append(v.text)
                    else:
                        row_data.append('')
                if row_data:
                    rows.append(row_data)
    except:
        pass
    
    return rows

# Read the Excel file
excel_file = './PRIVATE mode contacts_export_20250919_134134.xlsx'

try:
    with ZipFile(excel_file, 'r') as zip_file:
        # Extract Commission Rules sheet
        data = extract_sheet_data(zip_file, 'Commission Rules')
        
        if data:
            print(f"Commission Rules sheet has {len(data)} rows")
            
            # Assume first row is headers
            if len(data) > 0:
                headers = data[0]
                print(f"Headers: {headers}")
                
                # Find column indices
                carrier_idx = None
                mga_idx = None
                for i, h in enumerate(headers):
                    if 'carrier' in h.lower():
                        carrier_idx = i
                    if 'mga' in h.lower():
                        mga_idx = i
                
                if carrier_idx is not None and mga_idx is not None:
                    # Count Johnson and Johnson associations
                    jj_count = 0
                    jj_carriers = set()
                    
                    for row in data[1:]:  # Skip header
                        if len(row) > mga_idx and row[mga_idx] == 'Johnson and Johnson':
                            jj_count += 1
                            if len(row) > carrier_idx:
                                jj_carriers.add(row[carrier_idx])
                    
                    print(f"\nJohnson and Johnson associations: {jj_count}")
                    print(f"Carriers associated with J&J: {sorted(jj_carriers)}")
                    
                    # Check for the 5 specific carriers
                    carriers_to_check = ['Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston']
                    print("\nChecking specific carriers:")
                    for carrier in carriers_to_check:
                        found = False
                        jj_found = False
                        for row in data[1:]:
                            if len(row) > carrier_idx and row[carrier_idx] == carrier:
                                found = True
                                if len(row) > mga_idx and row[mga_idx] == 'Johnson and Johnson':
                                    jj_found = True
                                    break
                        
                        status = "Not in file"
                        if found:
                            status = "With J&J" if jj_found else "In file but not with J&J"
                        print(f"  {carrier}: {status}")
        else:
            print("Could not read Commission Rules sheet")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()