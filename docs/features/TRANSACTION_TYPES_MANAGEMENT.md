# Transaction Types Management System

## Overview
The Transaction Types Management system provides complete control over transaction types used throughout the commission tracking application. Located in Admin Panel → Transaction Types & Mapping tab, it combines transaction type definition, management, and statement mapping in one unified interface.

## Date Implemented
- Initial Implementation: August 6, 2025 (Version 3.9.36)

## Features

### 1. Transaction Types Overview
- **Live Database Counts**: Shows actual usage of each transaction type
- **Descriptions**: Document what each transaction type represents
- **Active/Inactive Status**: Control which types are available for use
- **In Database Indicator**: Shows if type has any transactions

### 2. Metrics Dashboard
- **Total Types**: Count of unique transaction types in database
- **Total Transactions**: Sum of all transactions across all types
- **Active Types**: Number of currently active transaction types
- **Unused Types**: Types defined but with 0 transactions

### 3. Management Features

#### Edit Descriptions
- Click in the Description column to add/edit descriptions
- Helps document the purpose of each transaction type
- Descriptions are saved to configuration file

#### Activate/Deactivate Types
- Check/uncheck the Active column to control availability
- Inactive types won't appear in dropdowns but retain their data
- Useful for phasing out old types without losing history

#### Delete Types
- Check the Delete checkbox for types with 0 transactions
- Only available for unused types to preserve data integrity
- Removes type from configuration completely

#### Merge Types
- Select target type in "Merge To" dropdown
- Updates ALL transactions from source to target type
- Source type is removed after successful merge
- Shows transaction count to confirm scope of change
- Example: Merge STL → PMT to consolidate payment types

### 4. Add New Transaction Types
- Enter type code (e.g., "REI" for Reinstatement)
- Provide description for clarity
- New types are immediately available for use

### 5. Statement Type Mapping
Located at the bottom of the tab, this section handles reconciliation imports:
- Maps statement codes to standardized types
- Prevents import errors from unknown types
- Default mapping: STL → PMT
- Add new mappings as needed

## Configuration Storage

### Transaction Type Definitions
Stored in `config_files/transaction_types.json`:
```json
{
  "NEW": {
    "description": "New business policy",
    "active": true
  },
  "RWL": {
    "description": "Policy renewal",
    "active": true
  },
  "PMT": {
    "description": "Payment-driven commission",
    "active": true
  }
}
```

### Statement Mappings
Stored in `config_files/transaction_type_mappings.json`:
```json
{
  "STL": "PMT",
  "XCL": "CAN"
}
```

## Commission Calculations by Type

Different transaction types trigger different commission calculations:

- **NEW**: 50% of agency commission (new business)
- **RWL**: 25% of agency commission (renewals)
- **END**: Variable - 50% if new policy, 25% if renewal
- **CAN/XCL**: Negative commission (chargeback)
- **PMT**: Payment-driven commission (as-earned)

## Best Practices

1. **Document Types**: Always add descriptions to clarify purpose
2. **Merge Carefully**: Merging is permanent and affects all historical data
3. **Deactivate vs Delete**: Prefer deactivating over deleting to preserve options
4. **Test Mappings**: Verify statement mappings before large imports
5. **Regular Review**: Check unused types periodically for cleanup

## Common Use Cases

### Consolidating Duplicate Types
1. Identify types with similar purposes (e.g., STL and PMT)
2. Select the preferred type in "Merge To" column
3. Click Save to merge all transactions
4. Source type is removed automatically

### Phasing Out Old Types
1. Uncheck "Active" for types no longer in use
2. They remain in database but won't appear in new transaction dropdowns
3. Historical data remains intact

### Handling New Statement Formats
1. If import fails due to unknown type
2. Add mapping in Statement Type Mapping section
3. Map to appropriate standardized type
4. Retry import

## Technical Notes

### Database Operations
- Merge operations update the `Transaction Type` column in policies table
- Uses SQL UPDATE with proper transaction handling
- Cache is cleared after database modifications

### Error Handling
- Prevents deletion of types with existing transactions
- Validates merge operations before execution
- Shows clear error messages for failed operations

### Performance
- Live counts may take a moment for large databases
- Merge operations process all affected records in one batch
- Automatic page refresh after successful operations

## Related Documentation
- [TRANSACTION_TYPE_MAPPING.md](TRANSACTION_TYPE_MAPPING.md) - Statement mapping details
- [RECONCILIATION_SYSTEM.md](RECONCILIATION_SYSTEM.md) - How types affect reconciliation
- [CHANGELOG.md](../core/CHANGELOG.md) - Version history

## Troubleshooting

### Merge Not Working
- Ensure you've selected a target type in "Merge To" dropdown
- Click Save button to execute merge
- Check for error messages about database access

### Types Not Showing
- Click refresh button (🔄) to reload data
- Check if type is marked as Active
- Verify configuration file isn't corrupted

### Can't Delete Type
- Only types with 0 transactions can be deleted
- Use merge feature to consolidate types with transactions
- Consider deactivating instead of deleting