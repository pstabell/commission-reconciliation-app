-- Fix BOTH Transaction ID dates AND STMT DATE for void transactions 
-- to match their Batch ID (reconciliation_id)

-- First, let's see the current state and what needs to be fixed
WITH batch_info AS (
    SELECT DISTINCT
        reconciliation_id,
        -- Extract date from VOID-IMPORT batch IDs (format: VOID-IMPORT-YYYYMMDD-XXXXXXXX)
        SUBSTRING(reconciliation_id FROM 13 FOR 8) as batch_date_yyyymmdd,
        TO_CHAR(
            TO_DATE(
                SUBSTRING(reconciliation_id FROM 13 FOR 8),
                'YYYYMMDD'
            ),
            'MM/DD/YYYY'
        ) as correct_stmt_date
    FROM policies
    WHERE "Transaction ID" LIKE '%-VOID-%'
      AND reconciliation_id LIKE 'VOID-IMPORT-%'
)
SELECT 
    p."Transaction ID" as current_trans_id,
    -- Build the corrected Transaction ID
    SPLIT_PART(p."Transaction ID", '-VOID-', 1) || '-VOID-' || bi.batch_date_yyyymmdd as correct_trans_id,
    p.reconciliation_id as batch_id,
    p."STMT DATE" as current_stmt_date,
    bi.correct_stmt_date,
    p."Customer",
    p."Policy Number"
FROM policies p
INNER JOIN batch_info bi ON p.reconciliation_id = bi.reconciliation_id
WHERE p."Transaction ID" LIKE '%-VOID-%'
ORDER BY p.reconciliation_id, p."Transaction ID"
LIMIT 20;

-- Count how many records need updating
WITH batch_info AS (
    SELECT DISTINCT
        reconciliation_id,
        SUBSTRING(reconciliation_id FROM 13 FOR 8) as batch_date_yyyymmdd,
        TO_CHAR(
            TO_DATE(
                SUBSTRING(reconciliation_id FROM 13 FOR 8),
                'YYYYMMDD'
            ),
            'MM/DD/YYYY'
        ) as correct_stmt_date
    FROM policies
    WHERE "Transaction ID" LIKE '%-VOID-%'
      AND reconciliation_id LIKE 'VOID-IMPORT-%'
)
SELECT 
    COUNT(*) as total_void_transactions,
    COUNT(CASE 
        WHEN p."Transaction ID" != SPLIT_PART(p."Transaction ID", '-VOID-', 1) || '-VOID-' || bi.batch_date_yyyymmdd 
        THEN 1 
    END) as trans_ids_to_update,
    COUNT(CASE 
        WHEN p."STMT DATE" != bi.correct_stmt_date 
        THEN 1 
    END) as stmt_dates_to_update,
    COUNT(DISTINCT p.reconciliation_id) as batches_affected
FROM policies p
INNER JOIN batch_info bi ON p.reconciliation_id = bi.reconciliation_id
WHERE p."Transaction ID" LIKE '%-VOID-%';

-- Show a summary by batch
WITH batch_info AS (
    SELECT DISTINCT
        reconciliation_id,
        SUBSTRING(reconciliation_id FROM 13 FOR 8) as batch_date_yyyymmdd,
        TO_CHAR(
            TO_DATE(
                SUBSTRING(reconciliation_id FROM 13 FOR 8),
                'YYYYMMDD'
            ),
            'MM/DD/YYYY'
        ) as correct_stmt_date
    FROM policies
    WHERE "Transaction ID" LIKE '%-VOID-%'
      AND reconciliation_id LIKE 'VOID-IMPORT-%'
)
SELECT 
    p.reconciliation_id as batch_id,
    bi.batch_date_yyyymmdd as batch_date,
    bi.correct_stmt_date,
    COUNT(*) as transaction_count,
    STRING_AGG(DISTINCT SPLIT_PART(p."Transaction ID", '-', 3), ', ') as current_trans_dates
FROM policies p
INNER JOIN batch_info bi ON p.reconciliation_id = bi.reconciliation_id
WHERE p."Transaction ID" LIKE '%-VOID-%'
GROUP BY p.reconciliation_id, bi.batch_date_yyyymmdd, bi.correct_stmt_date
ORDER BY p.reconciliation_id;

-- To actually update BOTH the Transaction IDs and STMT DATEs, uncomment and run this:
/*
UPDATE policies p
SET 
    "Transaction ID" = SPLIT_PART(p."Transaction ID", '-VOID-', 1) || '-VOID-' || bi.batch_date_yyyymmdd,
    "STMT DATE" = bi.correct_stmt_date
FROM (
    SELECT DISTINCT
        reconciliation_id,
        SUBSTRING(reconciliation_id FROM 13 FOR 8) as batch_date_yyyymmdd,
        TO_CHAR(
            TO_DATE(
                SUBSTRING(reconciliation_id FROM 13 FOR 8),
                'YYYYMMDD'
            ),
            'MM/DD/YYYY'
        ) as correct_stmt_date
    FROM policies
    WHERE "Transaction ID" LIKE '%-VOID-%'
      AND reconciliation_id LIKE 'VOID-IMPORT-%'
) bi
WHERE p.reconciliation_id = bi.reconciliation_id
  AND p."Transaction ID" LIKE '%-VOID-%';
*/

-- After update, verify the results
/*
SELECT 
    reconciliation_id,
    "STMT DATE",
    SPLIT_PART("Transaction ID", '-VOID-', 2) as trans_id_date,
    COUNT(*) as transaction_count
FROM policies
WHERE "Transaction ID" LIKE '%-VOID-%'
  AND reconciliation_id LIKE 'VOID-IMPORT-%'
GROUP BY reconciliation_id, "STMT DATE", SPLIT_PART("Transaction ID", '-VOID-', 2)
ORDER BY reconciliation_id;
*/