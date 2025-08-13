# As-Earned Commissions Implementation Plan

**Created**: August 8, 2025  
**Last Updated**: August 10, 2025  
**Version**: 6.0 - WITH WC POLICY REQUIREMENT  
**Purpose**: Add display-only "As Earned Balance Due" column using existing dropdown, require payment plan for WC policies

## ⚠️ IMPLEMENTATION APPROACH
This implementation utilizes the EXISTING dropdown:
- Dropdown already exists with ["FULL", "MONTHLY", ""] options
- Just need to expand the options list
- REQUIRE payment plan for all WC (Workers Comp) policies
- Display-only column for Excel export
- NO changes to existing calculations

## Overview

We discovered that the "FULL OR MONTHLY PMTS" field already has a dropdown implemented! Currently it has 3 options:
- "FULL"
- "MONTHLY" 
- "" (blank)

We will simply update this existing dropdown to include all payment plan options and add the display-only "As Earned Balance Due" column to reports.

## Key Design Principles

1. **NO CHANGES to existing calculations** - "Policy Balance Due" remains exactly as-is
2. **Use existing dropdown** - Found at lines 4671 and 7158 in commission_app.py
3. **Display-only column** - New column is purely for visual/export purposes
4. **Simple list update** - Just change the payment_types array
5. **Excel-focused** - Designed for export and manual adjustments
6. **WC Policy Requirement** - Workers Comp policies MUST have a payment plan selected

## Implementation Phases

### Phase 1: Database Column Rename (Week 1)
**Purpose**: Clean up column naming for clarity

1. **Rename in Supabase**:
   ```sql
   ALTER TABLE policy_transactions 
   RENAME COLUMN "FULL OR MONTHLY PMTS" TO "AS_EARNED_PMT_PLAN";
   ```

2. **Update commission_app.py**:
   - Find/replace all references to old column name
   - Update column_mapping_config.py if needed
   - No data migration needed - values preserved

3. **Testing**:
   - Verify all forms still save/load correctly
   - Check reports display renamed column
   - Confirm no data loss

### Phase 2: Update Existing Dropdown Options & Add WC Requirement (Week 1)
**Purpose**: Expand the dropdown to include all payment plan options and require for WC policies

1. **Current Code Locations**:
   - Edit Transaction Modal: Line 4671 `payment_types = ["FULL", "MONTHLY", ""]`
   - Add New Transaction Form: Line 7158 (inline list)

2. **Update to New Options List**:
   ```python
   payment_types = [
       "",           # Keep blank as default (except for WC)
       "FULL",       # Existing option
       "MONTHLY",    # Existing option
       "QUARTERLY",
       "SEMI-ANNUAL",
       "ANNUAL",
       "WEEKLY",
       "BI-WEEKLY",
       "SEMI-MONTHLY"
   ]
   ```

3. **Add WC Policy Requirement**:
   - Check if Policy Type = "WC" (Workers Comp)
   - If yes: Make payment plan field REQUIRED
   - Add validation to prevent saving without payment plan
   - Show error message: "Payment plan is required for Workers Comp policies"

4. **Implementation Details**:
   - Add validation in both Add and Edit forms
   - Check policy type when form loads or policy type changes
   - Add red asterisk (*) to field label when required
   - Block form submission if WC policy has no payment plan

### Phase 3: Add Payment Frequency Recognition (Week 2)
**Purpose**: Convert dropdown selections to calculation values

1. **Payment Plan Recognition Function**:
   ```python
   def get_payment_frequency(payment_plan_text):
       """Convert payment plan selection to annual frequency."""
       if not payment_plan_text:
           return None
       
       plan = str(payment_plan_text).upper().strip()
       
       # Direct mapping for dropdown values
       frequency_map = {
           'FULL': 1,
           'ANNUAL': 1,
           'SEMI-ANNUAL': 2,
           'QUARTERLY': 4,
           'MONTHLY': 12,
           'SEMI-MONTHLY': 24,
           'BI-WEEKLY': 26,
           'WEEKLY': 52
       }
       
       return frequency_map.get(plan, None)
   ```

2. **Calculation Logic**:
   ```python
   def calculate_as_earned_balance(transaction):
       """Calculate as-earned balance if payment plan exists."""
       frequency = get_payment_frequency(transaction['AS_EARNED_PMT_PLAN'])
       
       if not frequency:
           return None  # Don't show column for this row
       
       # Calculate months elapsed
       effective_date = transaction['Effective Date']
       current_date = datetime.now()
       months_elapsed = calculate_months_between(effective_date, current_date)
       
       # Calculate earned amount
       total_comm = transaction['Total Agent Comm'] or 0
       period_amount = total_comm / frequency
       earned_periods = months_elapsed * (frequency / 12)
       earned_amount = period_amount * earned_periods
       
       # Cap at total commission
       earned_amount = min(earned_amount, total_comm)
       
       # Calculate balance
       paid_amount = transaction['Agent Paid Amount (STMT)'] or 0
       return earned_amount - paid_amount
   ```

### Phase 4: Add Display-Only Column (Week 2)
**Purpose**: Show calculated values in reports

1. **Column Visibility Logic**:
   - Check if ANY transaction has a payment plan value
   - If yes: Show "As Earned Balance Due" column
   - If no: Hide column completely

2. **Report Display**:
   - Add column after existing "Policy Balance Due"
   - Apply same formatting as balance columns
   - Include in subtotals/totals
   - Show actual earned balance calculations

3. **Key Points**: 
   - "Policy Balance Due" calculation remains UNCHANGED
   - Original balance still shows full amount owed
   - New column is additional information only

### Phase 5: Testing & Documentation (Week 3)
**Purpose**: Ensure reliability and user understanding

1. **Test Scenarios**:
   - All dropdown options calculate correctly
   - Blank option doesn't show column
   - Legacy values (if any exist as free text)
   - Excel export includes column when applicable

2. **Documentation Updates**:
   - Update user guide with payment plan options
   - Explain calculation methodology
   - Emphasize display-only nature

## Payment Plan Options & Frequencies

The dropdown will contain these options:

| Dropdown Value | Payments/Year | Description |
|----------------|---------------|-------------|
| (blank) | - | No payment plan (full commission) |
| FULL | 1 | Full payment (same as ANNUAL) |
| ANNUAL | 1 | One payment per year |
| SEMI-ANNUAL | 2 | Two payments per year |
| QUARTERLY | 4 | Four payments per year |
| MONTHLY | 12 | Twelve payments per year |
| SEMI-MONTHLY | 24 | Twenty-four payments per year |
| BI-WEEKLY | 26 | Twenty-six payments per year |
| WEEKLY | 52 | Fifty-two payments per year |

## Calculation Examples

### Example 1: MONTHLY Payment Plan
```
User Selects: "MONTHLY" (from dropdown)
Policy Start: January 1, 2024
Current Date: August 10, 2025 (20 months elapsed)
Total Agent Comm: $1,200
Agent Paid: $500

System Recognizes: 12 payments/year
Earned Periods: 20 months
Earned Amount: ($1,200/12) × 20 = $2,000
Capped at: $1,200 (total commission)
As Earned Balance Due: $1,200 - $500 = $700

Policy Balance Due: $700 (UNCHANGED - shows full balance)
```

### Example 2: Blank Selection
```
User Selects: "" (blank from dropdown)
Result: No payment frequency
Action: "As Earned Balance Due" column doesn't appear
Policy Balance Due: Shows normal full balance
```

## Benefits of This Approach

1. **Minimal Code Changes**: Just update the options array
2. **Uses Existing UI**: Dropdown already built and working
3. **Consistent UX**: Same dropdown behavior users know
4. **Clean Data**: Standardized values from dropdown
5. **Easy Implementation**: Most work already done!

## What This Implementation Includes

1. **Update existing dropdown** - Add new payment options
2. **Simple recognition function** - Map dropdown values to frequencies
3. **Display-only column** - Show calculated as-earned balance
4. **Conditional visibility** - Column appears only when needed
5. **Excel export** - Include new column when visible

## Success Criteria

1. Dropdown shows all payment plan options
2. Selections save and load correctly
3. Calculations match manual expectations
4. Excel export includes column when applicable
5. No impact on existing functionality

## Implementation Notes

### Code Changes Summary
1. **Line 4671**: Update `payment_types` array in Edit modal
2. **Line 7158**: Update dropdown options in Add form
3. **Add**: Payment frequency recognition function
4. **Add**: As-earned balance calculation in reports
5. **Add**: Column visibility logic

### Backward Compatibility
- Existing "FULL" and "MONTHLY" values continue to work
- Blank values remain blank (no column shown)
- Any legacy free-text values (if they exist) won't trigger calculations

## Rollback Plan

If needed:
1. Revert dropdown options to original ["FULL", "MONTHLY", ""]
2. Remove calculation functions
3. Remove new column from reports
4. No database changes to reverse (except column rename)

## Future Considerations

This implementation provides a clean foundation for:
- Adding more payment options if needed
- Implementing carrier-specific rules later
- Enhanced reporting features
- Integration with payment systems

But for now, we're keeping it simple by just expanding the existing dropdown!