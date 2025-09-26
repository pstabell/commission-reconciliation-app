-- Fix user_policy_type_mappings table structure to use JSONB instead of individual columns
-- This matches what the Python code expects

-- Step 1: Create backup of existing data
CREATE TEMP TABLE temp_policy_mappings AS
SELECT user_id, user_email, statement_value, mapped_type
FROM user_policy_type_mappings;

-- Step 2: Drop the existing table
DROP TABLE IF EXISTS user_policy_type_mappings;

-- Step 3: Recreate table with JSONB structure
CREATE TABLE user_policy_type_mappings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    user_email TEXT NOT NULL,
    mappings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_id UNIQUE(user_id),
    CONSTRAINT unique_user_email UNIQUE(user_email)
);

-- Step 4: Create indexes
CREATE INDEX IF NOT EXISTS idx_user_policy_type_mappings_user_id ON user_policy_type_mappings(user_id);
CREATE INDEX IF NOT EXISTS idx_user_policy_type_mappings_user_email ON user_policy_type_mappings(user_email);

-- Step 5: Migrate data from backup, converting to JSONB format
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

-- Step 6: Also do the same for user_transaction_type_mappings
CREATE TEMP TABLE temp_transaction_mappings AS
SELECT user_id, user_email, statement_code, mapped_type
FROM user_transaction_type_mappings;

DROP TABLE IF EXISTS user_transaction_type_mappings;

CREATE TABLE user_transaction_type_mappings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    user_email TEXT NOT NULL,
    mappings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_tx_user_id UNIQUE(user_id),
    CONSTRAINT unique_tx_user_email UNIQUE(user_email)
);

CREATE INDEX IF NOT EXISTS idx_user_transaction_type_mappings_user_id ON user_transaction_type_mappings(user_id);
CREATE INDEX IF NOT EXISTS idx_user_transaction_type_mappings_user_email ON user_transaction_type_mappings(user_email);

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

-- Clean up temp tables
DROP TABLE temp_policy_mappings;
DROP TABLE temp_transaction_mappings;

-- Show results
SELECT 
    'user_policy_type_mappings' as table_name,
    COUNT(*) as records,
    'Fixed structure to use JSONB' as status
FROM user_policy_type_mappings
UNION ALL
SELECT 
    'user_transaction_type_mappings',
    COUNT(*),
    'Fixed structure to use JSONB'
FROM user_transaction_type_mappings;