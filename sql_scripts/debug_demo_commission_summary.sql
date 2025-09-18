-- Debug why Agent Commission Estimated shows $0.00 on dashboard

-- Check 2025 unreconciled transactions that should show in "Unreconciled (Estimated)"
SELECT 
    COUNT(*) as total_2025_unreconciled,
    COUNT(CASE WHEN "Agent Estimated Comm $" IS NOT NULL THEN 1 END) as has_agent_comm,
    SUM(COALESCE("Premium Sold"::NUMERIC, 0)) as premium_sum,
    SUM(COALESCE("Agent Estimated Comm $"::NUMERIC, 0)) as agent_comm_sum
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction Type" NOT IN ('PMT', 'ADJ')  -- Exclude payment entries
    AND "Effective Date" >= '2025-01-01'
    AND "Effective Date" <= '2025-12-31'
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%')  -- Unreconciled
    AND ("reconciliation_status" IS NULL OR "reconciliation_status" = '');

-- Look at a sample of 2025 policies to see their commission values
SELECT 
    "Policy Number",
    "Transaction Type",
    "Effective Date",
    "Premium Sold",
    "Policy Gross Comm %",
    "Agent Comm %",
    "Agent Estimated Comm $",
    "Transaction ID",
    "reconciliation_status"
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Effective Date" >= '2025-01-01'
    AND "Effective Date" <= '2025-12-31'
    AND ("Transaction ID" IS NULL OR "Transaction ID" NOT LIKE '%-STMT-%')
ORDER BY "Effective Date" DESC
LIMIT 10;

-- Check if the issue is with the Transaction ID pattern
SELECT 
    CASE 
        WHEN "Transaction ID" IS NULL THEN 'NULL Transaction ID'
        WHEN "Transaction ID" = '' THEN 'Empty Transaction ID'
        WHEN "Transaction ID" LIKE '%-STMT-%' THEN 'Reconciled (has -STMT-)'
        ELSE 'Unreconciled (no -STMT-)'
    END as transaction_status,
    COUNT(*) as count,
    SUM(CASE 
        WHEN "Agent Estimated Comm $" IS NULL THEN 0
        WHEN "Agent Estimated Comm $"::TEXT = '' THEN 0
        ELSE "Agent Estimated Comm $"::NUMERIC
    END) as total_agent_comm
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Effective Date" >= '2025-01-01'
GROUP BY transaction_status;