-- Verify what's really in the policies table

-- 1. Show the ONE email and its count
SELECT 'The only email in policies table:' as check;
SELECT user_email, COUNT(*) as total_policies
FROM policies
GROUP BY user_email;

-- 2. Total count (should match above)
SELECT 'Total policies count:' as check;
SELECT COUNT(*) as total
FROM policies;

-- 3. Check when policies were last updated (to see if any were recently deleted)
SELECT 'Recent update activity:' as check;
SELECT 
    DATE(updated_at) as update_date,
    COUNT(*) as policies_touched
FROM policies
WHERE updated_at IS NOT NULL
GROUP BY DATE(updated_at)
ORDER BY update_date DESC
LIMIT 7;

-- 4. Check if we can see any pattern in transaction IDs that might indicate deletion
SELECT 'Transaction ID patterns (first 10 and last 10):' as check;
(SELECT "Transaction ID", "Customer", "Premium Sold" 
 FROM policies 
 ORDER BY "Transaction ID" ASC 
 LIMIT 10)
UNION ALL
(SELECT "Transaction ID", "Customer", "Premium Sold" 
 FROM policies 
 ORDER BY "Transaction ID" DESC 
 LIMIT 10);

-- 5. Is there a reconciliations or audit table that might show deletions?
SELECT 'Check for reconciliation/audit tables:' as check;
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND (table_name LIKE '%audit%' 
       OR table_name LIKE '%history%' 
       OR table_name LIKE '%deleted%'
       OR table_name LIKE '%archive%');