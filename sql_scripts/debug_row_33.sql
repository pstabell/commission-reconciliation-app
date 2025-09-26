-- Debug row 33 which has the totals amount 1568.941
-- Need to see what's in the Customer field to properly exclude it

-- 1. Show details of the row with amount 1568.941
SELECT 'Row with amount 1568.941:' as analysis;
SELECT 
    "Transaction ID",
    "Customer",
    "Transaction Type",
    "Premium Sold",
    "Total Agent Comm",
    "Agent Paid Amount (STMT)",
    CAST("Total Agent Comm" AS NUMERIC) as numeric_total_comm
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND ABS(CAST("Total Agent Comm" AS NUMERIC) - 1568.941) < 0.01;

-- 2. Show all rows ordered by Transaction ID to find row 33
SELECT 'All rows with row numbers:' as analysis;
WITH numbered_rows AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY "Transaction ID") as row_num,
        "Transaction ID",
        "Customer",
        "Transaction Type",
        "Total Agent Comm"
    FROM policies
    WHERE user_email = 'demo@agentcommissiontracker.com'
)
SELECT * FROM numbered_rows
WHERE row_num BETWEEN 28 AND 35;

-- 3. Check for common totals row patterns
SELECT 'Check for totals patterns:' as analysis;
SELECT 
    "Transaction ID",
    "Customer",
    "Transaction Type",
    "Total Agent Comm"
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND (
    "Customer" IS NULL OR 
    "Customer" = '' OR
    TRIM("Customer") = '' OR
    UPPER("Customer") LIKE '%TOTAL%' OR
    UPPER("Customer") LIKE '%SUM%' OR
    UPPER("Customer") LIKE '%GRAND%'
);

-- 4. Calculate the correct total (excluding the 1568.941 row)
SELECT 'Correct calculation excluding totals row:' as analysis;
SELECT 
    SUM(CASE 
        WHEN ABS(CAST("Total Agent Comm" AS NUMERIC) - 1568.941) < 0.01 THEN 0
        WHEN "Transaction Type" IN ('CAN', 'XCL') THEN 0
        ELSE CAST("Total Agent Comm" AS NUMERIC)
    END) as correct_total_agent_comm,
    SUM(CASE 
        WHEN "Transaction Type" IN ('CAN', 'XCL') THEN 0
        ELSE CAST("Agent Paid Amount (STMT)" AS NUMERIC)
    END) as total_paid,
    SUM(CASE 
        WHEN ABS(CAST("Total Agent Comm" AS NUMERIC) - 1568.941) < 0.01 THEN 0
        WHEN "Transaction Type" IN ('CAN', 'XCL') THEN 0
        ELSE CAST("Total Agent Comm" AS NUMERIC)
    END) - 
    SUM(CASE 
        WHEN "Transaction Type" IN ('CAN', 'XCL') THEN 0
        ELSE COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)
    END) as correct_commission_due
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com';

-- 5. Show the last few rows to see if there's a pattern
SELECT 'Last 10 rows:' as analysis;
SELECT 
    "Transaction ID",
    "Customer",
    "Transaction Type",
    "Total Agent Comm"
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
ORDER BY "Transaction ID" DESC
LIMIT 10;