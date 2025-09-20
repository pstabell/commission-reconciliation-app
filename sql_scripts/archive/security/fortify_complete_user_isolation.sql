-- FORTIFY: COMPLETE USER ISOLATION FOR ALL COMMISSION DATA
-- No shared carriers, MGAs, or relationships - each user has their own

-- 1. First, backup current data before changes
CREATE TABLE IF NOT EXISTS backup_carriers_20250118 AS SELECT * FROM carriers;
CREATE TABLE IF NOT EXISTS backup_mgas_20250118 AS SELECT * FROM mgas;
CREATE TABLE IF NOT EXISTS backup_commission_rules_20250118 AS SELECT * FROM commission_rules;

-- 2. Check current structure
SELECT 'Current Table Structure:' as check;
SELECT 
    c.table_name,
    c.column_name,
    c.data_type,
    CASE WHEN c.column_name = 'user_email' THEN '✅ Has user_email' ELSE '❌ Missing user_email' END as status
FROM information_schema.columns c
WHERE c.table_schema = 'public'
  AND c.table_name IN ('carriers', 'mgas', 'carrier_mga_relationships', 'commission_rules')
  AND c.column_name IN ('user_email', 'carrier_id', 'mga_id')
ORDER BY c.table_name, c.ordinal_position;

-- 3. Add user_email to tables that don't have it
ALTER TABLE carriers 
ADD COLUMN IF NOT EXISTS user_email TEXT NOT NULL DEFAULT 'MIGRATION_NEEDED';

ALTER TABLE mgas 
ADD COLUMN IF NOT EXISTS user_email TEXT NOT NULL DEFAULT 'MIGRATION_NEEDED';

ALTER TABLE carrier_mga_relationships 
ADD COLUMN IF NOT EXISTS user_email TEXT NOT NULL DEFAULT 'MIGRATION_NEEDED';

-- 4. Update existing records to belong to specific users
-- For demo user
UPDATE carriers 
SET user_email = 'Demo@AgentCommissionTracker.com' 
WHERE user_email = 'MIGRATION_NEEDED' OR user_email IS NULL;

UPDATE mgas 
SET user_email = 'Demo@AgentCommissionTracker.com' 
WHERE user_email = 'MIGRATION_NEEDED' OR user_email IS NULL;

UPDATE carrier_mga_relationships 
SET user_email = 'Demo@AgentCommissionTracker.com' 
WHERE user_email = 'MIGRATION_NEEDED' OR user_email IS NULL;

-- 5. ENABLE RLS on all tables
ALTER TABLE carriers ENABLE ROW LEVEL SECURITY;
ALTER TABLE mgas ENABLE ROW LEVEL SECURITY;
ALTER TABLE carrier_mga_relationships ENABLE ROW LEVEL SECURITY;
ALTER TABLE commission_rules ENABLE ROW LEVEL SECURITY;

-- 6. Drop ALL existing RLS policies to start fresh
DROP POLICY IF EXISTS "Enable read access for authenticated users" ON carriers;
DROP POLICY IF EXISTS "Users can delete own carriers" ON carriers;
DROP POLICY IF EXISTS "Users can insert own carriers" ON carriers;
DROP POLICY IF EXISTS "Users can update own carriers" ON carriers;
DROP POLICY IF EXISTS "Users see global and own carriers" ON carriers;

DROP POLICY IF EXISTS "Enable read access for authenticated users" ON mgas;
DROP POLICY IF EXISTS "Users can delete own mgas" ON mgas;
DROP POLICY IF EXISTS "Users can insert own mgas" ON mgas;
DROP POLICY IF EXISTS "Users can update own mgas" ON mgas;
DROP POLICY IF EXISTS "Users see global and own mgas" ON mgas;

DROP POLICY IF EXISTS "Enable read access for authenticated users" ON carrier_mga_relationships;
DROP POLICY IF EXISTS "Only service role can modify carrier_mga_relationships" ON carrier_mga_relationships;
DROP POLICY IF EXISTS "Read only access to carrier_mga_relationships" ON carrier_mga_relationships;

-- 7. Create STRICT user isolation policies
-- Carriers - users see ONLY their own
CREATE POLICY "Users see only own carriers" ON carriers
    FOR ALL USING (user_email = current_setting('request.jwt.claims', true)::json->>'email');

-- MGAs - users see ONLY their own
CREATE POLICY "Users see only own mgas" ON mgas
    FOR ALL USING (user_email = current_setting('request.jwt.claims', true)::json->>'email');

-- Relationships - users see ONLY their own
CREATE POLICY "Users see only own relationships" ON carrier_mga_relationships
    FOR ALL USING (user_email = current_setting('request.jwt.claims', true)::json->>'email');

-- Commission rules - already has strict isolation
DROP POLICY IF EXISTS "Service role full access commission_rules" ON commission_rules;
DROP POLICY IF EXISTS "Users can delete own commission rules" ON commission_rules;
DROP POLICY IF EXISTS "Users can insert own commission rules" ON commission_rules;
DROP POLICY IF EXISTS "Users can update own commission rules" ON commission_rules;
DROP POLICY IF EXISTS "Users can view own commission rules" ON commission_rules;

CREATE POLICY "Users see only own commission rules" ON commission_rules
    FOR ALL USING (user_email = current_setting('request.jwt.claims', true)::json->>'email');

-- 8. Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_carriers_user_email ON carriers(user_email);
CREATE INDEX IF NOT EXISTS idx_mgas_user_email ON mgas(user_email);
CREATE INDEX IF NOT EXISTS idx_relationships_user_email ON carrier_mga_relationships(user_email);
CREATE INDEX IF NOT EXISTS idx_commission_rules_user_email ON commission_rules(user_email);

-- 9. Verify the fortification
SELECT 'Fortification Complete:' as status;
SELECT 
    tablename,
    COUNT(*) as policy_count,
    'STRICT USER ISOLATION' as security_level
FROM pg_policies
WHERE tablename IN ('carriers', 'mgas', 'carrier_mga_relationships', 'commission_rules')
GROUP BY tablename
ORDER BY tablename;

-- 10. Show data counts per user
SELECT 'Data per User:' as check;
SELECT 
    user_email,
    (SELECT COUNT(*) FROM carriers c WHERE c.user_email = u.user_email) as carriers,
    (SELECT COUNT(*) FROM mgas m WHERE m.user_email = u.user_email) as mgas,
    (SELECT COUNT(*) FROM commission_rules cr WHERE cr.user_email = u.user_email) as rules
FROM (SELECT DISTINCT user_email FROM carriers) u
ORDER BY user_email;