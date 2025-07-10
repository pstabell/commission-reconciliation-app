# Quick Start: Auto-Fill Policy Terms for Existing Policies

## What This Does
Automatically calculates and fills in the Policy Term field for your existing policies by looking at how many days are between Effective Date and X-DATE.

## Safe Preview First (Run This)
```sql
-- SEE WHAT WILL HAPPEN (no changes made)
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

## The Actual Update (Run When Ready)
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

## Check Results
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

## The Math
- ~90 days = 3-month policy
- ~180 days = 6-month policy
- ~270 days = 9-month policy
- ~365 days = 12-month policy

We use ranges (like 170-190 days for 6 months) to handle month variations!