# Transaction Type Mapping System

## Overview
The Sales Commission App uses a Transaction Type Mapping system to standardize transaction types from various reconciliation statements into consistent internal types. This ensures data consistency and proper commission categorization across different carrier statement formats.

## Date Implemented
August 5, 2025 (Version 3.9.33)

## The Core Concept

### Why Transaction Type Mapping is Essential
Different insurance carriers and MGAs use various codes in their commission statements to represent transaction types. For example:
- One carrier might use "STL" for settlement/payment transactions
- Another might use "PAYMENT" or "PMT" 
- Some use "NB" while others use "NEW" for new business

The Transaction Type Mapping system solves this by:
1. **Standardizing** all incoming transaction types to a consistent set
2. **Validating** that all statement types are mapped before import
3. **Distinguishing** between different commission triggers

### The Key Distinction: Policy Action vs Customer Payment Commissions

**This is the critical concept that took several iterations to understand:**

There are fundamentally two types of commission triggers:

1. **Policy Action-Driven Commissions** (NEW, RWL, END, CAN)
   - Triggered by policy lifecycle events
   - Commission earned when the policy action occurs
   - Examples:
     - NEW: Commission on new policy issuance
     - RWL: Commission on policy renewal
     - END: Commission on endorsement (policy change)
     - CAN: Negative commission (chargeback) on cancellation

2. **Customer Payment-Driven Commissions** (PMT)
   - Triggered by customer premium payments
   - Commission earned "as-earned" when customer pays
   - Often shown as "STL" (settlement) in carrier statements
   - Represents the actual cash flow of commission payments

### The STL → PMT Mapping
The default mapping of STL → PMT is not arbitrary. It represents:
- **STL** (Settlement): The carrier's code indicating a commission payment based on premium collection
- **PMT** (Payment): Our standardized code for customer payment-driven commissions

This distinction is crucial for:
- Accurate cash flow tracking
- Understanding commission timing (immediate vs as-earned)
- Reconciliation accuracy
- Financial reporting

## Implementation Details

### Configuration Storage
Mappings are stored in `config_files/transaction_type_mappings.json`:
```json
{
  "STL": "PMT",
  "NB": "NEW",
  "RENEW": "RWL"
}
```

### Valid Transaction Types
The system recognizes these standardized transaction types:
- **NEW**: New business
- **RWL**: Renewal
- **END**: Endorsement
- **CAN**: Cancellation
- **PMT**: Payment (as-earned commission)
- **XCL**: (Special cancellation type)
- **PCH**: (Policy change)
- **STL**: (Settlement - typically mapped to PMT)
- **BoR**: (Book of Record)

### Admin Panel Interface
Located in Admin Panel → Transaction Type Mapping tab:
- Visual interface for managing mappings
- Add new mappings with dropdown selection
- Remove existing mappings
- Download configuration for backup
- Shows current mapping count

### Reconciliation Import Process

1. **Validation Phase**
   - Checks all transaction types in the statement
   - Identifies any unmapped types
   - Blocks import if unmapped types found
   - Shows clear error with unmapped types listed

2. **Mapping Application**
   - During transaction creation, applies mappings automatically
   - Shows visual feedback: "Mapped from statement type 'STL' → 'PMT'"
   - Pre-selects mapped type in transaction type dropdown

3. **User Override**
   - Users can still manually select different types if needed
   - System shows the mapping that was applied for transparency

## Common Mapping Scenarios

### Scenario 1: As-Earned Commissions
- Statement shows: STL (Settlement)
- Maps to: PMT (Payment)
- Meaning: Commission paid when customer pays premium

### Scenario 2: New Business Variations
- Statement shows: NB, NEW BIZ, NEW BUSINESS
- Maps to: NEW
- Meaning: Commission on new policy issuance

### Scenario 3: Renewal Variations
- Statement shows: RENEW, RENEWAL, REN
- Maps to: RWL
- Meaning: Commission on policy renewal

## Best Practices

1. **Review Before Import**
   - Always check the Transaction Type Mapping tab before importing new carriers
   - Add mappings for any new transaction types you encounter

2. **Consistent Mapping**
   - Use the same target type for similar source types
   - Document any special mappings in the NOTES field

3. **Backup Configuration**
   - Regularly download the configuration file
   - Keep a record of your mapping decisions

## Troubleshooting

### "Unmapped Transaction Types Found" Error
1. Note the unmapped types shown in the error
2. Go to Admin Panel → Transaction Type Mapping
3. Add mappings for each unmapped type
4. Return to reconciliation and retry import

### Incorrect Mapping Applied
1. Check Admin Panel → Transaction Type Mapping
2. Remove the incorrect mapping
3. Add the correct mapping
4. Re-import the statement

## Technical Implementation Notes

### Where Mappings Are Applied
1. **commission_app.py:7845-7891** - Validation during import
2. **commission_app.py:2857-2868** - Application during transaction creation
3. **commission_app.py:2508-2535** - UI feedback in transaction creation form
4. **commission_app.py:10460-10614** - Admin Panel mapping interface

### Key Functions
- Mapping validation happens before any data is imported
- Mappings are loaded from JSON file for each operation
- System provides default STL → PMT mapping on first use

## Related Documentation
- [RECONCILIATION_SYSTEM.md](RECONCILIATION_SYSTEM.md) - How reconciliation creates transactions
- [POLICY_TERM_FILTERING.md](POLICY_TERM_FILTERING.md) - How transactions are filtered and displayed
- [CLAUDE.md](../operations/CLAUDE.md) - Recent changes and known issues