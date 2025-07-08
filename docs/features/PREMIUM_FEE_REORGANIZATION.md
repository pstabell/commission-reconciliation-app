# Premium & Fee Section Reorganization

**Created**: January 7, 2025  
**Purpose**: Document the reorganization of premium entry and fee/tax handling for better clarity and workflow

## Overview

This document outlines the reorganization of how premiums, broker fees, and carrier taxes/fees are handled in the Add New Policy and Edit Policy forms. The changes improve clarity by separating premium entry from fee/tax entry and using more descriptive field names.

## Current Issues

1. **Redundant Fields**: "Premium Sold ($)" appears in multiple places
2. **Unclear Section Title**: "Premium & Fee Information" doesn't indicate its actual purpose
3. **Confusing Flow**: Users unclear where to enter premium vs fees/taxes
4. **Poor Field Names**: "Enter Premium Sold and see Agency Revenue" is verbose and unclear

## New Structure

### Premium Entry (Primary Fields)

**For New Policies:**
- Field Name: "New Policy Premium ($)"
- Location: Main form area (not in fee section)
- Purpose: Enter the total premium for new policies

**For Endorsements:**
- Field Name: "Endorsement Premium (Calculator) ($)"
- Location: Main form area (not in fee section)
- Purpose: Calculate premium changes for endorsements

### Broker Fee / Carrier Taxes & Fees Section

**Section Title**: "Broker Fee / Carrier Taxes & Fees"

**Fields**:
1. **Broker Fee ($)**
   - User input
   - Agency keeps 100%, agent gets 50% commission
   - Help text: "Agency broker fee (you receive 50% commission)"

2. **Carrier Taxes & Fees ($)**
   - User input (formerly "Policy Taxes & Fees")
   - Non-commissionable amounts
   - Help text: "Non-commissionable carrier taxes and fees"

3. **Commissionable Premium ($)**
   - Calculated field (read-only)
   - Formula: Premium - Carrier Taxes & Fees
   - Help text: "Premium minus carrier taxes & fees"

## Implementation Details

### Form Layout Changes

#### Add New Policy Transaction Form

**Before**:
```
Premium & Fee Information
- Premium Sold ($)          - Policy Taxes & Fees ($)
- Broker Fee ($)            - Commissionable Premium ($)
```

**After**:
```
[Main Form Area]
- New Policy Premium ($)    [other fields...]

Broker Fee / Carrier Taxes & Fees
- Broker Fee ($)            - Carrier Taxes & Fees ($)
                           - Commissionable Premium ($)
```

#### Edit Policy Transaction Form

Same reorganization as Add New Policy form, with dynamic field naming based on transaction type.

### Field Behavior

1. **Premium Fields**:
   - User enters premium in main form area
   - Value flows to commission calculations
   - No longer duplicated in fee section

2. **Broker Fee**:
   - Optional field
   - Always generates 50% agent commission
   - Added to total agent commission

3. **Carrier Taxes & Fees**:
   - Optional field
   - Reduces commissionable premium
   - Never generates commission

4. **Commissionable Premium**:
   - Auto-calculated
   - Updates when premium or taxes change
   - Base for all commission calculations

### Calculation Flow

1. User enters Premium (New Policy or Endorsement)
2. User enters Broker Fee (optional)
3. User enters Carrier Taxes & Fees (optional)
4. System calculates:
   ```
   Commissionable Premium = Premium - Carrier Taxes & Fees
   Agency Commission = Commissionable Premium × Gross Rate
   Agent Commission = Agency Commission × Agent Rate
   Broker Fee Agent Comm = Broker Fee × 0.50
   Total Agent Comm = Agent Commission + Broker Fee Agent Comm
   ```

## Benefits

1. **Clarity**: Clear separation between premium entry and fee/tax entry
2. **Workflow**: Logical flow from premium → fees → calculations
3. **Accuracy**: No confusion about where to enter values
4. **Flexibility**: Handles both new policies and endorsements cleanly

## Migration Notes

- Database column "Policy Taxes & Fees" remains unchanged
- Only UI labels and organization change
- Backward compatible with existing data
- No data migration required

## Testing Checklist

- [ ] Add New Policy form shows reorganized sections
- [ ] Edit Policy form shows reorganized sections
- [ ] "New Policy Premium" field works correctly
- [ ] "Endorsement Premium (Calculator)" field works correctly
- [ ] Broker Fee section clearly labeled
- [ ] Carrier Taxes & Fees properly labeled
- [ ] Commissionable Premium calculates correctly
- [ ] All calculations update properly
- [ ] Help text is clear and helpful
- [ ] No duplicate Premium Sold fields

---

*This reorganization improves user experience by creating a logical flow and clear field purposes without changing the underlying calculation logic.*