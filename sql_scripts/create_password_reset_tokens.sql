-- Create password reset tokens table
-- Run this in your production Supabase SQL editor

CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_email FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_password_reset_token ON password_reset_tokens(token);
CREATE INDEX IF NOT EXISTS idx_password_reset_email ON password_reset_tokens(email);

-- Add RLS policies
ALTER TABLE password_reset_tokens ENABLE ROW LEVEL SECURITY;

-- Allow anon users to insert tokens (for password reset requests)
CREATE POLICY "Allow anon to create reset tokens" ON password_reset_tokens
    FOR INSERT
    TO anon
    WITH CHECK (true);

-- Allow anon users to read their own tokens
CREATE POLICY "Allow anon to read valid tokens" ON password_reset_tokens
    FOR SELECT
    TO anon
    USING (expires_at > NOW() AND used = FALSE);

-- Allow anon users to update tokens (mark as used)
CREATE POLICY "Allow anon to mark tokens as used" ON password_reset_tokens
    FOR UPDATE
    TO anon
    USING (expires_at > NOW() AND used = FALSE)
    WITH CHECK (used = TRUE);

-- Add password_hash column to users table if it doesn't exist
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);

-- Note: In production, you'll want to properly hash passwords
-- For now, we'll store a placeholder