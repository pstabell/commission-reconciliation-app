-- QUICK START GUIDE - PRODUCTION-SAFE AGENCY SETUP
-- Run these scripts in order on your PROD Supabase

-- ============================================================
-- DAY 1: Basic Setup (5 minutes)
-- ============================================================

-- 1. Run the main migration (safe - only adds tables)
-- Copy and run PROD_SAFE_AGENCY_MIGRATIONS.sql in Supabase SQL editor

-- 2. Verify tables were created
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('agencies', 'agency_users');
-- Expected: 2 rows

-- 3. Verify policies table has new columns
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'policies' 
AND column_name LIKE '%agency%' OR column_name LIKE '%agent%';
-- Expected: agency_id, agent_id, created_by, updated_by

-- 4. Check that existing data is untouched
SELECT COUNT(*) as existing_policies_unchanged 
FROM policies WHERE agency_id IS NULL;
-- Should match your current policy count

-- ============================================================
-- DAY 2: Create Test Agency (For testing only)
-- ============================================================

-- 1. Create a test agency
INSERT INTO agencies (name, owner_email, subdomain) 
VALUES ('Test Agency Beta', 'test@example.com', 'test-agency-beta')
RETURNING id;
-- Save this ID!

-- 2. Create test users (replace <agency-id> with ID from above)
INSERT INTO agency_users (agency_id, email, password_hash, role, first_name, last_name, agent_code) VALUES
    ('<agency-id>', 'owner@test.com', '$2b$10$YourHashHere', 'owner', 'John', 'Owner', 'OWNER001'),
    ('<agency-id>', 'admin@test.com', '$2b$10$YourHashHere', 'admin', 'Jane', 'Admin', 'ADMIN001'),
    ('<agency-id>', 'agent1@test.com', '$2b$10$YourHashHere', 'agent', 'Bob', 'Agent', 'AGENT001'),
    ('<agency-id>', 'agent2@test.com', '$2b$10$YourHashHere', 'agent', 'Sue', 'Agent', 'AGENT002');

-- 3. Create test policies for agents (optional)
-- This helps verify multi-agent filtering works

-- ============================================================
-- DAY 3-14: Build Features (On branch)
-- ============================================================

-- While you build on the agency-platform branch:
-- 1. The database is ready with agency tables
-- 2. Your production app ignores these tables completely
-- 3. No RLS is enabled, so no security risks
-- 4. You can query and test with the test agency

-- ============================================================
-- TESTING QUERIES (Use these during development)
-- ============================================================

-- See all agencies (for debugging)
SELECT id, name, subdomain, created_at FROM agencies;

-- See users in test agency
SELECT id, email, role, agent_code FROM agency_users 
WHERE agency_id = '<your-test-agency-id>';

-- Test adding agency policy
INSERT INTO policies (
    -- your existing columns...,
    agency_id,
    agent_id,
    created_by
) VALUES (
    -- your values...,
    '<agency-id>',
    '<agent-user-id>',
    '<agent-user-id>'
);

-- Query policies by agent
SELECT * FROM policies 
WHERE agency_id = '<agency-id>' 
AND agent_id = '<agent-user-id>';

-- ============================================================
-- FEATURE FLAG QUERIES (For your app)
-- ============================================================

-- Check if user is agency user (in your app logic)
-- SELECT agency_id FROM agency_users WHERE email = $1;
-- If NULL or no rows: solo agent mode
-- If agency_id exists: agency mode

-- Get user's role and permissions
-- SELECT role, permissions FROM agency_users 
-- WHERE email = $1 AND agency_id = $2;

-- ============================================================
-- MONITORING (Run periodically)
-- ============================================================

-- Check for any issues
SELECT 
    (SELECT COUNT(*) FROM agencies) as total_agencies,
    (SELECT COUNT(*) FROM agency_users) as total_agency_users,
    (SELECT COUNT(*) FROM policies WHERE agency_id IS NOT NULL) as agency_policies,
    (SELECT COUNT(*) FROM policies WHERE agency_id IS NULL) as solo_policies;

-- ============================================================
-- EMERGENCY CLEANUP (If needed)
-- ============================================================

/*
-- Remove test data only
DELETE FROM policies WHERE agency_id = '<test-agency-id>';
DELETE FROM agency_users WHERE agency_id = '<test-agency-id>';
DELETE FROM agencies WHERE id = '<test-agency-id>';
*/

-- ============================================================
-- WHEN READY TO LAUNCH
-- ============================================================

/*
Phase 1: Soft Launch
1. Merge agency-platform branch to main
2. Deploy with AGENCY_MODE=false (features hidden)
3. Create first real agency in database
4. Set AGENCY_MODE=true for that agency only
5. Test thoroughly

Phase 2: Enable RLS (Optional - adds security)
1. Run PROD_SAFE_RLS_POLICIES.sql (creates policies)
2. Test with test agency first
3. Enable RLS table by table:
   ALTER TABLE policies ENABLE ROW LEVEL SECURITY;
   ALTER TABLE agencies ENABLE ROW LEVEL SECURITY;
   -- etc.

Phase 3: General Availability
1. Open registration for agencies
2. Migration tool for existing solo users
3. Marketing launch
*/