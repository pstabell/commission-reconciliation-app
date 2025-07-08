# Formula Design - Master Implementation Plan
**Created**: July 5, 2025  
**Last Updated**: July 6, 2025  
**Purpose**: Complete technical design for implementing locked formula fields in the commission tracking system

## ✅ IMPLEMENTATION COMPLETE - July 6, 2025

**SUCCESS**: Formula calculations are now FULLY IMPLEMENTED in the Edit Policies form!

### Current State:
- ✅ **Formula Fields Working**: Agency Estimated Comm/Revenue (CRM) and Agent Estimated Comm $ auto-calculate
- ✅ **Phase 0 Complete**: Reconciliation transaction protection is working
- ✅ **Edit Form**: Automatic calculations when entering Premium Sold or Policy Gross Comm %
- ✅ **User Experience**: No more calculators needed!

### What Was Implemented:
1. ✅ Formula fields are read-only (disabled)
2. ✅ Values calculate automatically based on inputs
3. ✅ Tooltips show formulas with actual values
4. ✅ Manual entry prevented in calculated fields
5. ✅ Handles agent rate as decimal (0.50) or percentage (50%)

## 📌 Scope Clarification

This document covers TWO types of field locking that share the same visual design:

1. **Formula Fields** (Primary Focus)
   - Agency Estimated Comm/Revenue (CRM) - Always calculated
   - Agent Estimated Comm $ - Always calculated

2. **Reconciliation Transaction Protection** (Security Requirement)
   - All fields in -STMT- transactions (from RECONCILIATION_SYSTEM_DESIGN.md)
   - All fields in -VOID- transactions
   - All fields in -ADJ- transactions

Both use the same gray styling (#F5F5F5 background, #666666 text) for consistency.

## 🎯 Executive Summary

This design implements two critical formula-driven fields that will be:
- **Automatically calculated** - No manual entry allowed
- **Visually distinct** - Grayed out to show they're locked
- **Always accurate** - Eliminating manual calculation errors
- **Fully transparent** - Formulas documented and visible to users

## 📐 Formula Specifications

### Formula #1: Agency Estimated Comm/Revenue (CRM)
**Purpose**: Calculate the gross commission the agency receives from the carrier  
**Formula**: `Premium Sold × Policy Gross Comm % = Agency Estimated Comm/Revenue (CRM)`  
**Example**: $10,000 × 10% = $1,000

### Formula #2: Agent Estimated Comm $
**Purpose**: Calculate the agent's portion of the commission  
**Formula**: `Agency Estimated Comm/Revenue (CRM) × Agent Comm Rate = Agent Estimated Comm $`  
**Agent Comm Rate Logic**:
- NEW, NBS, STL, BoR: 50%
- RWL, REWRITE: 25%
- END, PCH: 50% if new business, 25% if renewal
- CAN, XCL: 0%

**Example**: $1,000 × 50% = $500

## 🔒 Field Locking Implementation

### Special Transaction Protection (-STMT-, -VOID-, -ADJ-)

**Critical Requirement**: All reconciliation transactions must be completely locked to preserve audit integrity.

1. **Identification Logic**
   ```python
   def is_reconciliation_transaction(transaction_id):
       """Check if transaction is a reconciliation entry that should be locked."""
       if not transaction_id:
           return False
       return any(suffix in str(transaction_id) for suffix in ['-STMT-', '-VOID-', '-ADJ-'])
   ```

2. **Complete Row Locking**
   - ALL fields disabled for reconciliation transactions
   - Same gray background as formula fields (#F5F5F5)
   - Darker gray text (#666666) for consistency
   - Lock icon prefix in Transaction ID display
   - Tooltip: "Reconciliation entry - Cannot be edited"
   - Cannot be selected for deletion

3. **Visual Indication in Data Editor**
   ```
   🔒 XYZ123-STMT-20250704 | Smith Co | $1,000 | $500 | [All fields locked]
   ✏️ ABC456              | Jones Inc | $2,000 | $1,000 | [Editable]
   🔒 DEF789-VOID-20250704 | Wilson LLC | -$500 | -$250 | [All fields locked]
   ```

### Formula Field Locking

In addition to reconciliation protection, the following fields are always locked (formula-driven):

### Visual Design
1. **Edit Policies Data Table**
   - Locked columns with light gray background (#F5F5F5)
   - Darker gray text (#666666) to indicate non-editable
   - Lock icon (🔒) in column header
   - Tooltip on hover: "Calculated field - Formula: [formula]"

2. **Add/Edit Policy Forms**
   - Display-only fields with gray background
   - Show calculated value in real-time as inputs change
   - Formula displayed below field
   - No input cursor or interaction

3. **Visual Mockup**
   ```
   Premium Sold: [_$10,000.00____]
   Policy Gross Comm %: [_10.00%_____]
   
   Agency Estimated Comm/Revenue (CRM): [$1,000.00] 🔒
   Formula: Premium × Gross Comm %
   
   Transaction Type: [NEW ▼]
   
   Agent Estimated Comm $: [$500.00] 🔒
   Formula: Agency Comm × 50% (NEW rate)
   ```

## 💻 Technical Implementation

### 1. Database Layer
- Keep columns in database for performance and reporting
- Add database trigger (optional) to enforce formula on insert/update
- Create view with calculated columns as backup verification

### 2. Application Layer

#### Column Configuration (commission_app.py)
```python
# In Edit Policies data editor
column_config = {
    "Agency Estimated Comm/Revenue (CRM)": st.column_config.NumberColumn(
        "Agency Estimated Comm/Revenue (CRM) 🔒",
        help="Formula: Premium Sold × Policy Gross Comm %",
        disabled=True,
        format="$%.2f"
    ),
    "Agent Estimated Comm $": st.column_config.NumberColumn(
        "Agent Estimated Comm $ 🔒",
        help="Formula: Agency Comm × Agent Rate",
        disabled=True,
        format="$%.2f"
    )
}
```

#### Calculation Functions
```python
def calculate_agency_commission(premium_sold, gross_comm_pct):
    """Calculate agency commission from premium and rate."""
    try:
        premium = float(premium_sold or 0)
        rate = float(gross_comm_pct or 0)
        return premium * (rate / 100)
    except (ValueError, TypeError):
        return 0.0

def calculate_agent_commission(agency_commission, transaction_type, is_new_business=True):
    """Calculate agent commission based on agency commission and transaction type."""
    try:
        agency_comm = float(agency_commission or 0)
        
        # Determine agent rate based on transaction type
        agent_rates = {
            'NEW': 0.50, 'NBS': 0.50, 'STL': 0.50, 'BoR': 0.50,
            'RWL': 0.25, 'REWRITE': 0.25,
            'CAN': 0.00, 'XCL': 0.00
        }
        
        # Special handling for END/PCH
        if transaction_type in ['END', 'PCH']:
            rate = 0.50 if is_new_business else 0.25
        else:
            rate = agent_rates.get(transaction_type, 0.50)
            
        return agency_comm * rate
    except (ValueError, TypeError):
        return 0.0
```

#### Real-time Calculation Triggers
```python
# When Premium Sold or Gross Comm % changes:
1. Recalculate Agency Estimated Comm
2. Cascade to recalculate Agent Estimated Comm

# When Transaction Type changes:
1. Recalculate Agent Estimated Comm only
```

### 3. CSS Styling
```css
/* Locked formula fields */
.formula-field {
    background-color: #F5F5F5 !important;
    color: #666666 !important;
    cursor: not-allowed !important;
}

.formula-field:hover::after {
    content: attr(data-formula);
    position: absolute;
    background: #333;
    color: white;
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 12px;
}
```

## 📋 Implementation Phases

### Phase 0: Critical Security Fix (Immediate)
- [ ] Lock all -STMT-, -VOID-, -ADJ- transactions in Edit Policies
- [ ] Prevent deletion of reconciliation entries
- [ ] Add visual indicators for locked reconciliation rows
- [ ] Test that reconciliation integrity is preserved

### Phase 1: Backend Foundation (Week 1)
- [ ] Create calculation functions in helpers.py
- [ ] Add column configuration with disabled=True
- [ ] Implement real-time calculation on form inputs
- [ ] Add formula validation tests

### Phase 2: Frontend Polish (Week 2)
- [ ] Apply CSS styling for locked fields
- [ ] Add formula tooltips and help text
- [ ] Update forms to show formulas below fields
- [ ] Create visual distinction in data editor

### Phase 3: Data Migration & Testing (Week 3)
- [ ] Run batch calculation to update existing records
- [ ] Verify all calculations are correct
- [ ] Test edge cases (null values, zero amounts)
- [ ] User acceptance testing

### Phase 4: Documentation & Training (Week 4)
- [ ] Update help documentation
- [ ] Add formula examples to UI
- [ ] Create training materials
- [ ] Deploy to production

## 📚 User Documentation

### Help Page Content
```markdown
## Automatic Formula Calculations

The following fields are automatically calculated and cannot be manually edited:

### Agency Estimated Comm/Revenue (CRM) 🔒
**Formula**: Premium Sold × Policy Gross Comm %
**Example**: $10,000 premium × 10% rate = $1,000 agency commission

This represents the gross commission the agency receives from the insurance carrier.

### Agent Estimated Comm $ 🔒
**Formula**: Agency Commission × Agent Commission Rate
**Commission Rates by Transaction Type**:
- NEW, NBS, STL, BoR: 50%
- RWL, REWRITE: 25%
- END, PCH: 50% (new business) or 25% (renewal)
- CAN, XCL: 0%

**Example**: $1,000 agency commission × 50% (NEW) = $500 agent commission

These fields appear with a gray background and lock icon to indicate they are formula-driven.
```

### Edit Policies Page Notice
```
ℹ️ Note: Fields marked with 🔒 are automatically calculated using formulas. 
To change these values, update the underlying fields (Premium, Gross Comm %, or Transaction Type).
```

## 🎯 Benefits & Impact

### Data Quality Improvements
1. **100% Accuracy**: No manual calculation errors
2. **Consistency**: Every record follows the same rules
3. **Transparency**: Formulas are visible and documented
4. **Efficiency**: No time spent double-checking math

### User Experience
1. **Clear Visual Cues**: Locked fields are obviously different
2. **Real-time Feedback**: See calculations update instantly
3. **Helpful Documentation**: Formulas explained in context
4. **Reduced Confusion**: No wondering why values don't match

### Audit & Compliance
1. **Traceable Calculations**: Can always verify the math
2. **No Override Capability**: Prevents accidental or intentional errors
3. **Historical Accuracy**: Past calculations remain correct
4. **Regulatory Compliance**: Consistent application of commission rules

## ⚠️ Important Considerations

### Edge Cases
1. **Null/Empty Values**: Treat as zero in calculations
2. **Percentage Format**: Handle both 10 and 0.10 as 10%
3. **Negative Values**: Allow for adjustments/chargebacks
4. **Decimal Precision**: Always round to 2 decimal places

### Migration Strategy
1. **Backup First**: Create full database backup
2. **Test Migration**: Run on subset of data first
3. **Batch Process**: Update all existing records with calculated values
4. **Verification**: Compare calculated vs. existing values
5. **Rollback Plan**: Keep ability to revert if needed

### Performance Optimization
1. **Calculate on Save**: Store calculated values in database
2. **Recalculate on Edit**: Only when component fields change
3. **Batch Operations**: Efficient updates for bulk changes
4. **Index Key Fields**: Ensure premium, rates are indexed

## 🚀 Future Enhancements

### Phase 2 Possibilities
1. **Custom Formulas**: User-defined calculation rules
2. **Formula History**: Track when formulas change
3. **What-If Analysis**: Test different scenarios
4. **Bulk Recalculation**: Tools for rate changes

### Advanced Features
1. **Tiered Commissions**: Volume-based rate structures
2. **Bonus Calculations**: Performance incentives
3. **Split Commissions**: Multiple agents per policy
4. **Override Approval**: Workflow for exceptions

## ✅ Success Criteria

1. **Zero Manual Entries**: These fields cannot be edited by users
2. **100% Formula Accuracy**: All calculations match documented formulas
3. **Clear Visual Design**: Users immediately recognize locked fields
4. **Complete Documentation**: Formulas explained in help and UI
5. **Smooth Migration**: Existing data updated without issues

---

*This formula design will transform data quality by eliminating manual calculation errors and ensuring consistency across all commission calculations. The locked field approach with clear visual indicators will make the system both more reliable and easier to use.*