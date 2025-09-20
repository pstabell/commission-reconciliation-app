-- Investigate where the 41 transactions could have gone

-- 1. Check audit_logs for any policy deletions
SELECT 'Recent audit log entries:' as check;
SELECT * 
FROM audit_logs 
WHERE table_name = 'policies' 
   OR action ILIKE '%delete%'
   OR action ILIKE '%remove%'
   OR details ILIKE '%demo%'
ORDER BY timestamp DESC
LIMIT 20;

-- 2. Check if there's a soft delete column in policies
SELECT 'Check for soft delete columns:' as check;
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'policies'
  AND (column_name LIKE '%delete%' 
       OR column_name LIKE '%removed%'
       OR column_name LIKE '%archived%'
       OR column_name LIKE '%active%'
       OR column_name LIKE '%status%');

-- 3. Look for any hidden/inactive policies
SELECT 'Check for status/active fields:' as check;
SELECT COUNT(*) as total_including_inactive
FROM policies
WHERE 1=1; -- This will show ALL records regardless of any status

-- 4. The 466 number might have included STMT transactions - let's check
SELECT 'Policies by Transaction Type:' as check;
SELECT "Transaction Type", COUNT(*) as count
FROM policies
WHERE user_email = 'demo@agentcommissiontracker.com'
GROUP BY "Transaction Type"
ORDER BY count DESC;

-- 5. Check the Edit Policy Transactions issue - duplicates created today?
SELECT 'Policies updated in last 24 hours:' as check;
SELECT 
    DATE_TRUNC('hour', updated_at) as hour,
    COUNT(*) as policies_updated
FROM policies
WHERE updated_at > NOW() - INTERVAL '24 hours'
GROUP BY DATE_TRUNC('hour', updated_at)
ORDER BY hour DESC;

-- 6. Maybe the 41 were in a different database/schema?
SELECT 'Other schemas with policies tables:' as check;
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_name = 'policies'
  AND table_schema != 'public';