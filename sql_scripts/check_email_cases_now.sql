-- CHECK WHAT'S HAPPENING RIGHT NOW
SELECT user_email, COUNT(*) as count
FROM policies
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
GROUP BY user_email
ORDER BY count DESC;

-- Show total
SELECT COUNT(*) as total_all_demo_variations
FROM policies
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com';

-- Check if any were created/updated recently with wrong case
SELECT user_email, 
       COUNT(*) as count,
       MAX(updated_at) as last_updated
FROM policies
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
GROUP BY user_email
ORDER BY last_updated DESC;