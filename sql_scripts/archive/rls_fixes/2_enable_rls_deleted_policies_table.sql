-- =====================================================
-- RLS Setup for DELETED_POLICIES Table
-- Run this BEFORE enabling RLS on the deleted_policies table
-- =====================================================

-- Step 1: Drop any existing policies to start fresh
DROP POLICY IF EXISTS "Enable all operations for anon key" ON deleted_policies;

-- Step 2: Create a permissive policy for the anon role
-- This allows your app (using anon key) to perform all operations
CREATE POLICY "Enable all operations for anon key" 
ON deleted_policies
FOR ALL                    -- Covers SELECT, INSERT, UPDATE, DELETE
TO anon                    -- Applies to anonymous/public access (your app)
USING (true)              -- No restrictions on reading
WITH CHECK (true);        -- No restrictions on writing

-- Step 3: Ensure anon role has necessary permissions
GRANT ALL ON deleted_policies TO anon;

-- Step 4: Enable RLS (Run this separately after confirming the policy is created)
-- ALTER TABLE deleted_policies ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- TEST QUERIES (Run these after enabling RLS)
-- =====================================================

-- Test 1: Can you read deletion history?
-- Expected: Should return a count (might be 0 if no deletions yet)
SELECT COUNT(*) as total_deleted FROM deleted_policies;

-- Test 2: Can you read specific deleted records?
-- Expected: Should return data if any records exist
SELECT transaction_id, customer_name, deleted_at 
FROM deleted_policies 
LIMIT 5;

-- Test 3: Test the restore functionality (read policy_data)
-- Expected: Should show the JSON data
SELECT transaction_id, policy_data->>'Customer' as customer
FROM deleted_policies 
LIMIT 1;

-- If any test fails, disable RLS immediately:
-- ALTER TABLE deleted_policies DISABLE ROW LEVEL SECURITY;