-- Fix STMT DATE for void transactions to match the date in their Transaction ID
-- Transaction ID format: XXXXXXX-VOID-YYYYMMDD

-- First, let's see what needs to be updated
WITH void_transactions AS (
    SELECT 
        "Transaction ID",
        "STMT DATE" as current_stmt_date,
        -- Extract date from Transaction ID and format as MM/DD/YYYY
        TO_CHAR(
            TO_DATE(
                SUBSTRING("Transaction ID" FROM POSITION('-VOID-' IN "Transaction ID") + 6 FOR 8),
                'YYYYMMDD'
            ),
            'MM/DD/YYYY'
        ) as correct_stmt_date
    FROM policies
    WHERE "Transaction ID" LIKE '%-VOID-%'
)
SELECT 
    "Transaction ID",
    current_stmt_date,
    correct_stmt_date,
    CASE 
        WHEN current_stmt_date != correct_stmt_date THEN 'Needs Update'
        ELSE 'Already Correct'
    END as status
FROM void_transactions
ORDER BY correct_stmt_date DESC, "Transaction ID";

-- To actually update the dates, uncomment and run this:
/*
UPDATE policies
SET "STMT DATE" = TO_CHAR(
    TO_DATE(
        SUBSTRING("Transaction ID" FROM POSITION('-VOID-' IN "Transaction ID") + 6 FOR 8),
        'YYYYMMDD'
    ),
    'MM/DD/YYYY'
)
WHERE "Transaction ID" LIKE '%-VOID-%'
  AND "STMT DATE" != TO_CHAR(
    TO_DATE(
        SUBSTRING("Transaction ID" FROM POSITION('-VOID-' IN "Transaction ID") + 6 FOR 8),
        'YYYYMMDD'
    ),
    'MM/DD/YYYY'
  );
*/