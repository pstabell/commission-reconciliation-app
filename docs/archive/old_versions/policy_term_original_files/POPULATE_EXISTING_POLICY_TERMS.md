# How to Populate Policy Terms for Existing Policies

## Overview
You have existing policies in your database that don't have the Policy Term field filled in. We can automatically calculate and set these terms by looking at the number of days between the Effective Date and X-DATE (expiration date).

## The Logic
The SQL query calculates the number of days between Effective Date and X-DATE, then assigns a term:
- **~90 days** (80-100) → 3-month policy
- **~180 days** (170-190) → 6-month policy  
- **~270 days** (260-280) → 9-month policy
- **~365 days** (355-375) → 12-month policy
- **Anything else** → Leaves as NULL (you can review manually)

## Step 1: Preview What Will Be Updated
First, let's see what the query will do WITHOUT making changes:

```sql
-- PREVIEW: See what Policy Terms would be assigned
SELECT 
    "Customer",
    "Policy Number",
    "Transaction Type",
    "Effective Date",
    "X-DATE",
    DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) as days_difference,
    CASE 
        WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 80 AND 100 THEN 3
        WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 170 AND 190 THEN 6
        WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 260 AND 280 THEN 9
        WHEN DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 355 AND 375 THEN 12
        ELSE NULL
    END as suggested_policy_term
FROM policies
WHERE "Policy Term" IS NULL 
    AND "Transaction Type" IN ('NEW', 'RWL')
    AND "X-DATE" IS NOT NULL 
    AND "Effective Date" IS NOT NULL
ORDER BY days_difference;
```

## Step 2: Check for Outliers
Look for policies that won't get a term assigned (unusual date ranges):

```sql
-- Find policies with unusual term lengths
SELECT 
    "Customer",
    "Policy Number",
    "Effective Date",
    "X-DATE",
    DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) as days_difference
FROM policies
WHERE "Policy Term" IS NULL 
    AND "Transaction Type" IN ('NEW', 'RWL')
    AND "X-DATE" IS NOT NULL 
    AND "Effective Date" IS NOT NULL
    AND DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) NOT IN (
        SELECT DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY'))
        FROM policies
        WHERE DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 80 AND 100
           OR DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 170 AND 190
           OR DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 260 AND 280
           OR DATE_PART('day', TO_DATE("X-DATE", 'MM/DD/YYYY') - TO_DATE("Effective Date", 'MM/DD/YYYY')) BETWEEN 355 AND 375
    )
ORDER BY days_difference;
```

## Step 3: Run the Update (When Ready)
Once you're satisfied with the preview, run the actual update:

```sql
-- UPDATE: Set Policy Terms based on date calculations
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
  AND "Transaction Type" IN ('NEW', 'RWL')
  AND "X-DATE" IS NOT NULL 
  AND "Effective Date" IS NOT NULL;
```

## Step 4: Verify the Results
Check how many policies were updated:

```sql
-- Count policies by term
SELECT 
    "Policy Term",
    COUNT(*) as policy_count
FROM policies
WHERE "Transaction Type" IN ('NEW', 'RWL')
GROUP BY "Policy Term"
ORDER BY "Policy Term";
```

## Why the Date Ranges?

The ranges account for variations in actual days:
- **3 months**: 80-100 days (covers Feb with 28 days, months with 30-31 days)
- **6 months**: 170-190 days (typically 180-183 days)
- **9 months**: 260-280 days (typically 270-274 days)
- **12 months**: 355-375 days (covers regular years and leap years)

## Manual Review Needed

After running the update, you should manually review:
1. Policies that still have NULL Policy Term (unusual date ranges)
2. Very old policies where date calculations might be off
3. Policies with special circumstances

You can find these with:
```sql
-- Find policies that still need Policy Term set
SELECT 
    "Customer",
    "Policy Number",
    "Effective Date",
    "X-DATE"
FROM policies
WHERE "Policy Term" IS NULL
  AND "Transaction Type" IN ('NEW', 'RWL')
ORDER BY "Customer";
```

## Benefits
- Instantly populates terms for most existing policies
- Improves renewal calculation accuracy immediately
- Identifies outliers that need manual attention
- No risk to existing data (only fills NULL values)