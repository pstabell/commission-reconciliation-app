# Duplicate Transaction Feature

## Overview
The Duplicate Transaction feature allows users to quickly create new transactions based on existing ones. This is particularly useful for creating cancellations, endorsements, or similar policies without re-entering all the data.

## How to Use

### 1. Select a Transaction
- Navigate to the **Edit Policy Transactions** page
- Search for the transaction you want to duplicate
- Check the selection box for exactly ONE transaction

### 2. Click Duplicate Button
- The "📋 Duplicate Selected Transaction" button will become enabled
- Click the button to open the edit form with copied data

### 3. Modify as Needed
- A new Transaction ID is automatically generated
- All data is copied except internal tracking fields
- The form title shows "Create Duplicate" instead of "Save Changes"
- Modify any fields as needed (e.g., change to CAN for cancellation)

### 4. Save the Duplicate
- Click "Create Duplicate" to save as a new transaction
- The system will INSERT a new record (not update the original)

## Fields Excluded from Duplication
The following fields are NOT copied to maintain data integrity:
- `Transaction ID` - A new ID is generated
- `_id` - Database internal ID
- `created_at`, `updated_at` - Timestamps
- `reconciliation_status`, `reconciliation_id`, `reconciled_at` - Reconciliation tracking
- `is_reconciliation_entry` - Reconciliation flag
- `Select` - UI selection checkbox

## Common Use Cases

### Creating a Cancellation
1. Duplicate the original NEW or RWL transaction
2. Change Transaction Type to CAN
3. Enter the original Policy Number in Prior Policy Number field
4. Adjust dates as needed
5. Click Calculate to compute negative commissions (chargebacks)

### Creating an Endorsement
1. Duplicate the current policy transaction
2. Change Transaction Type to END
3. Update premium amounts (use the Premium Calculator)
4. Adjust effective dates
5. Save the endorsement

### Creating a Similar Policy
1. Duplicate an existing policy for the same client
2. Update Policy Number
3. Adjust coverage amounts and dates
4. Save as a new policy

## Special Features

### Agent Comm % Override for Cancellations
When creating a CAN (cancellation) transaction:
1. The system automatically calculates the chargeback rate based on Prior Policy Number
2. After clicking Calculate, the Agent Comm % field becomes editable
3. You can manually override the percentage for special cases
4. The field shows "🔓 UNLOCKED" when editable
5. Useful for cancelling NEW policies where you need 50% chargeback but want to keep Prior Policy Number for audit trail

## Technical Details

### Implementation
- The duplicate functionality is implemented in the `edit_transaction_form()` function
- Uses a `duplicate_mode` session state flag to differentiate from normal edits
- The form logic checks this flag to determine whether to INSERT or UPDATE

### Button Logic
- The button is only enabled when exactly one transaction is selected
- Selection count is calculated once and cached for performance
- Both Duplicate and Edit buttons use the same selection logic

### Database Operation
- Always performs an INSERT operation when in duplicate mode
- Cleans data using `clean_data_for_database()` before insertion
- Generates new Transaction ID using `generate_transaction_id()`

## Version History
- **v3.9.3** (2025-07-30): Initial implementation of Duplicate Transaction feature
- Added Agent Comm % override capability for cancellations