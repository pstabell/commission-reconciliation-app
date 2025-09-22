-- Migrate existing global settings to user-specific settings
-- This populates the new user settings tables with default values

-- 1. Create default column mappings for all users
INSERT INTO user_column_mappings (user_id, user_email, column_mappings)
SELECT 
    id as user_id,
    email as user_email,
    '{
        "Agent Comm %": "Agent Comm %",
        "Agency Estimated Comm/Revenue (CRM)": "Agency Estimated Comm/Revenue (CRM)",
        "Agent Estimated Comm $": "Agent Estimated Comm $",
        "Agent Paid Amount (STMT)": "Agent Paid Amount (STMT)",
        "Agency Comm Received (STMT)": "Agency Comm Received (STMT)",
        "Policy Gross Comm %": "Policy Gross Comm %",
        "Premium Sold": "Premium Sold",
        "Policy Balance Due": "Policy Balance Due",
        "Customer": "Customer",
        "Policy Number": "Policy Number",
        "Transaction Type": "Transaction Type",
        "Effective Date": "Effective Date",
        "X-DATE": "X-DATE"
    }'::jsonb
FROM users
ON CONFLICT (user_id) DO NOTHING;

-- 2. Create default preferences for all users
INSERT INTO user_preferences (user_id, user_email, color_theme)
SELECT 
    id as user_id,
    email as user_email,
    'light' as color_theme
FROM users
ON CONFLICT (user_id) DO NOTHING;

-- 3. Create default agent rates for all users
INSERT INTO user_default_agent_rates (user_id, user_email, new_business_rate, renewal_rate)
SELECT 
    id as user_id,
    email as user_email,
    50.00 as new_business_rate,
    25.00 as renewal_rate
FROM users
ON CONFLICT (user_id) DO NOTHING;

-- 4. Create default policy types for all users
INSERT INTO user_policy_types (user_id, user_email, policy_type, display_order)
SELECT 
    u.id as user_id,
    u.email as user_email,
    pt.policy_type,
    pt.display_order
FROM users u
CROSS JOIN (
    VALUES 
        ('Personal Lines', 1),
        ('Commercial Lines', 2),
        ('Homeowners', 3),
        ('Auto', 4),
        ('Umbrella', 5),
        ('Flood', 6),
        ('Other', 99)
) as pt(policy_type, display_order)
ON CONFLICT (user_id, policy_type) DO NOTHING;

-- 5. Create default transaction types for all users
INSERT INTO user_transaction_types (user_id, user_email, transaction_type, category, display_order)
SELECT 
    u.id as user_id,
    u.email as user_email,
    tt.transaction_type,
    tt.category,
    tt.display_order
FROM users u
CROSS JOIN (
    VALUES 
        ('NEW', 'New Business', 1),
        ('RENEWAL', 'Renewal', 2),
        ('RWRITE', 'Rewrite', 3),
        ('BOR', 'Broker of Record', 4),
        ('XLN', 'Cancellation', 5),
        ('REINST', 'Reinstatement', 6),
        ('PCANCEL', 'Policy Cancellation', 7),
        ('ADJ', 'Adjustment', 8)
) as tt(transaction_type, category, display_order)
ON CONFLICT (user_id, transaction_type) DO NOTHING;

-- 6. Create default policy type mappings for all users
INSERT INTO user_policy_type_mappings (user_id, user_email, statement_value, mapped_type)
SELECT 
    u.id as user_id,
    u.email as user_email,
    ptm.statement_value,
    ptm.mapped_type
FROM users u
CROSS JOIN (
    VALUES 
        ('Personal', 'Personal Lines'),
        ('Commercial', 'Commercial Lines'),
        ('HO', 'Homeowners'),
        ('Auto', 'Auto'),
        ('Flood', 'Flood')
) as ptm(statement_value, mapped_type)
ON CONFLICT (user_id, statement_value) DO NOTHING;

-- 7. Create default transaction type mappings for all users
INSERT INTO user_transaction_type_mappings (user_id, user_email, statement_code, mapped_type)
SELECT 
    u.id as user_id,
    u.email as user_email,
    ttm.statement_code,
    ttm.mapped_type
FROM users u
CROSS JOIN (
    VALUES 
        ('01', 'NEW'),
        ('02', 'RENEWAL'),
        ('03', 'RWRITE'),
        ('04', 'BOR'),
        ('05', 'XLN'),
        ('06', 'REINST')
) as ttm(statement_code, mapped_type)
ON CONFLICT (user_id, statement_code) DO NOTHING;

-- Verify migration
SELECT 'Migration Summary:' as status;
SELECT 
    'user_column_mappings' as table_name, 
    COUNT(*) as record_count 
FROM user_column_mappings
UNION ALL
SELECT 
    'user_preferences', 
    COUNT(*) 
FROM user_preferences
UNION ALL
SELECT 
    'user_default_agent_rates', 
    COUNT(*) 
FROM user_default_agent_rates
UNION ALL
SELECT 
    'user_policy_types', 
    COUNT(*) 
FROM user_policy_types
UNION ALL
SELECT 
    'user_transaction_types', 
    COUNT(*) 
FROM user_transaction_types;