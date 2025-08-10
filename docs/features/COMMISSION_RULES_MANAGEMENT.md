# Commission Rules Management

## Overview
The Commission Rules Management system provides comprehensive control over commission rates and rules for carriers, MGAs, and policy types. Located in the Contacts section, it includes advanced features for editing rules with retroactive date handling and automatic transaction recalculation.

## Date Implemented
- Initial System: July 2025
- Edit with Retroactive Dates: August 6, 2025 (Version 3.9.37)
- Removed Delete Function: August 6, 2025 (Version 3.9.37)

## Key Features

### 1. Commission Rule Display
- **Visual Card Layout**: Each rule displays as a card with clear sections
- **Information Shown**:
  - MGA/Direct appointment
  - Policy types covered
  - NEW and RWL rates
  - Effective date
  - Payment terms
  - Description

### 2. Action Buttons
- **✏️ Edit Rule**: Modify rates, dates, and descriptions
- **📅 End Date**: Deactivate rules while preserving history
- **No Delete Button**: Maintains data integrity

### 3. Edit Rule Functionality

#### Basic Editing
- Change NEW % rate (0-100%)
- Change RWL % rate (0-100%)
- Modify effective date
- Update payment terms (Advanced/As Earned)
- Edit description

#### Retroactive Date Detection
When changing the effective date to an earlier date:
- **Warning Display**: "⚠️ **Retroactive Date Detected!**"
- **Information Message**: "All existing transactions using this rule will have their commission rates recalculated based on the new rates."
- **Automatic Recalculation**: System finds and updates all affected policies

#### Recalculation Process
1. Identifies all policies using the edited rule
2. Recalculates agent commission based on:
   - NEW transactions: Uses new NEW % rate
   - RWL transactions: Uses new RWL % rate
   - Other types: No change
3. Updates database with new commission amounts
4. Shows count of transactions updated

### 4. End Date Functionality
- **Purpose**: Deactivate rules without deletion
- **Process**:
  1. Click 📅 button
  2. Enter end date
  3. Provide reason (e.g., "Rate increase")
  4. Confirm action
- **Result**: Rule becomes inactive but remains in historical records

## Foreign Key Constraints

### Why No Delete Button?
- Commission rules are referenced by policies table
- Database enforces referential integrity
- Deletion would fail with foreign key constraint error
- End-dating preserves historical accuracy

### Error Handling
If deletion is attempted (via direct database access):
- Error: "Cannot delete this rule - it's being used by existing policies"
- Suggestion: "Use 'End Date' instead to deactivate this rule while preserving historical data"

## Best Practices

### 1. Rate Changes
- **Going Forward**: Simply edit the rule with today's date
- **Retroactive**: Edit with past date, system handles recalculation
- **Historical Preservation**: Original transactions maintain audit trail

### 2. Rule Management
- **Active Rules**: Display at top with full action buttons
- **Historical Rules**: Show in separate section when checkbox enabled
- **Audit Trail**: All changes are tracked with dates

### 3. Policy Type Management
- Rules can cover specific policy types or "All Policy Types"
- Multiple policy types supported (comma-separated)
- Integrates with policy type configuration
- **Priority System** (as of v3.9.41):
  - Exact single policy type match: Priority 200
  - Multi-type rule containing the policy type: Priority 100
  - Catch-all rule (no policy type): Priority 10
  - Example: GL-only rule beats "GL, WC" rule when searching for GL

## Integration Points

### 1. Add/Edit Policy
- Commission rules auto-populate based on:
  - Selected carrier
  - Selected MGA (if applicable)
  - Policy type
  - Effective date
- Override capability with reason tracking

### 2. Transaction Recalculation
- Only affects Agent Estimated Comm $
- Preserves Agency Estimated Comm $
- Maintains all other transaction data

### 3. Reporting
- Historical rules preserved for accurate reporting
- Rate changes tracked by effective date
- Complete audit trail for compliance

## Technical Implementation

### Database Structure
```sql
commission_rules table:
- rule_id (UUID, primary key)
- carrier_id (references carriers)
- mga_id (references mgas, nullable)
- policy_type (text, nullable for catch-all)
- new_rate (numeric)
- renewal_rate (numeric)
- effective_date (date)
- end_date (date, nullable)
- is_active (boolean)
- payment_terms (text)
- rule_description (text)
```

### Retroactive Update Query
```python
# Find affected policies
affected_policies = supabase.table('policies')
    .select('*')
    .eq('commission_rule_id', rule['rule_id'])
    .execute()

# Update each policy
for policy in affected_policies.data:
    if policy['Transaction Type'] == 'NEW':
        new_comm = agency_comm * (new_rate / 100)
    elif policy['Transaction Type'] == 'RWL':
        new_comm = agency_comm * (renewal_rate / 100)
```

## Common Scenarios

### Scenario 1: Rate Increase
1. Edit rule with today's date
2. Change rates
3. Future policies use new rates
4. Past policies unchanged

### Scenario 2: Retroactive Correction
1. Edit rule with past effective date
2. System warns about retroactive change
3. Confirm to proceed
4. All affected transactions recalculated
5. See count of updated transactions

### Scenario 3: Ending a Relationship
1. Click 📅 End Date button
2. Set end date to last day of relationship
3. Add reason (e.g., "Carrier terminated agreement")
4. Rule becomes historical

## Troubleshooting

### "Cannot delete rule" error
- **Cause**: Rule is referenced by policies
- **Solution**: Use End Date instead of delete

### Retroactive changes not applying
- **Check**: Transaction types (only NEW/RWL affected)
- **Verify**: Rule is actually used by policies
- **Confirm**: Effective date is truly retroactive

### Wrong rates showing in Add Policy
- **Check**: Effective date of policy vs rule
- **Verify**: Policy type matches rule
- **Confirm**: MGA selection matches rule

## Related Documentation
- [Contacts Management](../help_content/02_features_guide.md#contacts)
- [Add New Policy](../help_content/02_features_guide.md#add-new-policy-transaction)
- [CHANGELOG.md](../core/CHANGELOG.md) - Version history