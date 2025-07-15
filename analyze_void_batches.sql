-- Analyze void transactions and their batch relationships

-- 1. Show all unique batch IDs for void transactions
SELECT DISTINCT 
    reconciliation_id as batch_id,
    COUNT(*) as transaction_count
FROM policies
WHERE "Transaction ID" LIKE '%-VOID-%'
GROUP BY reconciliation_id
ORDER BY reconciliation_id;

-- 2. Show sample void transactions with their batch IDs
SELECT 
    "Transaction ID",
    reconciliation_id as batch_id,
    "STMT DATE",
    "Customer",
    "Policy Number",
    "NOTES"
FROM policies
WHERE "Transaction ID" LIKE '%-VOID-%'
ORDER BY reconciliation_id, "Transaction ID"
LIMIT 20;

-- 3. For VOID-IMPORT batches, extract the correct date and show what needs updating
WITH void_import_batches AS (
    SELECT DISTINCT
        reconciliation_id as batch_id,
        -- Extract date from batch ID format: VOID-IMPORT-YYYYMMDD-XXXXXXXX
        CASE 
            WHEN reconciliation_id LIKE 'VOID-IMPORT-%' THEN
                TO_CHAR(
                    TO_DATE(
                        SUBSTRING(reconciliation_id FROM 13 FOR 8),
                        'YYYYMMDD'
                    ),
                    'MM/DD/YYYY'
                )
            ELSE NULL
        END as correct_stmt_date
    FROM policies
    WHERE "Transaction ID" LIKE '%-VOID-%'
      AND reconciliation_id LIKE 'VOID-IMPORT-%'
)
SELECT 
    p."Transaction ID",
    p.reconciliation_id as batch_id,
    p."STMT DATE" as current_stmt_date,
    vib.correct_stmt_date,
    CASE 
        WHEN p."STMT DATE" != vib.correct_stmt_date THEN 'Needs Update'
        ELSE 'Already Correct'
    END as status
FROM policies p
INNER JOIN void_import_batches vib ON p.reconciliation_id = vib.batch_id
WHERE p."Transaction ID" LIKE '%-VOID-%'
ORDER BY p.reconciliation_id, p."Transaction ID";