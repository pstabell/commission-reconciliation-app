# Add Policy Form Redesign - Broker Fees & Taxes Implementation

**Created**: January 7, 2025  
**Purpose**: Document the UI redesign for Add New Policy Transaction form to support broker fees and tax separation

## Overview

This document outlines the UI changes needed for the "Add New Policy Transaction" and "Edit Policy Transactions" forms to support the new broker fee and tax/fee separation features.

## Current Form Structure

### Existing Sections:
1. Client Information
2. Policy Information  
3. Commission Details
4. Other Fields
5. Internal Fields (Read-only)

## Redesigned Form Structure

### 1. Client Information (No Changes)
- Customer Name
- Client ID

### 2. Policy Information (No Changes)
```
Left Column:                    Right Column:
- Policy Type                   - Policy Number
- Carrier Name                  - Transaction Type
```

### 3. Premium & Fee Information (NEW SECTION)
```
Left Column:                    Right Column:
- Premium Sold ($)              - Policy Taxes & Fees ($)
- Broker Fee ($)                - Commissionable Premium ($) [calculated, gray]
```

**Field Properties:**
- **Premium Sold**: Editable, yellow highlight, number input
- **Policy Taxes & Fees**: Editable, white background, number input
- **Broker Fee**: Editable, white background, number input
- **Commissionable Premium**: Read-only, gray background (#F5F5F5), auto-calculated

### 4. Commission Details (UPDATED)
```
Left Column:                    Right Column:
- Policy Gross Comm %           - Agency Est. Comm/Revenue (CRM) [calculated]
- Agent Comm (NEW/RWL) [gray]   - Agent Estimated Comm $ [calculated]
- Broker Fee Agent Comm [gray]  - Total Agent Comm [calculated, gray]
```

**Field Properties:**
- **Policy Gross Comm %**: Editable, white background
- **Agency Est. Comm/Revenue (CRM)**: Read-only, gray background, yellow highlight
- **Agent Comm (NEW 50% RWL 25%)**: Read-only, gray background, shows rate
- **Agent Estimated Comm $**: Read-only, gray background
- **Broker Fee Agent Comm**: Read-only, gray background, NEW field
- **Total Agent Comm**: Read-only, gray background, NEW field

### 5. Other Fields (No Changes)
```
Left Column:                    Right Column:
- Effective Date                - Policy Origination Date
- X-DATE                        - FULL OR MONTHLY PMTS
- NEW BIZ CHECKLIST COMPLETE    - NOTES
```

### 6. Internal Fields (Read-only) (UPDATED)
```
Left Column:                    Right Column:
- STMT DATE                     - Agent Paid Amount (STMT)
- Agency Comm Received (STMT)   - Policy Balance Due [calculated]
```

## Visual Design Specifications

### Field Styling

#### Editable Fields (White Background)
- Premium Sold (with yellow highlight #fff3b0)
- Policy Taxes & Fees
- Broker Fee
- Policy Gross Comm %
- All standard policy fields

#### Calculated Fields (Gray Background #F5F5F5)
- Commissionable Premium
- Agency Est. Comm/Revenue (CRM) (with yellow highlight)
- Agent Comm (NEW 50% RWL 25%)
- Agent Estimated Comm $
- Broker Fee Agent Comm
- Total Agent Comm
- Policy Balance Due

#### Visual Indicators
- 🔒 Lock icon for reconciliation transactions
- 📊 Calculator icon for formula fields
- 💰 Dollar sign for monetary fields
- % Percentage symbol for rate fields

### Tooltips and Help Text

#### Premium & Fee Information
- **Premium Sold**: "Total premium amount including taxes and fees"
- **Policy Taxes & Fees**: "Non-commissionable taxes and fees (will be subtracted from premium)"
- **Broker Fee**: "Agency broker fee (you receive 50% commission on this amount)"
- **Commissionable Premium**: "Premium Sold minus Policy Taxes & Fees"

#### Commission Details
- **Broker Fee Agent Comm**: "Your 50% commission on the broker fee"
- **Total Agent Comm**: "Your total commission including broker fee portion"

## Form Behavior

### Real-time Calculations
When user enters or changes:
1. **Premium Sold or Policy Taxes & Fees**:
   - Update Commissionable Premium
   - Recalculate Agency Est. Comm/Revenue
   - Recalculate Agent Estimated Comm $
   - Update Total Agent Comm

2. **Broker Fee**:
   - Calculate Broker Fee Agent Comm (always 50%)
   - Update Total Agent Comm

3. **Policy Gross Comm %**:
   - Recalculate Agency Est. Comm/Revenue
   - Recalculate Agent Estimated Comm $
   - Update Total Agent Comm

### Validation Rules
1. **Premium Sold** ≥ **Policy Taxes & Fees**
2. All monetary fields must be ≥ 0
3. Policy Gross Comm % must be between 0-100
4. Commissionable Premium cannot be negative

### Error Messages
- "Policy Taxes & Fees cannot exceed Premium Sold"
- "Broker Fee must be a positive number or zero"
- "Commission percentage must be between 0 and 100"

## Migration Considerations

### For Existing Forms
1. Add new section between Policy Information and Commission Details
2. Move some fields to create logical groupings
3. Update Commission Details section layout
4. Add new calculated fields

### For Edit Policy Form
- Same layout changes as Add Policy form
- Maintain existing edit/lock behaviors
- New fields follow same protection rules

## Mobile Responsiveness

### Small Screens (< 768px)
- Stack all fields in single column
- Maintain section groupings
- Show calculated fields below inputs
- Keep visual indicators visible

### Medium Screens (768px - 1024px)
- Maintain two-column layout where possible
- May stack Premium & Fee section
- Preserve field relationships

## Implementation Notes

### Database Requirements
- Migration script to add new columns
- Default values for existing records
- Update all queries to include new fields

### Calculation Engine
- Update formula functions
- Add broker fee calculation (always 50%)
- Modify commission calculations to use Commissionable Premium

### Testing Requirements
1. Test all calculation scenarios
2. Verify validation rules
3. Test with $0 broker fees
4. Test with taxes exceeding premium (should error)
5. Test mobile layouts

## Success Metrics

1. **Accuracy**: All calculations produce correct results
2. **Clarity**: Users understand new fields without training
3. **Efficiency**: Form completion time remains similar
4. **Consistency**: Matches existing form patterns

---

*This redesign maintains the familiar form structure while seamlessly integrating the new broker fee and tax separation features.*