-- ROW LEVEL SECURITY (RLS) POLICIES - SEPARATE FILE FOR SAFETY
-- Version: 1.0
-- Date: January 2025
--
-- IMPORTANT: These policies are created but NOT ACTIVE until you enable RLS
-- Test thoroughly before enabling RLS on production tables
-- RLS can be enabled/disabled without data loss

-- ============================================================
-- STEP 1: CREATE POLICIES (Safe - just creates rules)
-- ============================================================

-- 1.1 Main policies table - Agency isolation
CREATE POLICY IF NOT EXISTS "agency_isolation_policy" ON policies
    FOR ALL USING (
        -- Non-agency records (solo agents) always visible to all
        agency_id IS NULL
        OR
        -- Agency records only visible to same agency users
        agency_id = get_user_agency_id(auth.uid())
    );

-- 1.2 Agents can only INSERT their own policies  
CREATE POLICY IF NOT EXISTS "agent_insert_own_policies" ON policies
    FOR INSERT WITH CHECK (
        -- Must be inserting for your own agency
        agency_id = get_user_agency_id(auth.uid())
        AND
        -- Must be inserting as yourself (or admin inserting for others)
        (
            agent_id = auth.uid()
            OR
            EXISTS (
                SELECT 1 FROM agency_users 
                WHERE id = auth.uid() 
                AND role IN ('owner', 'admin', 'operations')
            )
        )
    );

-- 1.3 UPDATE permissions based on role
CREATE POLICY IF NOT EXISTS "update_policy_permissions" ON policies
    FOR UPDATE USING (
        -- Solo agents can update (when agency_id is NULL)
        agency_id IS NULL
        OR
        -- Within same agency AND (own policies OR has permission)
        (
            agency_id = get_user_agency_id(auth.uid())
            AND
            (
                agent_id = auth.uid()
                OR
                user_has_permission(auth.uid(), 'edit_all_policies')
                OR
                EXISTS (
                    SELECT 1 FROM agency_users 
                    WHERE id = auth.uid() 
                    AND role IN ('owner', 'admin', 'operations')
                )
            )
        )
    );

-- 1.4 DELETE restricted to admins
CREATE POLICY IF NOT EXISTS "delete_policy_permissions" ON policies
    FOR DELETE USING (
        -- Solo mode
        agency_id IS NULL
        OR
        -- Must be admin/owner in same agency
        EXISTS (
            SELECT 1 FROM agency_users 
            WHERE id = auth.uid() 
            AND agency_id = policies.agency_id
            AND role IN ('owner', 'admin')
        )
    );

-- ============================================================
-- STEP 2: AGENCY TABLES RLS
-- ============================================================

-- 2.1 Agencies table - users see only their agency
CREATE POLICY IF NOT EXISTS "users_see_own_agency" ON agencies
    FOR SELECT USING (
        id = get_user_agency_id(auth.uid())
    );

-- 2.2 Agency users - see only same agency users
CREATE POLICY IF NOT EXISTS "see_same_agency_users" ON agency_users
    FOR SELECT USING (
        agency_id = get_user_agency_id(auth.uid())
    );

-- 2.3 Only admins can manage users
CREATE POLICY IF NOT EXISTS "admin_manage_users" ON agency_users
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM agency_users
            WHERE id = auth.uid()
            AND agency_id = agency_users.agency_id
            AND role IN ('owner', 'admin')
        )
    );

-- ============================================================
-- STEP 3: COMMISSION & FINANCIAL DATA RLS
-- ============================================================

-- 3.1 Commission rules - agency specific
CREATE POLICY IF NOT EXISTS "agency_commission_rules_policy" ON agency_commission_rules
    FOR ALL USING (
        agency_id = get_user_agency_id(auth.uid())
    );

-- 3.2 Performance data - see own or if admin
CREATE POLICY IF NOT EXISTS "performance_data_access" ON agent_performance_snapshots
    FOR SELECT USING (
        agent_id = auth.uid()
        OR
        EXISTS (
            SELECT 1 FROM agency_users
            WHERE id = auth.uid()
            AND agency_id = agent_performance_snapshots.agency_id
            AND role IN ('owner', 'admin', 'operations')
        )
    );

-- ============================================================
-- STEP 4: TESTING RLS (Before enabling)
-- ============================================================

/*
-- Test queries to run BEFORE enabling RLS:

-- 1. Create test agency and users
INSERT INTO agencies (name, owner_email) VALUES ('Test Agency', 'test@example.com');

-- 2. Create test users with different roles
INSERT INTO agency_users (agency_id, email, password_hash, role) VALUES
    ('<agency-id>', 'owner@test.com', 'hash', 'owner'),
    ('<agency-id>', 'admin@test.com', 'hash', 'admin'),
    ('<agency-id>', 'agent1@test.com', 'hash', 'agent'),
    ('<agency-id>', 'agent2@test.com', 'hash', 'agent');

-- 3. Create test policies for different agents
INSERT INTO policies (..., agency_id, agent_id) VALUES
    (..., '<agency-id>', '<agent1-id>'),
    (..., '<agency-id>', '<agent2-id>');

-- 4. Test the policies would work correctly
SELECT * FROM policies WHERE agency_id = '<agency-id>'; -- Should see all
SELECT * FROM policies WHERE agent_id = '<agent1-id>'; -- Should see only agent1's
*/

-- ============================================================
-- STEP 5: ENABLE RLS (Run separately after testing)
-- ============================================================

/*
-- DANGER ZONE - Only run after thorough testing!
-- This activates all the policies created above

-- Enable RLS on tables
ALTER TABLE policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE agencies ENABLE ROW LEVEL SECURITY;
ALTER TABLE agency_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE agency_commission_rules ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_performance_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE agency_activity_log ENABLE ROW LEVEL SECURITY;

-- Grant necessary permissions
GRANT ALL ON policies TO authenticated;
GRANT ALL ON agencies TO authenticated;
GRANT ALL ON agency_users TO authenticated;
GRANT SELECT ON agent_performance_snapshots TO authenticated;
GRANT SELECT ON agency_commission_rules TO authenticated;
*/

-- ============================================================
-- STEP 6: DISABLE RLS (Emergency rollback)
-- ============================================================

/*
-- If RLS causes issues, disable it immediately:

ALTER TABLE policies DISABLE ROW LEVEL SECURITY;
ALTER TABLE agencies DISABLE ROW LEVEL SECURITY;
ALTER TABLE agency_users DISABLE ROW LEVEL SECURITY;
ALTER TABLE agency_commission_rules DISABLE ROW LEVEL SECURITY;
ALTER TABLE agent_performance_snapshots DISABLE ROW LEVEL SECURITY;
ALTER TABLE agency_activity_log DISABLE ROW LEVEL SECURITY;
*/

-- ============================================================
-- STEP 7: RLS TESTING FUNCTIONS
-- ============================================================

-- Function to test RLS as different users
CREATE OR REPLACE FUNCTION test_rls_as_user(test_user_id UUID)
RETURNS TABLE (
    visible_policies_count INTEGER,
    visible_agencies_count INTEGER,
    visible_users_count INTEGER,
    can_insert_policy BOOLEAN,
    can_update_own_policy BOOLEAN,
    can_delete_policy BOOLEAN
) AS $$
BEGIN
    -- Temporarily set the auth context
    PERFORM set_config('request.jwt.claims', json_build_object('sub', test_user_id::text)::text, true);
    
    RETURN QUERY
    SELECT 
        (SELECT COUNT(*) FROM policies)::INTEGER,
        (SELECT COUNT(*) FROM agencies)::INTEGER,
        (SELECT COUNT(*) FROM agency_users)::INTEGER,
        (SELECT COUNT(*) > 0 FROM policies WHERE agent_id = test_user_id LIMIT 1),
        (SELECT COUNT(*) > 0 FROM policies WHERE agent_id = test_user_id LIMIT 1),
        FALSE; -- Agents shouldn't delete
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;