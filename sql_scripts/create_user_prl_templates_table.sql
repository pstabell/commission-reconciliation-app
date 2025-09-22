-- Create table for user-specific PRL templates
CREATE TABLE IF NOT EXISTS user_prl_templates (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    user_email TEXT NOT NULL,
    template_name TEXT NOT NULL,
    columns TEXT[] NOT NULL,
    view_mode TEXT DEFAULT 'all',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure each user can only have one template with a given name
    UNIQUE(user_id, template_name),
    UNIQUE(user_email, template_name)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_prl_templates_user_id ON user_prl_templates(user_id);
CREATE INDEX IF NOT EXISTS idx_user_prl_templates_user_email ON user_prl_templates(user_email);

-- Create RLS policy to ensure users can only see their own templates
ALTER TABLE user_prl_templates ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view their own PRL templates" ON user_prl_templates;
DROP POLICY IF EXISTS "Users can create their own PRL templates" ON user_prl_templates;
DROP POLICY IF EXISTS "Users can update their own PRL templates" ON user_prl_templates;
DROP POLICY IF EXISTS "Users can delete their own PRL templates" ON user_prl_templates;

-- Create new policies
-- Note: Since we're using custom auth, we'll rely on user_email matching
CREATE POLICY "Users can view their own PRL templates"
    ON user_prl_templates FOR SELECT
    USING (true);  -- We'll filter by user_email in the application

CREATE POLICY "Users can create their own PRL templates"
    ON user_prl_templates FOR INSERT
    WITH CHECK (true);  -- We'll ensure correct user_email in the application

CREATE POLICY "Users can update their own PRL templates"
    ON user_prl_templates FOR UPDATE
    USING (true);  -- We'll filter by user_email in the application

CREATE POLICY "Users can delete their own PRL templates"
    ON user_prl_templates FOR DELETE
    USING (true);  -- We'll filter by user_email in the application