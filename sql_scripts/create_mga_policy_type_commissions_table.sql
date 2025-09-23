-- Create MGA Policy Type Commissions table
-- This table allows setting specific commission rates for each policy type per MGA

CREATE TABLE IF NOT EXISTS mga_policy_type_commissions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    mga_id UUID NOT NULL REFERENCES mgas(mga_id) ON DELETE CASCADE,
    policy_type TEXT NOT NULL,
    new_rate DECIMAL(5,2) NOT NULL CHECK (new_rate >= 0 AND new_rate <= 100),
    renewal_rate DECIMAL(5,2) CHECK (renewal_rate >= 0 AND renewal_rate <= 100),
    rewrite_rate DECIMAL(5,2) CHECK (rewrite_rate >= 0 AND rewrite_rate <= 100),
    is_active BOOLEAN DEFAULT true,
    user_email TEXT NOT NULL,
    user_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(mga_id, policy_type, user_email)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_mga_policy_type_comm_mga ON mga_policy_type_commissions(mga_id);
CREATE INDEX IF NOT EXISTS idx_mga_policy_type_comm_type ON mga_policy_type_commissions(policy_type);
CREATE INDEX IF NOT EXISTS idx_mga_policy_type_comm_user ON mga_policy_type_commissions(user_email);
CREATE INDEX IF NOT EXISTS idx_mga_policy_type_comm_user_id ON mga_policy_type_commissions(user_id);

-- Apply update trigger
CREATE TRIGGER update_mga_policy_type_comm_updated_at BEFORE UPDATE ON mga_policy_type_commissions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add RLS policies for user isolation
ALTER TABLE mga_policy_type_commissions ENABLE ROW LEVEL SECURITY;

-- RLS policy for user_id
CREATE POLICY "mga_policy_type_comm_user_id_isolation" ON mga_policy_type_commissions
    FOR ALL
    USING (
        CASE 
            WHEN current_setting('app.user_id', true) IS NOT NULL 
            THEN user_id::text = current_setting('app.user_id', true)
            ELSE true
        END
    );

-- RLS policy for user_email (fallback)
CREATE POLICY "mga_policy_type_comm_user_email_isolation" ON mga_policy_type_commissions
    FOR ALL
    USING (
        CASE 
            WHEN current_setting('app.user_email', true) IS NOT NULL 
            THEN user_email = current_setting('app.user_email', true)
            ELSE true
        END
    );