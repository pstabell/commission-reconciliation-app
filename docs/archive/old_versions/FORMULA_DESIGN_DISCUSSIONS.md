# Formula Design Discussions
**Created**: July 4, 2025  
**Purpose**: Technical design decisions for formula implementations

## 📊 Agency Estimated Comm/Revenue (CRM) - Calculated Field Design

### Current State
- Stored as regular database field
- Can be manually edited
- Formula: `Premium Sold × Policy Gross Comm %`
- Calculated only during "Add New Policy"

### Proposed Change: Pure Formula Field
Transform into a calculated field that:
- **Cannot be edited directly** (display-only)
- **Always displays**: `Premium Sold × Policy Gross Comm %`
- **Updates automatically** when Premium or Comm % changes
- **Not stored** - calculated on display

### Benefits
1. **Data Integrity**: No manual overrides to cause confusion
2. **Single Source of Truth**: Formula always governs
3. **Consistency**: Every transaction follows same rule
4. **Audit Trail**: Can trace changes through component fields
5. **No Sync Issues**: Never out of sync with components

### Implementation Approach
1. Make field read-only in all edit views
2. Calculate on-the-fly during display
3. Style differently (blue text or gray background)
4. Add tooltip: "Calculated: Premium × Comm %"
5. Remove from editable field lists

### Impact on Reconciliation
- Original transactions: Shows calculated amount
- Reconciliation transactions (-STMT): Always $0
- No confusion about "earned" vs "received"

### Migration Strategy
1. Run one-time update: Set all existing = Premium × Comm %
2. Make field calculated going forward
3. No data loss - formula can recreate any value

---

## 🔄 Future Formula Discussions

### Agent Commission Tiers (Potential)
*Placeholder for graduated commission rates based on volume*

### Bonus Calculations (Potential)
*Placeholder for performance-based bonus formulas*

### Override Handling (Potential)
*Placeholder for special case handling*

---

## 📝 Formula Design Principles

1. **Transparency**: Users should understand calculations
2. **Immutability**: Formulas shouldn't change historical data
3. **Traceability**: All inputs to formulas must be visible
4. **Consistency**: Same inputs = same outputs always
5. **Performance**: Calculate on display, not on storage

---

*Add new formula discussions above this line*