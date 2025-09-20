-- STEP 3: Update policies table with user_id
-- Run this third

-- Update policies with user_id (this is the biggest table)
UPDATE policies p
SET user_id = u.id
FROM users u
WHERE LOWER(p.user_email) = LOWER(u.email)
AND p.user_id IS NULL;

-- Verify the update worked
SELECT 
    COUNT(*) as total_policies,
    COUNT(user_id) as policies_with_user_id,
    COUNT(*) - COUNT(user_id) as missing_user_id
FROM policies
WHERE user_email IS NOT NULL;

-- Check demo user specifically
SELECT COUNT(*) as demo_policies
FROM policies p
JOIN users u ON p.user_id = u.id
WHERE u.email = 'demo@agentcommissiontracker.com';