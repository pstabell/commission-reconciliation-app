-- Debug why unreconciled 2025 transactions show $0 commission

-- 1. Check the Total Agent Comm values for unreconciled 2025 transactions
SELECT 
    COUNT(*) as count,
    SUM(CASE 
        WHEN "Total Agent Comm" IS NULL THEN 0
        WHEN "Total Agent Comm"::TEXT = '' THEN 0
        ELSE "Total Agent Comm"::NUMERIC
    END) as total_agent_comm_sum,
    SUM(CASE 
        WHEN "Agent Estimated Comm $" IS NULL THEN 0
        WHEN "Agent Estimated Comm $"::TEXT = '' THEN 0
        ELSE "Agent Estimated Comm $"::NUMERIC
    END) as agent_estimated_sum
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Effective Date"::DATE >= '2025-01-01'
    AND "Effective Date"::DATE <= '2025-12-31'
    AND "Transaction ID" NOT LIKE '%-STMT-%'
    AND "Transaction ID" NOT LIKE '%-VOID-%'
    AND "Transaction ID" NOT LIKE '%-ADJ-%'
    AND "Transaction Type" NOT IN ('PMT', 'ADJ');

-- 2. Show sample of unreconciled 2025 transactions with commission values
SELECT 
    "Policy Number",
    "Transaction Type",
    "Effective Date",
    "Transaction ID",
    "Premium Sold",
    "Agent Estimated Comm $",
    "Total Agent Comm"
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Effective Date"::DATE >= '2025-01-01'
    AND "Effective Date"::DATE <= '2025-12-31'
    AND "Transaction ID" NOT LIKE '%-STMT-%'
    AND "Transaction ID" NOT LIKE '%-VOID-%'
    AND "Transaction ID" NOT LIKE '%-ADJ-%'
    AND "Transaction Type" NOT IN ('PMT', 'ADJ')
LIMIT 10;

-- 3. Check if there are any -STMT- entries with 2025 effective dates
SELECT 
    COUNT(*) as stmt_count_2025_eff_date
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction ID" LIKE '%-STMT-%'
    AND "Effective Date"::DATE >= '2025-01-01'
    AND "Effective Date"::DATE <= '2025-12-31';