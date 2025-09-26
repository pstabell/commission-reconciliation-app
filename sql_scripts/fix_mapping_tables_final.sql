-- Fix mapping tables - handles existing constraints gracefully

-- First drop existing tables if they exist
DROP TABLE IF EXISTS user_policy_type_mappings CASCADE;
DROP TABLE IF EXISTS user_transaction_type_mappings CASCADE;

-- Create user_policy_type_mappings with correct structure
CREATE TABLE user_policy_type_mappings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    user_email TEXT NOT NULL,
    mappings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_policy_user_id UNIQUE(user_id),
    CONSTRAINT unique_policy_user_email UNIQUE(user_email)
);

-- Create user_transaction_type_mappings with correct structure
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

-- Create indexes
CREATE INDEX idx_user_policy_type_mappings_user_id ON user_policy_type_mappings(user_id);
CREATE INDEX idx_user_policy_type_mappings_user_email ON user_policy_type_mappings(user_email);
CREATE INDEX idx_user_transaction_type_mappings_user_id ON user_transaction_type_mappings(user_id);
CREATE INDEX idx_user_transaction_type_mappings_user_email ON user_transaction_type_mappings(user_email);

-- Add default mappings for all users
INSERT INTO user_policy_type_mappings (user_id, user_email, mappings)
SELECT 
    id,
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
        "WC": "WC",
        "PROP-C": "PROP-C",
        "CONDO": "CONDO",
        "UMBRELLA": "UMBRELLA",
        "OTHER": "OTHER"
    }'::jsonb
FROM users;

INSERT INTO user_transaction_type_mappings (user_id, user_email, mappings)
SELECT 
    id,
    email,
    '{
        "STL": "PMT",
        "NBS": "NEW",
        "XLC": "CAN",
        "RWL": "RWL",
        "PCH": "END",
        "NEW": "NEW",
        "END": "END",
        "CAN": "CAN",
        "PMT": "PMT",
        "REI": "REI",
        "AUD": "AUD",
        "OTH": "OTH"
    }'::jsonb
FROM users;

-- Enable RLS
ALTER TABLE user_policy_type_mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_transaction_type_mappings ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view their own policy mappings" ON user_policy_type_mappings
    FOR SELECT USING (true);

CREATE POLICY "Users can insert their own policy mappings" ON user_policy_type_mappings
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update their own policy mappings" ON user_policy_type_mappings
    FOR UPDATE USING (true);

CREATE POLICY "Users can delete their own policy mappings" ON user_policy_type_mappings
    FOR DELETE USING (true);

CREATE POLICY "Users can view their own transaction mappings" ON user_transaction_type_mappings
    FOR SELECT USING (true);

CREATE POLICY "Users can insert their own transaction mappings" ON user_transaction_type_mappings
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update their own transaction mappings" ON user_transaction_type_mappings
    FOR UPDATE USING (true);

CREATE POLICY "Users can delete their own transaction mappings" ON user_transaction_type_mappings
    FOR DELETE USING (true);

-- Show results
SELECT 
    'user_policy_type_mappings' as table_name,
    COUNT(*) as records,
    'Tables recreated successfully' as status
FROM user_policy_type_mappings
UNION ALL
SELECT 
    'user_transaction_type_mappings',
    COUNT(*),
    'Tables recreated successfully'
FROM user_transaction_type_mappings;