-- Create or fix user_policy_type_mappings and user_transaction_type_mappings tables
-- This script safely handles both new creation and migration scenarios

-- First, check if tables exist and have data
DO $$
BEGIN
    -- Handle user_policy_type_mappings
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'user_policy_type_mappings') THEN
        -- Check if it has the old structure (individual columns)
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'user_policy_type_mappings' 
                   AND column_name = 'statement_value') THEN
            -- Old structure exists, migrate it
            CREATE TEMP TABLE temp_policy_mappings AS
            SELECT user_id, user_email, statement_value, mapped_type
            FROM user_policy_type_mappings;
            
            DROP TABLE user_policy_type_mappings;
        END IF;
    END IF;
    
    -- Handle user_transaction_type_mappings
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'user_transaction_type_mappings') THEN
        -- Check if it has the old structure (individual columns)
        IF EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'user_transaction_type_mappings' 
                   AND column_name = 'statement_code') THEN
            -- Old structure exists, migrate it
            CREATE TEMP TABLE temp_transaction_mappings AS
            SELECT user_id, user_email, statement_code, mapped_type
            FROM user_transaction_type_mappings;
            
            DROP TABLE user_transaction_type_mappings;
        END IF;
    END IF;
END $$;

-- Create user_policy_type_mappings with correct structure
CREATE TABLE IF NOT EXISTS user_policy_type_mappings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    user_email TEXT NOT NULL,
    mappings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_id UNIQUE(user_id),
    CONSTRAINT unique_user_email UNIQUE(user_email)
);

-- Create user_transaction_type_mappings with correct structure
CREATE TABLE IF NOT EXISTS user_transaction_type_mappings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    user_email TEXT NOT NULL,
    mappings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_tx_user_id UNIQUE(user_id),
    CONSTRAINT unique_tx_user_email UNIQUE(user_email)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_user_policy_type_mappings_user_id ON user_policy_type_mappings(user_id);
CREATE INDEX IF NOT EXISTS idx_user_policy_type_mappings_user_email ON user_policy_type_mappings(user_email);
CREATE INDEX IF NOT EXISTS idx_user_transaction_type_mappings_user_id ON user_transaction_type_mappings(user_id);
CREATE INDEX IF NOT EXISTS idx_user_transaction_type_mappings_user_email ON user_transaction_type_mappings(user_email);

-- Migrate data if temp tables exist
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'temp_policy_mappings') THEN
        INSERT INTO user_policy_type_mappings (user_id, user_email, mappings)
        SELECT 
            user_id,
            user_email,
            jsonb_object_agg(statement_value, mapped_type) as mappings
        FROM temp_policy_mappings
        GROUP BY user_id, user_email
        ON CONFLICT (user_id) DO UPDATE
        SET mappings = EXCLUDED.mappings,
            updated_at = NOW();
        
        DROP TABLE temp_policy_mappings;
    END IF;
    
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'temp_transaction_mappings') THEN
        INSERT INTO user_transaction_type_mappings (user_id, user_email, mappings)
        SELECT 
            user_id,
            user_email,
            jsonb_object_agg(statement_code, mapped_type) as mappings
        FROM temp_transaction_mappings
        GROUP BY user_id, user_email
        ON CONFLICT (user_id) DO UPDATE
        SET mappings = EXCLUDED.mappings,
            updated_at = NOW();
        
        DROP TABLE temp_transaction_mappings;
    END IF;
END $$;

-- Add default mappings for users without any mappings
INSERT INTO user_policy_type_mappings (user_email, mappings)
SELECT DISTINCT 
    email,
    '{
        "HO3": "HOME",
        "HOME": "HOME",
        "PAWN": "PROP-C",
        "AUTOP": "AUTOP",
        "AUTOB": "AUTOB",
        "PL": "PL",
        "DFIRE": "DFIRE",
        "WORK": "WC",
        "CONDP": "CONDO",
        "FLODC": "FLOOD",
        "FLOOD": "FLOOD",
        "BOAT": "BOAT",
        "GL": "GL",
        "WC": "WC"
    }'::jsonb
FROM users
WHERE email NOT IN (SELECT user_email FROM user_policy_type_mappings)
ON CONFLICT (user_email) DO NOTHING;

INSERT INTO user_transaction_type_mappings (user_email, mappings)
SELECT DISTINCT 
    email,
    '{
        "STL": "PMT",
        "NBS": "NEW",
        "XLC": "CAN",
        "RWL": "RWL",
        "PCH": "END"
    }'::jsonb
FROM users
WHERE email NOT IN (SELECT user_email FROM user_transaction_type_mappings)
ON CONFLICT (user_email) DO NOTHING;

-- Show results
SELECT 
    'user_policy_type_mappings' as table_name,
    COUNT(*) as records,
    'Tables created/fixed successfully' as status
FROM user_policy_type_mappings
UNION ALL
SELECT 
    'user_transaction_type_mappings',
    COUNT(*),
    'Tables created/fixed successfully'
FROM user_transaction_type_mappings;