-- Commission Intelligence Platform - Database Migrations
-- Safe to run on production Supabase instance
-- All changes are additive only

-- ============================================================
-- API Keys Table
-- ============================================================
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_email VARCHAR(255) NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    permissions JSONB DEFAULT '{}',
    rate_limit INTEGER DEFAULT 1000,
    calls_made INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_api_keys_user_email ON api_keys(user_email);
CREATE INDEX IF NOT EXISTS idx_api_keys_api_key ON api_keys(api_key);
CREATE INDEX IF NOT EXISTS idx_api_keys_is_active ON api_keys(is_active);

-- ============================================================
-- Webhook Endpoints Table
-- ============================================================
CREATE TABLE IF NOT EXISTS webhook_endpoints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_email VARCHAR(255) NOT NULL,
    url VARCHAR(500) NOT NULL,
    events TEXT[] NOT NULL,
    secret VARCHAR(255),
    retry_policy VARCHAR(50) DEFAULT 'standard',
    is_active BOOLEAN DEFAULT true,
    last_triggered TIMESTAMP,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_webhook_endpoints_user_email ON webhook_endpoints(user_email);
CREATE INDEX IF NOT EXISTS idx_webhook_endpoints_is_active ON webhook_endpoints(is_active);

-- ============================================================
-- API Request Logs Table (for analytics)
-- ============================================================
CREATE TABLE IF NOT EXISTS api_request_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_key_id UUID REFERENCES api_keys(id),
    user_email VARCHAR(255),
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER,
    response_time_ms INTEGER,
    request_body JSONB,
    response_body JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for analytics
CREATE INDEX IF NOT EXISTS idx_api_request_logs_api_key_id ON api_request_logs(api_key_id);
CREATE INDEX IF NOT EXISTS idx_api_request_logs_created_at ON api_request_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_api_request_logs_endpoint ON api_request_logs(endpoint);

-- ============================================================
-- Webhook Event Logs Table
-- ============================================================
CREATE TABLE IF NOT EXISTS webhook_event_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    webhook_id UUID REFERENCES webhook_endpoints(id),
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(50) NOT NULL, -- 'pending', 'delivered', 'failed'
    attempts INTEGER DEFAULT 0,
    last_attempt TIMESTAMP,
    next_retry TIMESTAMP,
    response_code INTEGER,
    response_body TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_webhook_event_logs_webhook_id ON webhook_event_logs(webhook_id);
CREATE INDEX IF NOT EXISTS idx_webhook_event_logs_status ON webhook_event_logs(status);
CREATE INDEX IF NOT EXISTS idx_webhook_event_logs_created_at ON webhook_event_logs(created_at);

-- ============================================================
-- API Integration Mappings Table
-- ============================================================
CREATE TABLE IF NOT EXISTS api_integration_mappings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_email VARCHAR(255) NOT NULL,
    integration_type VARCHAR(100) NOT NULL, -- 'ezlynx', 'applied_epic', 'hubspot', etc
    field_mappings JSONB NOT NULL,
    config JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- Add API tracking columns to existing policies table
-- ============================================================
ALTER TABLE policies ADD COLUMN IF NOT EXISTS api_source VARCHAR(50);
ALTER TABLE policies ADD COLUMN IF NOT EXISTS last_api_sync TIMESTAMP;
ALTER TABLE policies ADD COLUMN IF NOT EXISTS external_id VARCHAR(255);
ALTER TABLE policies ADD COLUMN IF NOT EXISTS integration_metadata JSONB;

-- Indexes for API queries
CREATE INDEX IF NOT EXISTS idx_policies_api_source ON policies(api_source);
CREATE INDEX IF NOT EXISTS idx_policies_external_id ON policies(external_id);

-- ============================================================
-- Functions for API operations
-- ============================================================

-- Function to generate secure API key
CREATE OR REPLACE FUNCTION generate_api_key() RETURNS VARCHAR AS $$
DECLARE
    new_key VARCHAR;
BEGIN
    -- Generate a secure random key with prefix
    new_key := 'ck_' || encode(gen_random_bytes(32), 'hex');
    RETURN new_key;
END;
$$ LANGUAGE plpgsql;

-- Function to verify webhook signature
CREATE OR REPLACE FUNCTION verify_webhook_signature(
    payload TEXT,
    signature TEXT,
    secret TEXT
) RETURNS BOOLEAN AS $$
DECLARE
    computed_signature TEXT;
BEGIN
    -- Compute HMAC-SHA256 signature
    computed_signature := encode(
        crypto.hmac(payload::bytea, secret::bytea, 'sha256'::text),
        'hex'
    );
    RETURN computed_signature = signature;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- Row Level Security Policies
-- ============================================================

-- API Keys RLS
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own API keys" ON api_keys
    FOR SELECT USING (user_email = current_setting('app.user_email', true));

CREATE POLICY "Users can create own API keys" ON api_keys
    FOR INSERT WITH CHECK (user_email = current_setting('app.user_email', true));

CREATE POLICY "Users can update own API keys" ON api_keys
    FOR UPDATE USING (user_email = current_setting('app.user_email', true));

CREATE POLICY "Users can delete own API keys" ON api_keys
    FOR DELETE USING (user_email = current_setting('app.user_email', true));

-- Webhooks RLS
ALTER TABLE webhook_endpoints ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own webhooks" ON webhook_endpoints
    FOR ALL USING (user_email = current_setting('app.user_email', true));

-- ============================================================
-- Sample Data for Testing (Optional)
-- ============================================================

/*
-- Create a test API key
INSERT INTO api_keys (user_email, api_key, name, permissions, rate_limit)
VALUES (
    'demo@example.com',
    generate_api_key(),
    'Development API Key',
    '{"policies": ["read", "write"], "commissions": ["read"]}'::jsonb,
    1000
);

-- Create a test webhook
INSERT INTO webhook_endpoints (user_email, url, events, secret)
VALUES (
    'demo@example.com',
    'https://example.com/webhook',
    ARRAY['policy.created', 'commission.calculated'],
    encode(gen_random_bytes(32), 'hex')
);
*/

-- ============================================================
-- Rollback Script (Save separately)
-- ============================================================

/*
-- To rollback all API platform changes:
DROP TABLE IF EXISTS webhook_event_logs CASCADE;
DROP TABLE IF EXISTS api_request_logs CASCADE;
DROP TABLE IF EXISTS webhook_endpoints CASCADE;
DROP TABLE IF EXISTS api_keys CASCADE;
DROP TABLE IF EXISTS api_integration_mappings CASCADE;

ALTER TABLE policies DROP COLUMN IF EXISTS api_source;
ALTER TABLE policies DROP COLUMN IF EXISTS last_api_sync;
ALTER TABLE policies DROP COLUMN IF EXISTS external_id;
ALTER TABLE policies DROP COLUMN IF EXISTS integration_metadata;

DROP FUNCTION IF EXISTS generate_api_key();
DROP FUNCTION IF EXISTS verify_webhook_signature(TEXT, TEXT, TEXT);
*/