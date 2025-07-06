-- RLS (Row Level Security) Policies for Sales Commission App
-- Run these scripts BEFORE enabling RLS on each table
-- These policies allow the anon key to perform all operations

-- =====================================================
-- 1. POLICIES TABLE
-- =====================================================

-- Drop existing policies if any
DROP POLICY IF EXISTS "Enable all operations for anon key" ON policies;

-- Create policy that allows all operations for authenticated requests
CREATE POLICY "Enable all operations for anon key" 
ON policies
FOR ALL 
TO anon
USING (true)
WITH CHECK (true);

-- Grant necessary permissions
GRANT ALL ON policies TO anon;

-- To enable RLS after running this:
-- ALTER TABLE policies ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- 2. DELETED_POLICIES TABLE
-- =====================================================

-- Drop existing policies if any
DROP POLICY IF EXISTS "Enable all operations for anon key" ON deleted_policies;

-- Create policy that allows all operations for authenticated requests
CREATE POLICY "Enable all operations for anon key" 
ON deleted_policies
FOR ALL 
TO anon
USING (true)
WITH CHECK (true);

-- Grant necessary permissions
GRANT ALL ON deleted_policies TO anon;

-- To enable RLS after running this:
-- ALTER TABLE deleted_policies ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- 3. MANUAL_COMMISSION_ENTRIES TABLE
-- =====================================================

-- Drop existing policies if any
DROP POLICY IF EXISTS "Enable all operations for anon key" ON manual_commission_entries;

-- Create policy that allows all operations for authenticated requests
CREATE POLICY "Enable all operations for anon key" 
ON manual_commission_entries
FOR ALL 
TO anon
USING (true)
WITH CHECK (true);

-- Grant necessary permissions
GRANT ALL ON manual_commission_entries TO anon;

-- To enable RLS after running this:
-- ALTER TABLE manual_commission_entries ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================
-- After enabling RLS, run these to verify access:

-- Test SELECT
-- SELECT COUNT(*) FROM policies;
-- SELECT COUNT(*) FROM deleted_policies;
-- SELECT COUNT(*) FROM manual_commission_entries;

-- Test INSERT (careful - this will add a test record)
-- INSERT INTO policies (transaction_id, customer) VALUES ('TEST123', 'Test Customer');
-- DELETE FROM policies WHERE transaction_id = 'TEST123';

-- =====================================================
-- TO ENABLE RLS ON ALL TABLES AT ONCE
-- =====================================================
-- After running all the policies above, you can enable RLS:
/*
ALTER TABLE policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE deleted_policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE manual_commission_entries ENABLE ROW LEVEL SECURITY;
*/

-- =====================================================
-- TO DISABLE RLS (IF NEEDED)
-- =====================================================
/*
ALTER TABLE policies DISABLE ROW LEVEL SECURITY;
ALTER TABLE deleted_policies DISABLE ROW LEVEL SECURITY;
ALTER TABLE manual_commission_entries DISABLE ROW LEVEL SECURITY;
*/