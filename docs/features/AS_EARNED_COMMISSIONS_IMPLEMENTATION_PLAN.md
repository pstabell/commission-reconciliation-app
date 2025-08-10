# As-Earned Commissions Implementation Plan

**Created**: August 8, 2025  
**Last Updated**: August 8, 2025  
**Version**: 2.0  
**Purpose**: Implement automatic as-earned commission calculations based on payment plans

## ⚠️ IMPLEMENTATION SAFETY NOTICE
This implementation requires EXTREME CAUTION with comprehensive rollback capability at every step. Each phase must be independently reversible without affecting existing functionality.

## Overview

Transform the existing "FULL OR MONTHLY PMTS" column into a robust as-earned commission tracking system that automatically calculates what commissions are truly earned based on elapsed time and payment schedules.

## Key Components

### 1. Database Column Rename
- **Current Column in Supabase**: "FULL OR MONTHLY PMTS"
- **New Column in Supabase**: "AS_EARNED_PMT_PLAN"
- **IMPORTANT**: Clean column rename in both database AND application
- **No mapping needed** - Direct ALTER TABLE rename
- **SQL Command**: 
  ```sql
  ALTER TABLE policy_transactions 
  RENAME COLUMN "FULL OR MONTHLY PMTS" TO "AS_EARNED_PMT_PLAN";
  ```
- Update all column references in commission_app.py to match new name
- No data migration needed - existing values preserved

### 2. Payment Plan Options Configuration

#### Admin Panel Enhancement
- **New Section**: "As-Earned Payment Plans"
- **Location**: Admin Panel → Configuration tab
- **Features**:
  - Add/Edit/Delete payment plan options
  - Set calculation rules for each plan
  - Default options provided

#### Default Payment Plan Options
```
- MONTHLY (12 payments/year)
- SEMI-MONTHLY (24 payments/year)
- QUARTERLY (4 payments/year)
- SEMI-ANNUAL (2 payments/year)
- ANNUAL (1 payment/year - full commission)
- WEEKLY (52 payments/year)
- BI-WEEKLY (26 payments/year)
```

#### Configuration Storage
- Store in `config_files/as_earned_payment_plans.json`
- Each plan includes:
  - Display name
  - Payment frequency per year
  - Description/help text

### 3. Commission Rules Enhancement - HYBRID APPROACH

#### Carrier Level Setting
- **New Field**: "Default As-Earned Commissions" (checkbox)
- **Location**: Carrier add/edit forms in Contacts & Commission Structure
- **Purpose**: Set carrier-wide default for as-earned commissions
- **Behavior**: All commission rules inherit this setting by default

#### Commission Rule Override
- **New Field**: "As-Earned Override" (3-way selector)
  - "Use Carrier Default" (default selection)
  - "Force As-Earned" (override to require payment plan)
  - "Force Not As-Earned" (override to not require payment plan)
- **Location**: Commission Rules add/edit forms
- **Purpose**: Allow exceptions to carrier default

#### Logic Flow
```
1. Check commission rule for override setting
2. If "Use Carrier Default" → Check carrier's as-earned setting
3. If "Force As-Earned" → Require payment plan
4. If "Force Not As-Earned" → Payment plan optional
```

#### Example Scenario
- Progressive Carrier: ✓ Default As-Earned Commissions
- Rule 1: Progressive + Direct + Auto → "Use Carrier Default" → Requires payment plan
- Rule 2: Progressive + Direct + Home → "Use Carrier Default" → Requires payment plan
- Rule 3: Progressive + Special MGA → "Force Not As-Earned" → Payment plan optional

### 4. Transaction Form Updates - DETAILED SPECIFICATIONS

#### Field Transformation
- **Current Field**: "FULL OR MONTHLY PMTS" (free text input)
- **New Field**: "AS EARNED PMT PLAN" (dropdown select)
- **Database**: Same column, only UI label changes

#### Add New Policy Transaction Form
**Input Type Change:**
- From: Text input box where users type anything
- To: Dropdown populated from Admin Panel payment plans
- Additional: "Custom" option for legacy/special cases

**Dynamic Requirement Logic:**
1. User selects Carrier → System checks carrier default
2. User selects MGA → System checks for rule override
3. Field shows red asterisk (*) if payment plan required
4. Validation prevents save without payment plan
5. Help text updates based on requirement

**Visual Example:**
```
Before: FULL OR MONTHLY PMTS: [________________] (free text)

After:  AS EARNED PMT PLAN*: [▼ Select Plan     ]
                             [ MONTHLY          ]
                             [ QUARTERLY        ]
                             [ SEMI-ANNUAL      ]
                             [ ANNUAL           ]
                             [ Custom...        ]
        * Required - Progressive pays as-earned
```

#### Edit Policy Transaction Form (Modal)
**Backward Compatibility:**
- Existing free text values (like "PMTS", "Monthly") preserved
- Display as "Custom: [original value]" in dropdown
- User can keep custom or select standard option
- Gradual migration to standardized values

**Validation Behavior:**
- If carrier now requires payment plan but field empty → Show required
- If changing carrier → Re-evaluate requirement
- Warning if removing payment plan from as-earned carrier

#### Requirement Decision Tree
```
Is there a specific commission rule?
  └─ Yes: Check rule's as-earned override
      ├─ "Force As-Earned" → REQUIRED
      ├─ "Force Not As-Earned" → OPTIONAL
      └─ "Use Carrier Default" → Check carrier setting
          ├─ Carrier has "Default As-Earned" ✓ → REQUIRED
          └─ Carrier has "Default As-Earned" ✗ → OPTIONAL
  └─ No: Check carrier default only
```

### 5. Calculation Logic

#### Earned Commission Formula
```
Months Elapsed = Current Month - Policy Start Month + 1
Annual Periods = Payment frequency from configuration
Earned Periods = Months Elapsed × (Annual Periods ÷ 12)
Earned Commission = (Total Agent Comm ÷ Annual Periods) × Earned Periods
Earned Balance = Earned Commission - Agent Paid Amount
```

#### Detailed Calculation Example
```
Policy Start: June 14, 2024
Total Commission: $1,200
Payment Plan: MONTHLY (12 periods/year)
Current Date: August 8, 2025
Agent Paid: $500

Months Elapsed = 14 months (June 2024 to August 2025)
Earned Periods = 14 × (12 ÷ 12) = 14 periods
Earned Commission = ($1,200 ÷ 12) × 14 = $1,400
BUT: Cap at total commission = $1,200
Earned Balance = $1,200 - $500 = $700
```

#### Special Rules
- Partial months count as full months
- Cancellation month counts as earned
- No proration for mid-month starts/ends
- Blank payment plan = show full balance (current behavior)
- Earned amount cannot exceed total commission
- Negative balances possible if overpaid

### 6. Policy Revenue Ledger Reports

#### Automatic Balance Adjustment
- When "AS EARNED PMT PLAN" has value:
  - Calculate earned balance
  - Display in "Policy Balance Due" column
  - No visual changes needed

#### Column Visibility
- "AS EARNED PMT PLAN" column shows when:
  - Any transaction in report has payment plan value
  - Helps users understand adjusted balances

#### Subtotal Calculations
- Subtotals reflect earned balances
- Group totals adjust automatically
- Export preserves earned calculations

### 7. Visual Indicators

#### Report Enhancement
- Small indicator (★) next to earned balances
- Tooltip explains: "Balance adjusted for as-earned payment plan"
- Payment plan value visible in its column

#### Audit Trail
- Original full balance preserved in database
- Earned calculation happens at display time
- No data integrity issues

## Implementation Benefits

### 1. Accuracy
- Reflects true cash flow position
- Shows collectible amounts
- Prevents over-collection attempts

### 2. Flexibility
- Configurable payment plans
- Carrier-specific rules
- Backward compatible

### 3. Simplicity
- No new UI elements
- Automatic calculations
- Seamless integration

## Migration Strategy

### Phase 1: Backend Setup
1. Add configuration system for payment plans
2. Enhance commission rules with as-earned flag
3. Create calculation functions

### Phase 2: Form Updates
1. Convert text inputs to dropdowns
2. Add validation logic
3. Implement requirement rules

### Phase 3: Report Integration
1. Update balance calculations
2. Add column visibility logic
3. Test with various scenarios

### Phase 4: Documentation
1. Update help documentation
2. Create user guide for as-earned setup
3. Add examples to training materials

## Success Criteria

1. **Accurate Calculations**: Earned balances match expected values
2. **User Experience**: No additional clicks or complexity
3. **Data Integrity**: Original values preserved
4. **Performance**: No impact on report generation speed
5. **Flexibility**: Easy to add new payment plans

## Risk Mitigation

1. **Backward Compatibility**: Blank values continue current behavior
2. **Validation**: Prevent invalid payment plan entries
3. **Testing**: Comprehensive scenarios before release
4. **Rollback**: Easy disable via commission rules

## Implementation Safety Measures

### Phase-by-Phase Rollback Plan

#### Phase 1 Rollback (Configuration)
- Delete payment plans config file
- Remove admin panel UI components
- No database changes needed

#### Phase 2 Rollback (Commission Rules)
- Remove as-earned fields from UI
- Existing data remains untouched
- Rules continue functioning normally

#### Phase 3 Rollback (Transaction Forms)
- Revert dropdown to text input
- Existing values preserved
- No data loss

#### Phase 4 Rollback (Reports)
- Remove calculation logic
- Show original balances
- Column name reverts

### Testing Protocol

1. **Unit Tests**
   - Payment plan calculations
   - Edge case handling
   - Backward compatibility

2. **Integration Tests**
   - Commission rule inheritance
   - Report generation
   - Data integrity

3. **User Acceptance Tests**
   - Real carrier scenarios
   - Migration of existing data
   - Performance benchmarks

### Data Protection

1. **No Destructive Changes**
   - Original commission amounts preserved
   - Calculations happen at display time
   - Easy to revert

2. **Audit Trail**
   - Track payment plan changes
   - Log calculation results
   - Monitor for anomalies

3. **Gradual Rollout**
   - Start with one carrier
   - Monitor results
   - Expand carefully

## Phased Implementation Approach

### Phase 1: Foundation (Week 1)
1. Create payment plans configuration system
2. Add admin panel UI for managing plans
3. Create calculation functions (not yet integrated)
4. **Checkpoint**: Test configuration without affecting production

### Phase 2: Carrier Setup (Week 2)
1. Add "Default As-Earned" checkbox to carriers
2. Update carrier edit forms
3. Test with sample carriers
4. **Checkpoint**: Verify carrier settings work correctly

### Phase 3: Commission Rules (Week 3)
1. Add override selector to commission rules
2. Implement inheritance logic
3. Test various rule combinations
4. **Checkpoint**: Confirm rules properly inherit/override

### Phase 4: Transaction Forms (Week 4)
1. Convert text input to dropdown
2. Add dynamic requirement logic
3. Preserve backward compatibility
4. **Checkpoint**: Test form behavior with various scenarios

### Phase 5: Report Integration (Week 5)
1. Add calculation logic to reports
2. Update column headers
3. Add visual indicators
4. **Checkpoint**: Verify calculations match expectations

### Phase 6: Production Rollout (Week 6)
1. Enable for pilot carrier
2. Monitor for issues
3. Gather user feedback
4. **Checkpoint**: Confirm stability before full rollout

## Future Enhancements

1. **Carrier Integration**: Auto-populate payment plans from carrier data
2. **Advanced Schedules**: Custom payment patterns
3. **Forecasting**: Project future earned amounts
4. **Alerts**: Notify when payments lag earned amounts
5. **Bulk Updates**: Apply payment plans to multiple transactions
6. **API Integration**: Accept payment plan data from external systems