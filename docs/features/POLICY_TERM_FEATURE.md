# Policy Term Feature - Complete Documentation

## Overview
The Policy Term feature allows tracking of policy duration in months (3, 6, 9, 12, or Custom) to ensure accurate renewal date calculations. Previously, the system assumed all policies had 6-month terms, which caused incorrect renewal dates for annual policies.

### Recent Updates (July 30, 2025)
- Fixed issue where user changes were being overridden (forced to 12 months)
- Added "Custom" option for non-standard terms (e.g., cancellations)
- Implemented auto-update of X-DATE when Policy Term changes
- Enhanced Calculate button to update X-DATE based on Policy Term

## Implementation Summary

### Database Changes
- Added "Policy Term" column ~~as INTEGER~~ now TEXT type to store months or "Custom"
- Updated CHECK constraint to ensure valid values ('3', '6', '9', '12', 'Custom')
- Added index for performance optimization
- Run `sql_scripts/update_policy_term_constraint_for_custom.sql` to update existing databases

### UI Changes
1. **Add New Policy Transaction Form**
   - Policy Term Months dropdown added next to Transaction Type
   - Options: blank (default), 3 months, 6 months, 9 months, 12 months, Custom

2. **Edit Policy Modal**
   - Policy Term Months field in Policy Information section
   - Properly handles existing values and null/empty values
   - X-DATE auto-updates when Policy Term is changed (except Custom)
   - Shows info message about pending X-DATE calculation
   - Calculate button applies the X-DATE update

3. **Renewal Calculations**
   - Updated to use actual Policy Term value
   - Falls back to 6 months if not specified (preserving current behavior)
   - Formula: New Expiration = Previous Expiration + Policy Term months

4. **Auto-Calculation Behavior**
   - NEW/RWL transactions suggest 12-month term but can be overridden
   - Changing Policy Term shows pending X-DATE calculation
   - Calculate button updates X-DATE to Effective Date + Policy Term
   - Custom option allows manual X-DATE entry without auto-calculation

## User Guide

### How to Use Policy Term

1. **When Adding a New Policy**
   - Look for "Policy Term Months" dropdown on the right side
   - Select the appropriate term: 3, 6, 9, 12 months, or Custom
   - Leave blank if unknown (defaults to 6 months for renewals)
   - X-DATE updates automatically based on your selection

2. **When Editing a Policy**
   - Find "Policy Term Months" in the Policy Information section
   - Change the term and X-DATE will show pending calculation
   - Click Calculate button to apply the X-DATE change
   - Your changes are now respected and not overridden!

3. **Common Values**
   - 3 months = Quarterly policies
   - 6 months = Semi-annual policies (most common)
   - 9 months = Three-quarter year policies
   - 12 months = Annual policies
   - Custom = Special cases (cancellations, non-standard terms)

4. **Using Custom Policy Term**
   - Select "Custom" when dates don't follow standard patterns
   - Manually enter the X-DATE as needed
   - No automatic calculation occurs
   - Useful for cancellations or special endorsements

### Why This Matters
- **Accurate Renewals**: Pending Policy Renewals page shows correct future dates
- **Better Planning**: Know exactly when policies need renewal attention
- **Commission Forecasting**: More accurate revenue projections

## Migration Guide for Existing Data

### Automatic Population
You can automatically calculate and populate Policy Terms for existing policies based on the date difference between Effective Date and X-DATE.

#### Preview Query (Safe - No Changes)
```sql
-- See what Policy Terms would be assigned
SELECT 
    "Customer",
    "Policy Number",
    "Effective Date",
    "X-DATE",
    DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) as days,
    CASE 
        WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 80 AND 100 THEN '3 months'
        WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 170 AND 190 THEN '6 months'
        WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 260 AND 280 THEN '9 months'
        WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 355 AND 375 THEN '12 months'
        ELSE 'Will stay empty - review manually'
    END as what_will_be_set
FROM policies
WHERE "Policy Term" IS NULL 
    AND "Transaction Type" IN ('NEW', 'RWL')
    AND "X-DATE" IS NOT NULL 
    AND "Effective Date" IS NOT NULL
ORDER BY "Customer"
LIMIT 20;
```

#### Update Query (Execute When Ready)
```sql
UPDATE policies 
SET "Policy Term" = 
  CASE 
    WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 80 AND 100 THEN 3
    WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 170 AND 190 THEN 6
    WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 260 AND 280 THEN 9
    WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 355 AND 375 THEN 12
    ELSE NULL
  END
WHERE "Policy Term" IS NULL 
  AND "Transaction Type" IN ('NEW', 'RWL');
```

#### Verify Results
```sql
-- See how many got updated
SELECT 
    CASE "Policy Term"
        WHEN 3 THEN '3-month policies'
        WHEN 6 THEN '6-month policies'
        WHEN 9 THEN '9-month policies'
        WHEN 12 THEN '12-month policies'
        ELSE 'Still need review'
    END as policy_type,
    COUNT(*) as count
FROM policies
WHERE "Transaction Type" IN ('NEW', 'RWL')
GROUP BY "Policy Term"
ORDER BY "Policy Term";
```

### Date Range Logic
The ranges account for month variations:
- ~90 days (80-100) = 3-month policy
- ~180 days (170-190) = 6-month policy  
- ~270 days (260-280) = 9-month policy
- ~365 days (355-375) = 12-month policy

## Technical Implementation Details

### Modified Files
1. **commission_app.py**
   - Line 3990-3999: Added Policy Term dropdown to Add form
   - Line 4146: Added Policy Term to new_policy data
   - Line 3074: Added 'Policy Term Months' to policy_fields
   - Line 3155-3175: Added Policy Term handling in Edit modal
   - Line 1935-1942: Updated renewal calculation to use Policy Term

2. **column_mapping_config.py**
   - Line 39: Added "Policy Term Months": "Policy Term" mapping

3. **SQL Script**
   - `sql_scripts/add_policy_term_column.sql`

### Form Layout
- **Add New Policy**: Transaction Type (left) | Policy Term Months (right)
- **Edit Policy**: Appears after Transaction Type in Policy Information section

## Testing Checklist

- [ ] **Add New Policy**: Policy Term dropdown appears and saves correctly
- [ ] **Edit Policy**: Shows existing values and allows updates
- [ ] **Pending Renewals**: Respects actual policy terms for renewal dates
- [ ] **Data Display**: Policy Term appears in all relevant views
- [ ] **Exports**: Include Policy Term column
- [ ] **Migration**: Existing policies can be updated via SQL

## FAQ

**Q: What if a policy has an unusual term like 18 months?**
A: Use the "Custom" option and manually set the X-DATE to the correct expiration.

**Q: Why were my Policy Term changes being overridden?**
A: This was a bug where NEW/RWL transactions forced 12 months. Fixed as of July 30, 2025.

**Q: Do I need to update all existing policies?**
A: No, it's optional. Focus on active policies that will renew soon.

**Q: What happens if left blank?**
A: System assumes 6-month term for renewal calculations (preserves current behavior).

**Q: How do I handle policy cancellations mid-term?**
A: Select "Custom" for Policy Term and set X-DATE to the cancellation date.

## Future Enhancements
- Support for custom policy terms beyond the standard options
- Automatic term detection from carrier data imports
- Policy term analytics and reporting