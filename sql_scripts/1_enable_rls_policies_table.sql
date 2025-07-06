-- =====================================================
-- RLS Setup for POLICIES Table
-- Run this BEFORE enabling RLS on the policies table
-- =====================================================

-- Step 1: Drop any existing policies to start fresh
DROP POLICY IF EXISTS "Enable all operations for anon key" ON policies;

-- Step 2: Create a permissive policy for the anon role
-- This allows your app (using anon key) to perform all operations
CREATE POLICY "Enable all operations for anon key" 
ON policies
FOR ALL                    -- Covers SELECT, INSERT, UPDATE, DELETE
TO anon                    -- Applies to anonymous/public access (your app)
USING (true)              -- No restrictions on reading
WITH CHECK (true);        -- No restrictions on writing

-- Step 3: Ensure anon role has necessary permissions
GRANT ALL ON policies TO anon;

-- Step 4: Enable RLS (Run this separately after confirming the policy is created)
-- ALTER TABLE policies ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- TEST QUERIES (Run these after enabling RLS)
-- =====================================================

-- Test 1: Can you read data?
-- Expected: Should return a count
SELECT COUNT(*) as total_records FROM policies;

-- Test 2: Can you read specific records?
-- Expected: Should return data
SELECT transaction_id, customer, premium_sold 
FROM policies 
LIMIT 5;

-- Test 3: Can you search?
-- Expected: Should return matching records
SELECT COUNT(*) as matching_records 
FROM policies 
WHERE customer ILIKE '%test%';

-- If any test fails, disable RLS immediately:
-- ALTER TABLE policies DISABLE ROW LEVEL SECURITY;