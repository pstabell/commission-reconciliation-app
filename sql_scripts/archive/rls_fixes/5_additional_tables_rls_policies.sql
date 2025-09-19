-- =====================================================
-- RLS Policies for Additional Tables
-- Run this if you haven't created policies for these tables yet
-- =====================================================

-- Commission Payments Table
DROP POLICY IF EXISTS "Enable all operations for anon key" ON commission_payments;
CREATE POLICY "Enable all operations for anon key" 
ON commission_payments
FOR ALL TO anon
USING (true)
WITH CHECK (true);
GRANT ALL ON commission_payments TO anon;

-- Commission Payments Simple Table
DROP POLICY IF EXISTS "Enable all operations for anon key" ON commission_payments_simple;
CREATE POLICY "Enable all operations for anon key" 
ON commission_payments_simple
FOR ALL TO anon
USING (true)
WITH CHECK (true);
GRANT ALL ON commission_payments_simple TO anon;

-- Renewal History Table
DROP POLICY IF EXISTS "Enable all operations for anon key" ON renewal_history;
CREATE POLICY "Enable all operations for anon key" 
ON renewal_history
FOR ALL TO anon
USING (true)
WITH CHECK (true);
GRANT ALL ON renewal_history TO anon;

-- =====================================================
-- VERIFY ALL TABLES WITH RLS STATUS
-- =====================================================
SELECT 
    tablename,
    rowsecurity as "RLS Enabled",
    CASE 
        WHEN rowsecurity THEN '✅ Protected'
        ELSE '❌ Not Protected'
    END as "Status"
FROM 
    pg_tables
WHERE 
    schemaname = 'public'
    AND tablename IN (
        'policies', 
        'deleted_policies', 
        'manual_commission_entries',
        'commission_payments',
        'commission_payments_simple',
        'renewal_history'
    )
ORDER BY 
    tablename;