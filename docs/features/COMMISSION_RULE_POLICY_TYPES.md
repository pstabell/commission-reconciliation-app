# Commission Rules with Policy Type Selection

## Overview
Commission rules now support policy type-specific rates, allowing for more granular control over commission percentages based on the combination of carrier, MGA, and policy type.

## Date Implemented
August 4, 2025 (Version 3.9.29)

## Features

### Multi-Select Policy Types
- Commission rules can be configured for specific policy types
- Multi-select dropdown allows selecting multiple policy types per rule
- Policy types are dynamically loaded from Admin Panel configuration
- "All Policy Types" option available for catch-all rules

### Rule Matching Priority
The system matches commission rules in the following priority order:
1. **Most Specific**: Carrier + MGA + Policy Type
2. **Policy-Specific**: Carrier + Policy Type (Direct appointments)
3. **MGA-Specific**: Carrier + MGA (All policy types)
4. **Carrier Default**: Carrier only (All MGAs, all policy types)

### User Experience Improvements

#### In Contacts Page (Creating Rules)
- Multi-select dropdown replaces text input for policy types
- "All Policy Types" as first option for catch-all rules
- Selected policy types displayed clearly in rule cards
- Rules without specific types show "All Policy Types"

#### In Add New Policy Transaction
- Policy type selection moved outside form (with Carrier and MGA)
- Commission rates update dynamically as you select Carrier → MGA → Policy Type
- Shows which specific rule was matched
- Displays both NEW and RWL rates with clear labeling

## Technical Implementation

### Database Structure
- `policy_type` column in `commission_rules` table stores comma-separated list
- NULL value indicates catch-all rule (all policy types)
- Maintains backward compatibility with existing rules

### Lookup Logic
```python
# Priority order for rule matching
1. lookup_commission_rule(carrier_id, mga_id, policy_type)
2. lookup_commission_rule(carrier_id, None, policy_type)  
3. lookup_commission_rule(carrier_id, mga_id, None)
4. lookup_commission_rule(carrier_id, None, None)
```

### Session State Caching
- Commission rates cached to handle transient database errors
- Prevents rate changes when connection temporarily unavailable
- Cached by carrier + MGA + policy type combination

## Example Use Cases

### Scenario 1: Carrier with Different Rates by Product
- Progressive Auto policies: 12% NEW, 10% RWL
- Progressive Home policies: 15% NEW, 15% RWL
- Progressive Umbrella policies: 20% NEW, 20% RWL

### Scenario 2: MGA-Specific Rates
- Citizens (Direct): All policy types at 10%
- Citizens (via TWFG MGA): All policy types at 8%
- Citizens (via Advantage MGA): Home only at 9%

### Scenario 3: Catch-All with Overrides
- AAA: Default 15% for all products
- AAA: Auto policies specifically at 12%
- System uses 12% for Auto, 15% for everything else

## Benefits
1. **Accuracy**: Correct commission rates automatically applied
2. **Flexibility**: Support for complex commission structures
3. **Efficiency**: No manual rate entry needed
4. **Auditability**: Clear tracking of which rule was applied
5. **Scalability**: Easy to add new policy types or rate structures

## Migration Notes
- Existing rules without policy types continue to work as catch-all rules
- Text-based policy type entries automatically migrated to new format
- No action required for existing commission rules