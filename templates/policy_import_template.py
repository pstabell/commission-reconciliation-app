"""
Create Excel template for policy imports
This script generates a template Excel file with all required columns and example data
"""

import pandas as pd
from datetime import datetime, timedelta
import os

# Define all columns needed for policy import
columns = [
    # Required fields
    'Client ID',
    'Transaction ID', 
    'Policy Type',
    'Customer',
    'Policy Number',
    'Transaction Type',
    'Effective Date',
    
    # Financial fields
    'Premium Sold',
    'Policy Gross Comm %',
    'Agency Estimated Comm/Revenue (CRM)',
    'Agent Comm %',
    'Total Agent Comm',
    
    # Carrier/MGA info
    'Carrier Name',
    'MGA',
    
    # Dates
    'Policy Origination Date',
    'X-DATE',
    'STMT Date',
    
    # Payment info
    'Payment Plan',
    'Agency Comm Received (STMT)',
    'Agent Paid Amount (STMT)',
    
    # Additional fields
    'Prior Policy Number',
    'NOTES',
    'Broker Fee',
    'Policy Taxes & Fees'
]

# Create example data to help users understand format
example_data = {
    'Client ID': ['CL12345', 'CL12346', 'CL12347', 'CL12348', 'CL12349'],
    'Transaction ID': ['NEW001', 'NEW002', 'END001', 'RWL001', 'CAN001'],
    'Policy Type': ['AUTO', 'HOME', 'AUTO', 'HOME', 'AUTO'],
    'Customer': ['John Smith', 'Jane Doe', 'John Smith', 'Jane Doe', 'Bob Johnson'],
    'Policy Number': ['AUTO-2024-001', 'HOME-2024-001', 'AUTO-2024-001', 'HOME-2025-001', 'AUTO-2024-002'],
    'Transaction Type': ['NEW', 'NEW', 'END', 'RWL', 'CAN'],
    'Effective Date': [
        datetime(2024, 1, 1),
        datetime(2024, 2, 15),
        datetime(2024, 6, 1),
        datetime(2025, 2, 15),
        datetime(2024, 8, 1)
    ],
    'Premium Sold': [2400.00, 1800.00, 200.00, 1900.00, -800.00],
    'Policy Gross Comm %': [15.0, 12.0, 15.0, 12.0, 15.0],
    'Agency Estimated Comm/Revenue (CRM)': [360.00, 216.00, 30.00, 228.00, -120.00],
    'Agent Comm %': [50.0, 50.0, 50.0, 25.0, 50.0],
    'Total Agent Comm': [180.00, 108.00, 15.00, 57.00, -60.00],
    'Carrier Name': ['Progressive', 'State Farm', 'Progressive', 'State Farm', 'Progressive'],
    'MGA': ['Direct', 'ABC MGA', 'Direct', 'ABC MGA', 'Direct'],
    'Policy Origination Date': [
        datetime(2024, 1, 1),
        datetime(2024, 2, 15),
        datetime(2024, 1, 1),
        datetime(2024, 2, 15),
        datetime(2024, 3, 1)
    ],
    'X-DATE': [
        datetime(2025, 1, 1),
        datetime(2025, 2, 15),
        datetime(2025, 1, 1),
        datetime(2026, 2, 15),
        datetime(2025, 3, 1)
    ],
    'STMT Date': [None, None, None, None, datetime(2024, 8, 15)],
    'Payment Plan': ['12-PAY', 'FULL', '12-PAY', 'FULL', '12-PAY'],
    'Agency Comm Received (STMT)': [None, None, None, None, -120.00],
    'Agent Paid Amount (STMT)': [None, None, None, None, -60.00],
    'Prior Policy Number': [None, None, None, 'HOME-2024-001', None],
    'NOTES': [
        'New auto policy',
        'New homeowner policy', 
        'Added coverage',
        'Renewal',
        'Cancelled - non-payment'
    ],
    'Broker Fee': [25.00, 0.00, 0.00, 0.00, 0.00],
    'Policy Taxes & Fees': [150.00, 125.00, 15.00, 130.00, -50.00]
}

# Create DataFrame
df = pd.DataFrame(example_data)

# Create instructions sheet
instructions = {
    'Column Name': [
        'Client ID',
        'Transaction ID',
        'Policy Type',
        'Customer',
        'Policy Number',
        'Transaction Type',
        'Effective Date',
        'Premium Sold',
        'Policy Gross Comm %',
        'Agency Estimated Comm/Revenue (CRM)',
        'Agent Comm %',
        'Total Agent Comm',
        'Carrier Name',
        'MGA',
        'Policy Origination Date',
        'X-DATE',
        'STMT Date',
        'Payment Plan',
        'Agency Comm Received (STMT)',
        'Agent Paid Amount (STMT)',
        'Prior Policy Number',
        'NOTES',
        'Broker Fee',
        'Policy Taxes & Fees'
    ],
    'Required': [
        'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes',
        'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'No'
    ],
    'Description': [
        'Unique identifier for the client (e.g., CL12345)',
        'Unique transaction ID (e.g., NEW001, END002)',
        'Type of policy (e.g., AUTO, HOME, LIFE, etc.)',
        'Customer/Insured name',
        'Policy number from carrier',
        'Transaction type: NEW, RWL, END, CAN, etc.',
        'Effective date of the transaction (MM/DD/YYYY)',
        'Premium amount (positive for NEW/RWL, negative for CAN)',
        'Gross commission percentage from carrier',
        'Agency commission amount',
        'Agent commission percentage (e.g., 50 for new, 25 for renewal)',
        'Total agent commission amount',
        'Name of insurance carrier',
        'Managing General Agent name (or "Direct")',
        'Original policy start date (MM/DD/YYYY)',
        'Policy expiration date (MM/DD/YYYY)',
        'Statement/reconciliation date (MM/DD/YYYY)',
        'Payment plan: FULL, 12-PAY, 6-PAY, etc.',
        'Commission received from carrier (for reconciliation)',
        'Amount paid to agent (for reconciliation)',
        'Previous policy number (for renewals/rewrites)',
        'Any notes or comments',
        'Broker fees charged',
        'Policy taxes and fees'
    ],
    'Example': [
        'CL12345',
        'NEW001',
        'AUTO',
        'John Smith',
        'AUTO-2024-001',
        'NEW',
        '01/01/2024',
        '2400.00',
        '15',
        '360.00',
        '50',
        '180.00',
        'Progressive',
        'Direct',
        '01/01/2024',
        '01/01/2025',
        '02/15/2024',
        '12-PAY',
        '360.00',
        '180.00',
        'AUTO-2023-001',
        'New auto policy',
        '25.00',
        '150.00'
    ]
}

instructions_df = pd.DataFrame(instructions)

# Create the Excel file with multiple sheets
output_path = os.path.join(os.path.dirname(__file__), 'Policy_Import_Template.xlsx')

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    # Write the main template sheet
    df.to_excel(writer, sheet_name='Import Template', index=False)
    
    # Write the instructions sheet
    instructions_df.to_excel(writer, sheet_name='Column Instructions', index=False)
    
    # Add a blank template sheet (no example data)
    blank_df = pd.DataFrame(columns=columns)
    blank_df.to_excel(writer, sheet_name='Blank Template', index=False)
    
    # Format the sheets
    workbook = writer.book
    
    # Format Import Template sheet
    template_sheet = workbook['Import Template']
    for cell in template_sheet[1]:  # Header row
        cell.font = cell.font.copy(bold=True)
        cell.fill = cell.fill.copy(fgColor="D3D3D3")
    
    # Auto-adjust column widths
    for column in template_sheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        template_sheet.column_dimensions[column_letter].width = adjusted_width
    
    # Format Instructions sheet
    instructions_sheet = workbook['Column Instructions']
    for cell in instructions_sheet[1]:  # Header row
        cell.font = cell.font.copy(bold=True)
        cell.fill = cell.fill.copy(fgColor="4472C4", color="FFFFFF")
    
    # Format Blank Template sheet
    blank_sheet = workbook['Blank Template']
    for cell in blank_sheet[1]:  # Header row
        cell.font = cell.font.copy(bold=True)
        cell.fill = cell.fill.copy(fgColor="70AD47")

print(f"Excel template created: {output_path}")

# Also create a CSV version for users who prefer CSV
csv_path = os.path.join(os.path.dirname(__file__), 'Policy_Import_Template.csv')
df.to_csv(csv_path, index=False)
print(f"CSV template created: {csv_path}")