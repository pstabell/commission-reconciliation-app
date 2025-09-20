-- PostgreSQL schema for Supabase deployment
-- Converted from SQLite schema

-- Enable UUID extension for better ID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if they exist (for clean deployment)
DROP TABLE IF EXISTS renewal_history CASCADE;
DROP TABLE IF EXISTS manual_commission_entries CASCADE;
DROP TABLE IF EXISTS commission_payments CASCADE;
DROP TABLE IF EXISTS policies CASCADE;

-- Create policies table (main table)
CREATE TABLE policies (
    -- Use UUID for better distributed systems compatibility
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    
    -- Core identifiers
    client_id TEXT,
    transaction_id TEXT UNIQUE NOT NULL,
    
    -- Customer information
    customer TEXT NOT NULL,
    
    -- Policy details
    carrier_name TEXT,
    policy_type TEXT,
    policy_number TEXT NOT NULL,
    transaction_type TEXT CHECK (transaction_type IN ('NEW', 'RWL', 'CAN', 'REI', 'REW')),
    
    -- Commission rates
    agent_comm_rate TEXT, -- Was "Agent Comm (NEW 50% RWL 25%)"
    
    -- Dates
    policy_origination_date DATE,
    effective_date DATE NOT NULL,
    expiration_date DATE, -- Was "X-DATE"
    
    -- Checklist and status
    new_biz_checklist_complete BOOLEAN DEFAULT FALSE,
    
    -- Financial fields
    premium_sold DECIMAL(10,2),
    policy_gross_comm_percent DECIMAL(5,2),
    stmt_date DATE,
    agency_estimated_comm_revenue DECIMAL(10,2), -- Was "Agency Estimated Comm/Revenue (AZ)"
    agency_gross_comm_received DECIMAL(10,2),
    agent_estimated_comm DECIMAL(10,2), -- Was "Agent Estimated Comm $"
    paid_amount DECIMAL(10,2),
    balance_due DECIMAL(10,2) GENERATED ALWAYS AS (
        COALESCE(agent_estimated_comm, 0) - COALESCE(paid_amount, 0)
    ) STORED,
    
    -- Payment type
    payment_type TEXT CHECK (payment_type IN ('FULL', 'MONTHLY')), -- Was "FULL OR MONTHLY PMTS"
    
    -- Notes
    notes TEXT,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for policies table
CREATE INDEX idx_policies_transaction_id ON policies(transaction_id);
CREATE INDEX idx_policies_client_id ON policies(client_id);
CREATE INDEX idx_policies_customer ON policies(customer);
CREATE INDEX idx_policies_policy_number ON policies(policy_number);
CREATE INDEX idx_policies_effective_date ON policies(effective_date);
CREATE INDEX idx_policies_transaction_type ON policies(transaction_type);

-- Create commission_payments table
CREATE TABLE commission_payments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    policy_number TEXT NOT NULL,
    customer TEXT NOT NULL,
    payment_amount DECIMAL(10,2) NOT NULL,
    statement_date DATE,
    payment_timestamp TIMESTAMPTZ DEFAULT NOW(),
    statement_details JSONB, -- Using JSONB for flexible storage
    
    -- Add foreign key relationship
    policy_id UUID,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for commission_payments
CREATE INDEX idx_commission_payments_policy_number ON commission_payments(policy_number);
CREATE INDEX idx_commission_payments_customer ON commission_payments(customer);
CREATE INDEX idx_commission_payments_statement_date ON commission_payments(statement_date);

-- Create manual_commission_entries table
CREATE TABLE manual_commission_entries (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    customer TEXT NOT NULL,
    policy_type TEXT,
    policy_number TEXT NOT NULL,
    effective_date DATE,
    transaction_type TEXT,
    commission_paid DECIMAL(10,2),
    agency_commission_received DECIMAL(10,2),
    statement_date DATE,
    client_id TEXT,
    transaction_id TEXT,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for manual_commission_entries
CREATE INDEX idx_manual_entries_client_id ON manual_commission_entries(client_id);
CREATE INDEX idx_manual_entries_transaction_id ON manual_commission_entries(transaction_id);
CREATE INDEX idx_manual_entries_policy_number ON manual_commission_entries(policy_number);

-- Create renewal_history table
CREATE TABLE renewal_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    renewal_timestamp TIMESTAMPTZ DEFAULT NOW(),
    renewed_by TEXT NOT NULL,
    original_transaction_id TEXT NOT NULL,
    new_transaction_id TEXT NOT NULL,
    details JSONB, -- Using JSONB for flexible storage
    
    -- Foreign key relationships
    original_policy_id UUID,
    new_policy_id UUID,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for renewal_history
CREATE INDEX idx_renewal_history_original_transaction ON renewal_history(original_transaction_id);
CREATE INDEX idx_renewal_history_new_transaction ON renewal_history(new_transaction_id);

-- Add foreign key constraints after all tables are created
ALTER TABLE commission_payments 
    ADD CONSTRAINT fk_commission_payments_policy 
    FOREIGN KEY (policy_id) 
    REFERENCES policies(id) 
    ON DELETE SET NULL;

ALTER TABLE renewal_history 
    ADD CONSTRAINT fk_renewal_original_policy 
    FOREIGN KEY (original_policy_id) 
    REFERENCES policies(id) 
    ON DELETE SET NULL;

ALTER TABLE renewal_history 
    ADD CONSTRAINT fk_renewal_new_policy 
    FOREIGN KEY (new_policy_id) 
    REFERENCES policies(id) 
    ON DELETE SET NULL;

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at columns
CREATE TRIGGER update_policies_updated_at BEFORE UPDATE ON policies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_commission_payments_updated_at BEFORE UPDATE ON commission_payments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_manual_entries_updated_at BEFORE UPDATE ON manual_commission_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create views for common queries
CREATE VIEW active_policies AS
SELECT * FROM policies
WHERE transaction_type != 'CAN'
AND (expiration_date IS NULL OR expiration_date >= CURRENT_DATE);

CREATE VIEW commission_summary AS
SELECT 
    customer,
    COUNT(*) as policy_count,
    SUM(agent_estimated_comm) as total_estimated_commission,
    SUM(paid_amount) as total_paid,
    SUM(balance_due) as total_balance_due
FROM policies
GROUP BY customer;

-- Row Level Security (RLS) policies can be added here for Supabase
-- Example:
-- ALTER TABLE policies ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Enable all access for authenticated users" ON policies
--     FOR ALL USING (auth.role() = 'authenticated');

-- Add comments for documentation
COMMENT ON TABLE policies IS 'Main table storing all insurance policy records';
COMMENT ON TABLE commission_payments IS 'Records of commission payments made to agents';
COMMENT ON TABLE manual_commission_entries IS 'Manual commission entries for special cases';
COMMENT ON TABLE renewal_history IS 'Audit trail of policy renewals';

COMMENT ON COLUMN policies.balance_due IS 'Automatically calculated as agent_estimated_comm - paid_amount';
COMMENT ON COLUMN policies.transaction_type IS 'NEW=New Business, RWL=Renewal, CAN=Cancellation, REI=Reinstatement, REW=Rewrite';