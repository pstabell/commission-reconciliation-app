# REWRITE as Policy Term Trigger - Implementation Plan

**Created**: August 11, 2025  
**Estimated Time**: 30 minutes  
**Risk Level**: Medium (affects core business logic)

## Implementation Steps

### Step 1: Update Pending Renewals Logic (5 minutes)

**File**: commission_app.py  
**Line**: 1812

```python
# BEFORE:
renewal_candidates = df[df[get_mapped_column("Transaction Type")].isin(["NEW", "RWL"])].copy()

# AFTER:
renewal_candidates = df[df[get_mapped_column("Transaction Type")].isin(["NEW", "RWL", "REWRITE"])].copy()
```

This ensures REWRITE policies appear in Pending Policy Renewals.

### Step 2: Update Policy Revenue Ledger Filters (10 minutes)

**Multiple updates needed:**

1. **Line 13505** - Effective Date dropdown filter:
```python
# BEFORE:
policy_start_data = filtered_data[filtered_data["Transaction Type"].isin(["NEW", "RWL"])]

# AFTER:
policy_start_data = filtered_data[filtered_data["Transaction Type"].isin(["NEW", "RWL", "REWRITE"])]
```

2. **Line 13515** - Update help text:
```python
# BEFORE:
help="Shows only NEW and RWL transaction dates (policy term starts)"

# AFTER:
help="Shows only NEW, RWL, and REWRITE transaction dates (policy term starts)"
```

3. **Line 13622** - Transaction type display:
```python
# BEFORE:
elif trans_type in ["NEW", "RWL"]:

# AFTER:
elif trans_type in ["NEW", "RWL", "REWRITE"]:
```

4. **Line 13675** - Term transaction filter:
```python
# BEFORE:
(policy_rows["Transaction Type"].isin(["NEW", "RWL"]))

# AFTER:
(policy_rows["Transaction Type"].isin(["NEW", "RWL", "REWRITE"]))
```

5. **Line 13702** - Policy term filtering:
```python
# BEFORE:
elif trans_type in ["NEW", "RWL"] and trans_x_date == selected_xdate:

# AFTER:
elif trans_type in ["NEW", "RWL", "REWRITE"] and trans_x_date == selected_xdate:
```

### Step 3: Update Commission Logic (5 minutes)

**Line 4662** - Commission rate determination:
```python
# BEFORE:
elif current_transaction_type not in ["NEW", "RWL", "NBS", "STL", "BoR"]:

# AFTER:
elif current_transaction_type not in ["NEW", "RWL", "NBS", "STL", "BoR", "REWRITE"]:
```

**Note**: This change is CRITICAL. Without it, REWRITE would get the wrong commission rate logic applied.

### Step 4: Update Documentation & Comments (5 minutes)

1. **Line 4282** - Update comment:
```python
# BEFORE:
# Auto-populate 12-month term for NEW and RWL (except AUTO) - but only as a suggestion

# AFTER:
# Auto-populate 12-month term for NEW, RWL, and REWRITE (except AUTO) - but only as a suggestion
```

2. **Line 12702** - Update help text:
```python
# BEFORE:
- Set NEW and RWL (renewal) rates separately

# AFTER:
- Set NEW, RWL (renewal), and REWRITE rates separately
```

### Step 5: Testing Checklist (5 minutes)

After implementation, verify:

1. **Policy Revenue Ledger**:
   - [ ] REWRITE transaction 2A92ZR7-IMPORT starts a new term group
   - [ ] Term grouping shows correct boundaries

2. **Policy Revenue Ledger Reports**:
   - [ ] Effective Date dropdown includes REWRITE dates
   - [ ] Filtering by REWRITE effective date works correctly

3. **Pending Policy Renewals**:
   - [ ] REWRITE policies appear when approaching expiration
   - [ ] Can renew a REWRITE policy

4. **Commission Calculations**:
   - [ ] REWRITE uses appropriate commission rates
   - [ ] Prior Policy Number logic still works

## Rollback Plan

If issues arise:
1. Revert all changes to lists containing transaction types
2. The changes are isolated and can be reverted line by line
3. No database changes required

## Notes

- REWRITE already uses renewal commission rates (this is correct behavior)
- Prior Policy Number functionality remains unchanged
- This change aligns system behavior with business reality