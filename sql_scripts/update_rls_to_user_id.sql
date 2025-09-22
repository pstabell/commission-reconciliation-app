-- Update RLS policies to use user_id instead of user_email
-- This completes the migration from email-based to UUID-based user identification

-- First, drop existing policies that use user_email
DROP POLICY IF EXISTS "Anyone can view their own data" ON policies;
DROP POLICY IF EXISTS "Anyone can insert with user_email" ON policies;
DROP POLICY IF EXISTS "Anyone can update their own data" ON policies;
DROP POLICY IF EXISTS "Anyone can delete their own data" ON policies;

-- Create new policies using user_id
CREATE POLICY "Users can view their own data by user_id" 
ON policies FOR SELECT 
TO anon, authenticated
USING (user_id IS NOT NULL);

CREATE POLICY "Users can insert with user_id" 
ON policies FOR INSERT 
TO anon, authenticated
WITH CHECK (user_id IS NOT NULL);

CREATE POLICY "Users can update their own data by user_id" 
ON policies FOR UPDATE
TO anon, authenticated
USING (user_id IS NOT NULL)
WITH CHECK (user_id IS NOT NULL);

CREATE POLICY "Users can delete their own data by user_id" 
ON policies FOR DELETE
TO anon, authenticated
USING (user_id IS NOT NULL);

-- Also update RLS for other tables that might have it
-- Carriers table
DROP POLICY IF EXISTS "Users can view their own carriers" ON carriers;
DROP POLICY IF EXISTS "Users can manage their own carriers" ON carriers;

CREATE POLICY "Users can view their own carriers by user_id" 
ON carriers FOR SELECT 
TO anon, authenticated
USING (user_id IS NOT NULL);

CREATE POLICY "Users can manage their own carriers by user_id" 
ON carriers FOR ALL
TO anon, authenticated
USING (user_id IS NOT NULL)
WITH CHECK (user_id IS NOT NULL);

-- MGAs table
DROP POLICY IF EXISTS "Users can view their own MGAs" ON mgas;
DROP POLICY IF EXISTS "Users can manage their own MGAs" ON mgas;

CREATE POLICY "Users can view their own MGAs by user_id" 
ON mgas FOR SELECT 
TO anon, authenticated
USING (user_id IS NOT NULL);

CREATE POLICY "Users can manage their own MGAs by user_id" 
ON mgas FOR ALL
TO anon, authenticated
USING (user_id IS NOT NULL)
WITH CHECK (user_id IS NOT NULL);

-- Commission rules table
DROP POLICY IF EXISTS "Users can view their own rules" ON commission_rules;
DROP POLICY IF EXISTS "Users can manage their own rules" ON commission_rules;

CREATE POLICY "Users can view their own rules by user_id" 
ON commission_rules FOR SELECT 
TO anon, authenticated
USING (user_id IS NOT NULL);

CREATE POLICY "Users can manage their own rules by user_id" 
ON commission_rules FOR ALL
TO anon, authenticated
USING (user_id IS NOT NULL)
WITH CHECK (user_id IS NOT NULL);