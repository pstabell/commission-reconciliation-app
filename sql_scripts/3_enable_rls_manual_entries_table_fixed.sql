-- =====================================================
-- RLS Setup for MANUAL_COMMISSION_ENTRIES Table (with correct column names)
-- Run this BEFORE enabling RLS on the manual_commission_entries table
-- =====================================================

-- Step 1: Drop any existing policies to start fresh
DROP POLICY IF EXISTS "Enable all operations for anon key" ON manual_commission_entries;

-- Step 2: Create a permissive policy for the anon role
-- This allows your app (using anon key) to perform all operations
CREATE POLICY "Enable all operations for anon key" 
ON manual_commission_entries
FOR ALL                    -- Covers SELECT, INSERT, UPDATE, DELETE
TO anon                    -- Applies to anonymous/public access (your app)
USING (true)              -- No restrictions on reading
WITH CHECK (true);        -- No restrictions on writing

-- Step 3: Ensure anon role has necessary permissions
GRANT ALL ON manual_commission_entries TO anon;

-- Step 4: Enable RLS (Run this separately after confirming the policy is created)
-- ALTER TABLE manual_commission_entries ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- TEST QUERIES (Run these after enabling RLS)
-- =====================================================

-- Test 1: Can you read manual entries?
-- Expected: Should return a count (might be 0 if no manual entries yet)
SELECT COUNT(*) as total_manual_entries FROM manual_commission_entries;

-- Test 2: Can you read specific manual entries?
-- Expected: Should return data if any records exist
SELECT id, customer, commission_paid, agency_commission_received 
FROM manual_commission_entries 
LIMIT 5;

-- Test 3: Can you insert a test manual entry?
-- Expected: Should successfully insert
-- INSERT INTO manual_commission_entries (customer, policy_type, commission_paid, effective_date, transaction_type) 
-- VALUES ('Test Client', 'Auto', 100.00, '2024-01-01', 'NEW');

-- Test 4: Can you delete the test entry?
-- Expected: Should successfully delete
-- DELETE FROM manual_commission_entries 
-- WHERE customer = 'Test Client' AND commission_paid = 100.00;

-- If any test fails, disable RLS immediately:
-- ALTER TABLE manual_commission_entries DISABLE ROW LEVEL SECURITY;