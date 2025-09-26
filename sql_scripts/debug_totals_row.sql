-- Debug the totals row issue
-- Row 33 has amount 1568.941 but is not being excluded
-- Need to see customer name and detect totals rows properly

-- 1. Show row 33 specifically (using row_number)
SELECT 'Row 33 Details:' as analysis;
WITH numbered_rows AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY "Transaction ID") as row_num
    FROM policies
    WHERE user_email = 'demo@agentcommissiontracker.com'
)
SELECT 
    row_num,
    "Transaction ID",
    "Customer",
    "Transaction Type",
    "Premium Sold",
    "Total Agent Comm",
    "Agent Paid Amount (STMT)",
    CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) as balance
FROM numbered_rows
WHERE row_num = 33;

-- 2. Show last 5 rows with customer names
SELECT 'Last 5 Rows:' as analysis;
WITH numbered_rows AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY "Transaction ID") as row_num,
        COUNT(*) OVER () as total_rows
    FROM policies
    WHERE user_email = 'demo@agentcommissiontracker.com'
)
SELECT 
    row_num,
    "Transaction ID",
    "Customer",
    "Transaction Type",
    "Premium Sold",
    "Total Agent Comm",
    CAST("Total Agent Comm" AS NUMERIC) - COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0) as balance
FROM numbered_rows
WHERE row_num > (total_rows - 5)
ORDER BY row_num;

-- 3. Find rows that look like totals rows (common patterns)
SELECT 'Potential Totals Rows:' as analysis;
SELECT 
    "Transaction ID",
    "Customer",
    "Transaction Type",
    "Premium Sold",
    "Total Agent Comm",
    CAST("Total Agent Comm" AS NUMERIC) as numeric_total_comm
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND (
    LOWER("Customer") LIKE '%total%' OR
    LOWER("Customer") LIKE '%sum%' OR
    "Customer" IS NULL OR
    "Customer" = '' OR
    LOWER("Customer") LIKE '%grand%' OR
    -- Check for rows where Total Agent Comm equals 1568.941
    ABS(CAST("Total Agent Comm" AS NUMERIC) - 1568.941) < 0.01
)
ORDER BY "Transaction ID";

-- 4. Calculate correct total excluding any totals rows
SELECT 'Correct Total Calculation:' as analysis;
SELECT 
    COUNT(*) as total_rows,
    SUM(CASE 
        WHEN ABS(CAST("Total Agent Comm" AS NUMERIC) - 1568.941) < 0.01 THEN 0  -- Exclude the totals row
        ELSE CAST("Total Agent Comm" AS NUMERIC)
    END) as total_agent_comm_excluding_totals,
    SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as total_paid,
    SUM(CASE 
        WHEN ABS(CAST("Total Agent Comm" AS NUMERIC) - 1568.941) < 0.01 THEN 0  -- Exclude the totals row
        ELSE CAST("Total Agent Comm" AS NUMERIC)
    END) - SUM(COALESCE(CAST("Agent Paid Amount (STMT)" AS NUMERIC), 0)) as commission_due_excluding_totals
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Transaction Type" NOT IN ('CAN', 'XCL');

-- 5. Show distribution of Total Agent Comm values to find duplicates
SELECT 'Distribution of Values:' as analysis;
SELECT 
    CAST("Total Agent Comm" AS NUMERIC) as total_agent_comm,
    COUNT(*) as count_of_rows
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
AND "Total Agent Comm" IS NOT NULL
GROUP BY CAST("Total Agent Comm" AS NUMERIC)
HAVING COUNT(*) > 1 OR CAST("Total Agent Comm" AS NUMERIC) > 1000
ORDER BY CAST("Total Agent Comm" AS NUMERIC) DESC;