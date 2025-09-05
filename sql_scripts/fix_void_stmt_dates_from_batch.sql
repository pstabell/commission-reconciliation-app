-- Fix STMT DATE for void transactions based on their Batch ID (reconciliation_id)
-- Batch ID format for imports: VOID-IMPORT-YYYYMMDD-XXXXXXXX

-- First, let's see what will be updated
WITH batch_dates AS (
    SELECT DISTINCT
        reconciliation_id,
        -- Extract date from VOID-IMPORT batch IDs
        TO_CHAR(
            TO_DATE(
                SUBSTRING(reconciliation_id FROM 13 FOR 8),
                'YYYYMMDD'
            ),
            'MM/DD/YYYY'
        ) as correct_date
    FROM policies
    WHERE "Transaction ID" LIKE '%-VOID-%'
      AND reconciliation_id LIKE 'VOID-IMPORT-%'
)
SELECT 
    p."Transaction ID",
    p.reconciliation_id,
    p."STMT DATE" as current_date,
    bd.correct_date,
    p."Customer",
    p."Policy Number"
FROM policies p
INNER JOIN batch_dates bd ON p.reconciliation_id = bd.reconciliation_id
WHERE p."Transaction ID" LIKE '%-VOID-%'
  AND p."STMT DATE" != bd.correct_date
ORDER BY p.reconciliation_id, p."Transaction ID";

-- Count how many records need updating
WITH batch_dates AS (
    SELECT DISTINCT
        reconciliation_id,
        TO_CHAR(
            TO_DATE(
                SUBSTRING(reconciliation_id FROM 13 FOR 8),
                'YYYYMMDD'
            ),
            'MM/DD/YYYY'
        ) as correct_date
    FROM policies
    WHERE "Transaction ID" LIKE '%-VOID-%'
      AND reconciliation_id LIKE 'VOID-IMPORT-%'
)
SELECT 
    COUNT(*) as records_to_update,
    COUNT(DISTINCT p.reconciliation_id) as batches_affected
FROM policies p
INNER JOIN batch_dates bd ON p.reconciliation_id = bd.reconciliation_id
WHERE p."Transaction ID" LIKE '%-VOID-%'
  AND p."STMT DATE" != bd.correct_date;

-- To actually update the dates, uncomment and run this:
/*
UPDATE policies p
SET "STMT DATE" = bd.correct_date
FROM (
    SELECT DISTINCT
        reconciliation_id,
        TO_CHAR(
            TO_DATE(
                SUBSTRING(reconciliation_id FROM 13 FOR 8),
                'YYYYMMDD'
            ),
            'MM/DD/YYYY'
        ) as correct_date
    FROM policies
    WHERE "Transaction ID" LIKE '%-VOID-%'
      AND reconciliation_id LIKE 'VOID-IMPORT-%'
) bd
WHERE p.reconciliation_id = bd.reconciliation_id
  AND p."Transaction ID" LIKE '%-VOID-%'
  AND p."STMT DATE" != bd.correct_date;
*/

-- After update, verify the results
/*
SELECT 
    reconciliation_id,
    "STMT DATE",
    COUNT(*) as transaction_count
FROM policies
WHERE "Transaction ID" LIKE '%-VOID-%'
  AND reconciliation_id LIKE 'VOID-IMPORT-%'
GROUP BY reconciliation_id, "STMT DATE"
ORDER BY reconciliation_id;
*/