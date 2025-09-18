-- Check commission-related fields in demo data

-- Check if Agent Comm % field has values
SELECT 
    COUNT(*) as total_policies,
    COUNT("Agent Comm %") as has_agent_comm_percent,
    COUNT(CASE WHEN "Agent Comm %" IS NOT NULL AND "Agent Comm %" != '' AND "Agent Comm %" != '0' THEN 1 END) as has_valid_agent_comm,
    COUNT("Policy Gross Comm %") as has_policy_gross_comm,
    COUNT(CASE WHEN "Policy Gross Comm %" IS NOT NULL AND "Policy Gross Comm %" != '' AND "Policy Gross Comm %" != '0' THEN 1 END) as has_valid_policy_comm
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction ID" NOT LIKE '%-STMT-%';

-- Show sample of non-reconciliation records to see commission fields
SELECT 
    "Transaction ID",
    "Transaction Type",
    "Premium Sold",
    "Policy Gross Comm %",
    "Agent Comm %",
    "Agency Estimated Comm/Revenue (CRM)",
    "Agent Estimated Comm $"
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction ID" NOT LIKE '%-STMT-%'
    AND "Transaction Type" IN ('NEW', 'RWL')
LIMIT 10;

-- Check for 2025 unreconciled transactions
SELECT 
    COUNT(*) as count_2025_unreconciled,
    SUM(CAST(NULLIF("Premium Sold", '') AS NUMERIC)) as total_premium,
    SUM(CAST(NULLIF("Agent Estimated Comm $", '') AS NUMERIC)) as total_agent_comm
FROM policies
WHERE 
    user_email = 'demo@agentcommissiontracker.com'
    AND "Transaction ID" NOT LIKE '%-STMT-%'
    AND "Effective Date" >= '2025-01-01'
    AND ("reconciliation_status" IS NULL OR "reconciliation_status" = '');