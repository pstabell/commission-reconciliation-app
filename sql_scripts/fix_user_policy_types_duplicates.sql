-- Check for duplicate user_ids in the table
SELECT user_id, user_email, COUNT(*) as count
FROM user_policy_types
WHERE user_id IS NOT NULL
GROUP BY user_id, user_email
HAVING COUNT(*) > 1
ORDER BY count DESC;

-- See all rows for users with duplicates
SELECT * FROM user_policy_types
WHERE user_id IN (
    SELECT user_id 
    FROM user_policy_types 
    WHERE user_id IS NOT NULL
    GROUP BY user_id 
    HAVING COUNT(*) > 1
)
ORDER BY user_id, created_at;

-- Clean up duplicates - keep the newest row with data
WITH duplicates AS (
    SELECT id, user_id, user_email, policy_types,
           ROW_NUMBER() OVER (
               PARTITION BY user_id 
               ORDER BY 
                   CASE WHEN policy_types != '[]'::jsonb THEN 0 ELSE 1 END,  -- Prefer rows with data
                   created_at DESC  -- Then prefer newest
           ) as rn
    FROM user_policy_types
    WHERE user_id IS NOT NULL
)
DELETE FROM user_policy_types
WHERE id IN (
    SELECT id FROM duplicates WHERE rn > 1
);

-- Now try adding the constraint again
ALTER TABLE user_policy_types 
ADD CONSTRAINT unique_user_id UNIQUE(user_id);

-- Verify the fix
SELECT 'After cleanup:' as status, COUNT(*) as total_rows, COUNT(DISTINCT user_id) as unique_users
FROM user_policy_types;