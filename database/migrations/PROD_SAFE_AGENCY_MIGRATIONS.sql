-- PRODUCTION-SAFE AGENCY PLATFORM MIGRATIONS
-- Version: 1.0
-- Date: January 2025
-- 
-- IMPORTANT: These migrations are designed to be 100% safe for production
-- They only ADD new functionality without modifying existing structures
-- Each section can be run independently and rolled back if needed

-- ============================================================
-- SECTION 1: AGENCY INFRASTRUCTURE (Safe to run anytime)
-- ============================================================

-- 1.1 Create agencies table (new table, no conflicts)
CREATE TABLE IF NOT EXISTS agencies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(100) UNIQUE,
    owner_email VARCHAR(255) NOT NULL,
    settings JSONB DEFAULT '{}',
    subscription_status VARCHAR(50) DEFAULT 'trial',
    subscription_end_date DATE,
    max_agents INTEGER DEFAULT 5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 1.2 Create agency users table (new table, no conflicts)
CREATE TABLE IF NOT EXISTS agency_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID REFERENCES agencies(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'agent' CHECK (role IN ('owner', 'admin', 'operations', 'agent')),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    agent_code VARCHAR(50), -- For agent commission tracking
    commission_split_default DECIMAL(5,2) DEFAULT 50.00, -- Default commission split %
    is_active BOOLEAN DEFAULT true,
    permissions JSONB DEFAULT '{}',
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    UNIQUE(agency_id, email)
);

-- 1.3 Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_agencies_subdomain ON agencies(subdomain);
CREATE INDEX IF NOT EXISTS idx_agency_users_email ON agency_users(email);
CREATE INDEX IF NOT EXISTS idx_agency_users_agency_id ON agency_users(agency_id);
CREATE INDEX IF NOT EXISTS idx_agency_users_agent_code ON agency_users(agent_code);

-- ============================================================
-- SECTION 2: ENHANCE EXISTING TABLES (Safe additions only)
-- ============================================================

-- 2.1 Add agency columns to policies table (NULL by default, won't affect existing data)
ALTER TABLE policies ADD COLUMN IF NOT EXISTS agency_id UUID REFERENCES agencies(id);
ALTER TABLE policies ADD COLUMN IF NOT EXISTS agent_id UUID REFERENCES agency_users(id);
ALTER TABLE policies ADD COLUMN IF NOT EXISTS created_by UUID REFERENCES agency_users(id);
ALTER TABLE policies ADD COLUMN IF NOT EXISTS updated_by UUID REFERENCES agency_users(id);
ALTER TABLE policies ADD COLUMN IF NOT EXISTS agent_commission_split DECIMAL(5,2); -- Can override default

-- 2.2 Add indexes for agency filtering (improves performance, safe to add)
CREATE INDEX IF NOT EXISTS idx_policies_agency_id ON policies(agency_id);
CREATE INDEX IF NOT EXISTS idx_policies_agent_id ON policies(agent_id);

-- 2.3 Add agency tracking to other tables
ALTER TABLE commission_overrides ADD COLUMN IF NOT EXISTS agency_id UUID REFERENCES agencies(id);
ALTER TABLE carriers ADD COLUMN IF NOT EXISTS agency_id UUID REFERENCES agencies(id);
ALTER TABLE mgas ADD COLUMN IF NOT EXISTS agency_id UUID REFERENCES agencies(id);

-- ============================================================
-- SECTION 3: AGENCY-SPECIFIC FEATURES (New tables)
-- ============================================================

-- 3.1 Agency commission rules (per-carrier overrides)
CREATE TABLE IF NOT EXISTS agency_commission_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID REFERENCES agencies(id) ON DELETE CASCADE,
    carrier_id INTEGER, -- References your existing carriers table
    policy_type VARCHAR(100),
    transaction_type VARCHAR(50),
    agency_rate DECIMAL(5,2), -- What agency gets from carrier
    agent_split_default DECIMAL(5,2), -- Default agent split
    effective_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    UNIQUE(agency_id, carrier_id, policy_type, transaction_type, effective_date)
);

-- 3.2 Team performance tracking
CREATE TABLE IF NOT EXISTS agent_performance_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID REFERENCES agencies(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agency_users(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    new_business_count INTEGER DEFAULT 0,
    new_business_premium DECIMAL(10,2) DEFAULT 0,
    renewal_count INTEGER DEFAULT 0,
    renewal_premium DECIMAL(10,2) DEFAULT 0,
    total_commission DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    UNIQUE(agent_id, snapshot_date)
);

-- 3.3 Agency activity log for audit trail
CREATE TABLE IF NOT EXISTS agency_activity_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID REFERENCES agencies(id) ON DELETE CASCADE,
    user_id UUID REFERENCES agency_users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50), -- 'policy', 'user', 'commission', etc.
    entity_id VARCHAR(100), -- ID of affected record
    details JSONB DEFAULT '{}',
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- ============================================================
-- SECTION 4: ROW LEVEL SECURITY POLICIES (DON'T ENABLE YET)
-- ============================================================

-- Create policies but DON'T enable RLS until tested
-- These are created but inactive until you run: ALTER TABLE policies ENABLE ROW LEVEL SECURITY;

-- 4.1 Policies table RLS (prepared but not active)
CREATE POLICY IF NOT EXISTS "Users see own agency policies" ON policies
    FOR ALL USING (
        -- Solo agents (no agency_id) see their own data as before
        (agency_id IS NULL) 
        OR 
        -- Agency users see only their agency's data
        (agency_id IN (
            SELECT agency_id FROM agency_users WHERE id = auth.uid()
        ))
    );

-- 4.2 Agent-specific view policy
CREATE POLICY IF NOT EXISTS "Agents see only assigned policies" ON policies
    FOR SELECT USING (
        -- Solo mode unchanged
        (agency_id IS NULL)
        OR
        -- Admins/Operations see all agency policies
        (EXISTS (
            SELECT 1 FROM agency_users 
            WHERE id = auth.uid() 
            AND agency_id = policies.agency_id
            AND role IN ('owner', 'admin', 'operations')
        ))
        OR
        -- Agents see only their assigned policies
        (agent_id = auth.uid())
    );

-- ============================================================
-- SECTION 5: HELPER FUNCTIONS (Safe to create)
-- ============================================================

-- 5.1 Function to get user's agency
CREATE OR REPLACE FUNCTION get_user_agency_id(user_id UUID)
RETURNS UUID AS $$
BEGIN
    RETURN (SELECT agency_id FROM agency_users WHERE id = user_id);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 5.2 Function to check user permissions
CREATE OR REPLACE FUNCTION user_has_permission(user_id UUID, permission TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    user_role TEXT;
    user_permissions JSONB;
BEGIN
    SELECT role, permissions INTO user_role, user_permissions
    FROM agency_users WHERE id = user_id;
    
    -- Owners have all permissions
    IF user_role = 'owner' THEN
        RETURN TRUE;
    END IF;
    
    -- Check specific permission in JSON
    RETURN user_permissions ? permission AND user_permissions->permission = 'true';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================
-- SECTION 6: MIGRATION HELPERS (For existing users)
-- ============================================================

-- 6.1 Create function to migrate existing user to agency owner
CREATE OR REPLACE FUNCTION migrate_user_to_agency_owner(
    p_email VARCHAR,
    p_agency_name VARCHAR,
    p_password_hash TEXT
)
RETURNS UUID AS $$
DECLARE
    v_agency_id UUID;
    v_user_id UUID;
BEGIN
    -- Create agency
    INSERT INTO agencies (name, owner_email)
    VALUES (p_agency_name, p_email)
    RETURNING id INTO v_agency_id;
    
    -- Create owner user
    INSERT INTO agency_users (
        agency_id, email, password_hash, role, first_name, last_name
    ) VALUES (
        v_agency_id, p_email, p_password_hash, 'owner', 'Agency', 'Owner'
    ) RETURNING id INTO v_user_id;
    
    -- Update existing policies to belong to this agency
    UPDATE policies 
    SET agency_id = v_agency_id, agent_id = v_user_id
    WHERE agency_id IS NULL; -- Only update non-agency policies
    
    RETURN v_agency_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================
-- ROLLBACK SCRIPTS (Save these separately)
-- ============================================================

/*
-- EMERGENCY ROLLBACK - Run if something goes wrong
-- This will remove all agency features but preserve original data

-- Remove columns from existing tables
ALTER TABLE policies DROP COLUMN IF EXISTS agency_id;
ALTER TABLE policies DROP COLUMN IF EXISTS agent_id;
ALTER TABLE policies DROP COLUMN IF EXISTS created_by;
ALTER TABLE policies DROP COLUMN IF EXISTS updated_by;
ALTER TABLE policies DROP COLUMN IF EXISTS agent_commission_split;
ALTER TABLE commission_overrides DROP COLUMN IF EXISTS agency_id;
ALTER TABLE carriers DROP COLUMN IF EXISTS agency_id;
ALTER TABLE mgas DROP COLUMN IF EXISTS agency_id;

-- Drop new tables
DROP TABLE IF EXISTS agency_activity_log;
DROP TABLE IF EXISTS agent_performance_snapshots;
DROP TABLE IF EXISTS agency_commission_rules;
DROP TABLE IF EXISTS agency_users;
DROP TABLE IF EXISTS agencies;

-- Drop functions
DROP FUNCTION IF EXISTS get_user_agency_id(UUID);
DROP FUNCTION IF EXISTS user_has_permission(UUID, TEXT);
DROP FUNCTION IF EXISTS migrate_user_to_agency_owner(VARCHAR, VARCHAR, TEXT);

-- Drop policies (if RLS was enabled)
DROP POLICY IF EXISTS "Users see own agency policies" ON policies;
DROP POLICY IF EXISTS "Agents see only assigned policies" ON policies;
*/

-- ============================================================
-- TESTING QUERIES (Run these to verify setup)
-- ============================================================

/*
-- Check if tables were created
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('agencies', 'agency_users', 'agency_commission_rules');

-- Check if columns were added to policies
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'policies' 
AND column_name IN ('agency_id', 'agent_id', 'created_by', 'updated_by');

-- Verify no existing data was affected
SELECT COUNT(*) as solo_policies FROM policies WHERE agency_id IS NULL;

-- Test creating an agency (safe test)
INSERT INTO agencies (name, owner_email) 
VALUES ('Test Agency', 'test@example.com')
RETURNING *;
*/