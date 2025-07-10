# Policy Term Field - User Guide

## What is Policy Term?
The "Policy Term" field stores the duration of an insurance policy in months. This helps the system accurately calculate renewal dates.

## How to Enter Policy Term
- **Enter just the number**: `6` or `12` (not "6 months" or "12 months")
- **The number represents months**: Always enter the term in months
- **Common values**:
  - `3` = 3-month policy
  - `6` = 6-month policy (most common)
  - `9` = 9-month policy
  - `12` = 12-month policy (annual)

## Where to Enter Policy Term

### 1. Add New Policy Transaction Page
When creating a new policy:
- Look for the "Policy Term Months" field on the right side, next to "Transaction Type"
- Select from the dropdown: 3 months, 6 months, 9 months, or 12 months
- This field is optional but recommended for accurate renewals

### 2. Edit Policy Transactions Page
When editing an existing policy:
- The "Policy Term" field appears in the Policy Information section
- You can update it to correct any mistakes
- Changes will affect future renewal calculations

## Examples

| Policy Type | Policy Term | What to Enter |
|------------|-------------|---------------|
| 6-month auto policy | 6 months | `6` |
| Annual homeowners | 12 months | `12` |
| Quarterly commercial | 3 months | `3` |
| 9-month specialty | 9 months | `9` |

## Why This Matters
- **Accurate Renewals**: The Pending Policy Renewals page will show correct future dates
- **Better Planning**: Know exactly when policies need renewal attention
- **Commission Forecasting**: More accurate revenue projections

## Important Notes
1. **Just the number**: Enter only the numeric value (6, not "6 months")
2. **Always in months**: The system assumes the number represents months
3. **Default behavior**: If left blank, the system defaults to 6 months for renewals
4. **Existing policies**: You can update existing policies to add their term

## FAQ

**Q: What if a policy has an unusual term like 18 months?**
A: Currently the system supports 3, 6, 9, and 12-month terms. For other terms, leave blank and the system will default to 6 months.

**Q: Do I need to update all existing policies?**
A: No, it's optional. Focus on updating active policies that will renew soon.

**Q: What happens if I leave it blank?**
A: The system will assume a 6-month term for renewal calculations (current behavior).

**Q: Can I enter "6 months" instead of just "6"?**
A: No, enter only the number. The system knows it represents months.