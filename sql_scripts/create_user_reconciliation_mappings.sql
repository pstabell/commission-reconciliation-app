-- Create table for storing user-specific reconciliation column mappings
-- This table stores the mappings that users create when importing CSV/Excel files
-- for reconciliation to map statement columns to system fields

CREATE TABLE IF NOT EXISTS user_reconciliation_mappings (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID,
    user_email TEXT NOT NULL,
    mapping_name TEXT NOT NULL,
    column_mappings JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    -- Ensure each user can only have one mapping with the same name
    CONSTRAINT unique_user_mapping_name UNIQUE (user_email, mapping_name)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_reconciliation_mappings_user_email 
    ON user_reconciliation_mappings(user_email);

CREATE INDEX IF NOT EXISTS idx_user_reconciliation_mappings_user_id 
    ON user_reconciliation_mappings(user_id);

CREATE INDEX IF NOT EXISTS idx_user_reconciliation_mappings_mapping_name 
    ON user_reconciliation_mappings(mapping_name);

-- Add RLS policies
ALTER TABLE user_reconciliation_mappings ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view their own reconciliation mappings" ON user_reconciliation_mappings;
DROP POLICY IF EXISTS "Users can insert their own reconciliation mappings" ON user_reconciliation_mappings;
DROP POLICY IF EXISTS "Users can update their own reconciliation mappings" ON user_reconciliation_mappings;
DROP POLICY IF EXISTS "Users can delete their own reconciliation mappings" ON user_reconciliation_mappings;

-- Create RLS policies that work with the app's custom auth
CREATE POLICY "Users can view their own reconciliation mappings"
    ON user_reconciliation_mappings FOR SELECT
    TO authenticated, anon
    USING (true); -- App handles filtering by user_email

CREATE POLICY "Users can insert their own reconciliation mappings"
    ON user_reconciliation_mappings FOR INSERT
    TO authenticated, anon
    WITH CHECK (true); -- App handles user validation

CREATE POLICY "Users can update their own reconciliation mappings"
    ON user_reconciliation_mappings FOR UPDATE
    TO authenticated, anon
    USING (true); -- App handles filtering by user_email

CREATE POLICY "Users can delete their own reconciliation mappings"
    ON user_reconciliation_mappings FOR DELETE
    TO authenticated, anon
    USING (true); -- App handles filtering by user_email

-- Add comment to table
COMMENT ON TABLE user_reconciliation_mappings IS 'Stores user-specific column mappings for reconciliation CSV/Excel imports';
COMMENT ON COLUMN user_reconciliation_mappings.mapping_name IS 'User-friendly name for the mapping (e.g., "ABC Insurance Statement")';
COMMENT ON COLUMN user_reconciliation_mappings.column_mappings IS 'JSON object mapping system fields to statement columns';