# Reconciliation Void Tracking System

## Overview

The Sales Commission App provides comprehensive tracking of voided reconciliations, ensuring complete visibility into which carrier statements have been reversed. This documentation covers the void tracking system implemented in version 3.5.4.

## Background

### The Problem
Users were voiding reconciliations but had no way to tell which statements were voided in the Reconciliation History. All reconciliations appeared as "ACTIVE" regardless of their actual status, creating confusion and risk of double-processing.

### The Discovery
Through investigation, we found that void transactions were being created with different Transaction ID patterns:
- Original reconciliation entries: `XXX-STMT-YYYYMMDD`
- Void reversal entries: `XXX-VOID-YYYYMMDD`

The Reconciliation History filter was only looking for `-STMT-` patterns, making void entries invisible.

## Implementation Details

### Transaction ID Patterns

1. **Statement Entries**: 
   - Pattern: `[7-char-ID]-STMT-[date]`
   - Example: `71DGE0V-STMT-20250731`
   - Status: `reconciled`

2. **Void Entries**:
   - Pattern: `[7-char-ID]-VOID-[date]`
   - Example: `Y355HZ2-VOID-20250710`
   - Status: `void` (lowercase)

### Batch ID Structure

1. **Original Batch**:
   - Pattern: `IMPORT-[date]-[unique-id]`
   - Example: `IMPORT-20250731-3232D7ED`

2. **Void Batch**:
   - Pattern: `VOID-IMPORT-[date]-[unique-id]`
   - Example: `VOID-IMPORT-20250731-3232D7ED`

## User Interface Enhancements

### By Batch View

The By Batch view now includes three critical columns:

| Column | Description | Values |
|--------|-------------|--------|
| **Status** | Current status of the batch | ACTIVE, VOIDED, VOID ENTRY |
| **Void ID** | ID of the void batch if voided | VOID-IMPORT-... or `-` |
| **Void Date** | Date when voided | MM/DD/YYYY or `-` |

**Color Coding**:
- Light red background (#ffcccc) for VOIDED batches
- Light orange background (#ffe6cc) for VOID ENTRY batches
- No background for ACTIVE batches

### All Transactions View

The detailed transaction view shows:

| Column | Description | Example |
|--------|-------------|---------|
| **Reconciliation Status** | Transaction status | RECONCILED or VOID |
| **Batch ID** | Which batch it belongs to | IMPORT-20250731-... |
| **Is Void Entry** | Identifies reversal entries | Yes or No |

## Technical Implementation

### Filter Enhancement

```python
# Old filter (only -STMT- transactions)
recon_entries = all_data[
    all_data['Transaction ID'].str.contains('-STMT-', na=False)
]

# New filter (includes both -STMT- and -VOID-)
recon_entries = all_data[
    (all_data['Transaction ID'].str.contains('-STMT-', na=False)) |
    (all_data['Transaction ID'].str.contains('-VOID-', na=False))
]
```

### Case-Insensitive Status Handling

```python
# Handle lowercase 'void' status
status = str(row.get('reconciliation_status', '')).upper()
if status == 'VOIDED' or status == 'VOID':
    batch_summary.at[idx, 'Status'] = 'VOIDED'
```

### Void Detection Logic

The system checks multiple indicators:
1. Transaction ID contains `-VOID-`
2. Batch ID starts with `VOID-`
3. Reconciliation status is 'void' (case-insensitive)
4. Existence of corresponding void batch

## Workflow Example

### 1. Original Reconciliation
- User reconciles statement dated 07/31/2024
- System creates batch: `IMPORT-20240731-ABC123`
- Transactions created with IDs like `XXX-STMT-20240731`
- Status: ACTIVE

### 2. Voiding Process
- User realizes date should be 07/31/2025
- Clicks "Void Reconciliation"
- System creates void batch: `VOID-IMPORT-20240731-ABC123`
- Reversal entries created with IDs like `XXX-VOID-20250710`
- Original batch status changes to: VOIDED

### 3. Visual Result
- Original batch shows with red background and VOIDED status
- Void batch shows with orange background and VOID ENTRY status
- Clear indication of which reconciliations are active vs. voided

## Benefits

1. **Audit Trail**: Complete history of all void operations
2. **Visual Clarity**: Immediate identification of voided statements
3. **Prevention**: Avoids accidental re-reconciliation of voided statements
4. **Compliance**: Maintains proper accounting records

## Troubleshooting

### Void Not Showing as VOIDED

If a voided reconciliation still shows as ACTIVE:
1. Check if void entries exist in All Policy Transactions
2. Verify Transaction IDs contain `-VOID-`
3. Ensure date range includes void entries
4. Confirm reconciliation_status field is populated

### Missing Void Entries

If void entries aren't visible:
1. Expand date range in Reconciliation History
2. Check All Policy Transactions for -VOID- transactions
3. Verify batch ID format matches expected pattern

## Future Enhancements

Potential improvements identified:
- Add "Void Reason" field for documentation
- Create void summary report
- Implement void approval workflow
- Add email notifications for void operations

---

*Last Updated: July 10, 2025*  
*Version: 3.5.4*