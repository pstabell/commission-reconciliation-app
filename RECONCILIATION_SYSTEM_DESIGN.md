# Reconciliation System Design - Master Recipe
**Created**: July 4, 2025  
**Purpose**: Implement proper double-entry accounting for commission reconciliation

## 🎯 Core Concept

Transform the commission tracking system into a true double-entry accounting ledger where:
- **Original transactions** = Credits (commission earned/owed)
- **Reconciliation transactions** = Debits (commission paid/received)
- **Net result** = Outstanding balance per policy

## 📊 Transaction Types & ID Structure

### 1. Original Transactions (Credits)
- **Transaction ID**: `A1B2C3D` (7 characters: mixed letters & numbers)
- **Purpose**: Record commission earned when policy is sold/renewed
- **Behavior**: Editable until reconciled

### 2. Reconciliation Transactions (Debits)
- **Transaction ID**: `X7Y8Z9Q-STMT-20250704`
  - Base: New 7-character unique ID
  - Suffix: `-STMT-` indicates reconciliation
  - Date: Statement date (YYYYMMDD format)
- **Purpose**: Record commission payments received from carrier
- **Behavior**: Permanently locked, no edits allowed

### 3. Adjustment Transactions
- **Transaction ID**: `M3N4P5R-ADJ-20250715`
- **Purpose**: Correct errors without modifying original records
- **Behavior**: Locked once created

### 4. Void Transactions
- **Transaction ID**: `K9L8M7N-VOID-20250720`
- **Purpose**: Reverse incorrect reconciliations
- **Behavior**: Locked once created

## 💰 Field Behavior by Transaction Type

### Original Transactions
| Field | Behavior | Value |
|-------|----------|--------|
| Agency Estimated Comm | Calculated | Premium × Comm % |
| Agent Estimated Comm | Calculated | Agency × Rate |
| Agency Comm Received | Empty | $0 |
| Agent Paid Amount | Empty | $0 |
| STMT DATE | Empty | Blank |
| All Fields | Editable | Until reconciled |

### Reconciliation Transactions (-STMT)
| Field | Behavior | Value |
|-------|----------|--------|
| Agency Estimated Comm | Locked | $0 |
| Agent Estimated Comm | Locked | $0 |
| Agency Comm Received | Display Only | Statement amount |
| Agent Paid Amount | Display Only | Statement amount |
| STMT DATE | Display Only | Statement date |
| All Fields | Read-Only | Forever |

## 🔒 Business Rules

### 1. Immutable Reconciliation Records
- Once created, `-STMT` transactions cannot be:
  - Edited
  - Deleted
  - Modified in any way
- This ensures audit trail integrity

### 2. Error Correction Protocol
**Option A: Adjustment Entry (Preferred)**
- Create new transaction with `-ADJ` suffix
- Enter positive/negative amounts to correct
- Original and incorrect entries remain unchanged
- Net effect achieves correct balance

**Option B: Void & Re-reconcile**
- Create `-VOID` entries to reverse entire statement
- Re-import/re-enter with correct amounts
- More complex but sometimes necessary

### 3. Calculated Fields
- `Agency Estimated Comm` = Formula-driven field
- See `FORMULA_DESIGN_DISCUSSIONS.md` for detailed implementation
- Key principle: Cannot be manually overridden

### 4. Visual Indicators
- `-STMT` transactions: Light green background
- `-ADJ` transactions: Light yellow background  
- `-VOID` transactions: Light red strikethrough
- Locked fields: Gray background
- Calculated fields: Blue text

## 📋 Implementation Checklist

### Phase 1: Core Structure
- [ ] Add transaction ID suffix support
- [ ] Implement field locking for `-STMT` transactions
- [ ] Set credit fields to $0 for reconciliations
- [ ] Add STMT DATE validation

### Phase 2: Calculated Fields
- [ ] Implement formula design from `FORMULA_DESIGN_DISCUSSIONS.md`
- [ ] Make Agency Estimated Comm display-only
- [ ] Auto-calculate on display
- [ ] Update all views to show calculated value

### Phase 3: Visual Design
- [ ] Add row coloring based on transaction type
- [ ] Implement field-level read-only styling
- [ ] Add tooltips explaining locked fields
- [ ] Create visual distinction for calculated fields

### Phase 4: Reconciliation Import
- [ ] Generate proper `-STMT-YYYYMMDD` IDs
- [ ] Validate no duplicate statement imports
- [ ] Ensure all credit fields set to $0
- [ ] Lock records immediately after creation

### Phase 5: Reporting
- [ ] Update reports to handle transaction types
- [ ] Create "Outstanding Balances" report
- [ ] Add statement reconciliation summary
- [ ] Build audit trail report

## 🎯 Expected Outcomes

### Clean Ledger View
```
Trans ID              Type    Premium   Agency Est   Agency Rcvd   Balance
A1B2C3D              ORIG    $1,000    $100         $0            $100
X7Y8Z9Q-STMT-20250704 RCVD    $0        $0           $100          ($100)
                                                      Net:          $0
```

### Outstanding Balances Report
- Shows only unreconciled original transactions
- True receivables aging
- No manual calculation needed

### Audit Trail
- Every transaction preserved
- Complete history of changes
- Corrections traceable
- CPA-friendly format

## ⚠️ Critical Success Factors

1. **No Backdating**: Reconciliations use current date, not original date
2. **Unique IDs**: Every row gets unique 7-character base ID
3. **Formula Integrity**: Calculated fields always use formula
4. **Immutability**: Historical records never modified
5. **Clear Suffixes**: -STMT, -ADJ, -VOID tell the story

## 🚀 Next Steps

1. Review and approve this design
2. Create backup of current system
3. Implement Phase 1 (Core Structure)
4. Test with sample reconciliation
5. Roll out remaining phases

---

*This design implements proper accounting principles while maintaining system simplicity and data integrity.*