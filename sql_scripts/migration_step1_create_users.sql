-- STEP 1: Create users for all existing emails
-- Run this first

-- Insert all unique emails into users table
INSERT INTO users (email)
SELECT DISTINCT LOWER(user_email) as email
FROM (
    SELECT user_email FROM policies WHERE user_email IS NOT NULL
    UNION
    SELECT user_email FROM carriers WHERE user_email IS NOT NULL
    UNION
    SELECT user_email FROM mgas WHERE user_email IS NOT NULL
    UNION
    SELECT user_email FROM commission_rules WHERE user_email IS NOT NULL
) all_emails
ON CONFLICT (email) DO NOTHING;

-- Verify users were created
SELECT id, email 
FROM users 
WHERE email IN ('demo@agentcommissiontracker.com', 'demo@agentcommissiontracker.com')
ORDER BY email;