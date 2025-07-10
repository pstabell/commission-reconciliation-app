# Policy Term Column - Quick Implementation Guide

## Why Add Policy Term?
Currently, the Pending Policy Renewals page assumes ALL policies have 6-month terms, which causes incorrect renewal dates for 12-month policies.

## Quick Steps to Implement

### 1. Run SQL to Add Column
```bash
# In your database
sql_scripts/add_policy_term_column.sql
```

### 2. Update Column Mapping
In `column_mapping_config.py`, add after "Policy Type":
```python
"Policy Term": "Policy Term",
```

### 3. Key Code Changes Needed

**Most Important Change** - Fix the renewal calculation (line 1934):
- Current: `pd.DateOffset(months=6)` (hardcoded)
- New: Use actual policy term from the new column

**Add to Forms**:
- Add New Policy Transaction form
- Edit Policy modal
- Include dropdown with options: "6 months", "12 months", etc.

### 4. Migration for Existing Data
The SQL script includes an optional UPDATE query that can calculate terms from existing dates:
- 170-190 days = 6 months
- 355-375 days = 12 months

## Expected Results
- The app continues to use the last transaction's expiration date as the renewal's effective date
- 6-month policies will get new expiration dates 6 months after their effective date
- 12-month policies will get new expiration dates 12 months after their effective date
- More accurate commission forecasting
- Better renewal tracking that respects actual policy terms

## Files Created
1. `sql_scripts/add_policy_term_column.sql` - Database changes
2. `docs/POLICY_TERM_IMPLEMENTATION_PLAN.md` - Detailed implementation guide
3. `POLICY_TERM_QUICK_GUIDE.md` - This quick reference