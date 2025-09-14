-- SAFE DELETE SCRIPT FOR DEMO USER DATA ONLY
-- This script will ONLY delete data for Demo@AgentCommissionTracker.com
-- Run this in Supabase SQL Editor

-- First, let's verify what we're about to delete
SELECT 
    'Demo policies to be deleted' as description,
    COUNT(*) as count,
    user_email
FROM policies
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY user_email;

-- Check if there's any related renewal history
SELECT 
    'Demo renewal history to be deleted' as description,
    COUNT(*) as count
FROM renewal_history
WHERE details::text LIKE '%Demo@AgentCommissionTracker.com%';

-- SAFETY CHECK: Show all unique user emails to ensure we're not affecting others
SELECT DISTINCT user_email, COUNT(*) as record_count
FROM policies
GROUP BY user_email
ORDER BY user_email;

-- Uncomment the lines below to actually DELETE (after verifying above)
-- Make sure you're comfortable with what will be deleted!

/*
-- DELETE Demo's policies (this is the main data)
DELETE FROM policies
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- DELETE Demo's renewal history if any
DELETE FROM renewal_history
WHERE details::text LIKE '%Demo@AgentCommissionTracker.com%';

-- Verify deletion was successful
SELECT 
    'Remaining Demo records' as check,
    COUNT(*) as count
FROM policies
WHERE user_email = 'Demo@AgentCommissionTracker.com';
*/

-- Alternative: If you want to be EXTRA safe, you can add more conditions
/*
DELETE FROM policies
WHERE user_email = 'Demo@AgentCommissionTracker.com'
  AND user_email NOT LIKE '%agentcommissiontracker.com'  -- Extra safety to ensure it's really Demo
  AND user_email != 'demo@agentcommissiontracker.com';   -- Don't delete lowercase version
*/