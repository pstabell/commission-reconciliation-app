-- Create tables for user-specific settings
-- This replaces global JSON files with per-user database storage

-- 1. User Column Mappings (replaces column_mapping.json)
CREATE TABLE IF NOT EXISTS user_column_mappings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) NOT NULL,
    user_email TEXT NOT NULL,
    column_mappings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- 2. User Preferences (replaces user_preferences.json) 
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) NOT NULL,
    user_email TEXT NOT NULL,
    color_theme TEXT DEFAULT 'light',
    other_preferences JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- 3. User Default Agent Rates (replaces default_agent_commission_rates.json)
CREATE TABLE IF NOT EXISTS user_default_agent_rates (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) NOT NULL,
    user_email TEXT NOT NULL,
    new_business_rate DECIMAL(5,2) DEFAULT 50.00,
    renewal_rate DECIMAL(5,2) DEFAULT 25.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- 4. User Policy Types (replaces policy_types_updated.json)
CREATE TABLE IF NOT EXISTS user_policy_types (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    user_email TEXT NOT NULL,
    policy_types JSONB NOT NULL DEFAULT '[]'::jsonb,
    default_type TEXT DEFAULT 'HO3',
    categories JSONB DEFAULT '["Personal Property", "Personal Auto", "Commercial", "Specialty", "Personal", "Other"]'::jsonb,
    version TEXT DEFAULT '1.0.0',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_id UNIQUE(user_id),
    CONSTRAINT unique_user_email UNIQUE(user_email)
);

-- 5. User Transaction Types (replaces transaction_types.json)
CREATE TABLE IF NOT EXISTS user_transaction_types (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) NOT NULL,
    user_email TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    category TEXT,
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, transaction_type)
);

-- 6. User Policy Type Mappings (replaces policy_type_mappings.json)
CREATE TABLE IF NOT EXISTS user_policy_type_mappings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) NOT NULL,
    user_email TEXT NOT NULL,
    statement_value TEXT NOT NULL,
    mapped_type TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, statement_value)
);

-- 7. User Transaction Type Mappings (replaces transaction_type_mappings.json)
CREATE TABLE IF NOT EXISTS user_transaction_type_mappings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) NOT NULL,
    user_email TEXT NOT NULL,
    statement_code TEXT NOT NULL,
    mapped_type TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, statement_code)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_column_mappings_user_id ON user_column_mappings(user_id);
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_user_default_agent_rates_user_id ON user_default_agent_rates(user_id);
CREATE INDEX IF NOT EXISTS idx_user_policy_types_user_id ON user_policy_types(user_id);
CREATE INDEX IF NOT EXISTS idx_user_transaction_types_user_id ON user_transaction_types(user_id);
CREATE INDEX IF NOT EXISTS idx_user_policy_type_mappings_user_id ON user_policy_type_mappings(user_id);
CREATE INDEX IF NOT EXISTS idx_user_transaction_type_mappings_user_id ON user_transaction_type_mappings(user_id);

-- Grant permissions (if using RLS)
-- ALTER TABLE user_column_mappings ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE user_default_agent_rates ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE user_policy_types ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE user_transaction_types ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE user_policy_type_mappings ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE user_transaction_type_mappings ENABLE ROW LEVEL SECURITY;