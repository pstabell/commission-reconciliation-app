-- PostgreSQL schema for Supabase deployment (SAFE VERSION - Corrected with actual column names)
-- This version matches the exact SQLite column names from the database

-- Enable UUID extension for better ID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create policies table (main table with exact column names from SQLite)
CREATE TABLE IF NOT EXISTS policies (
    -- Add a UUID primary key for PostgreSQL
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    
    -- Exact columns from SQLite database (keeping original names with quotes)
    "Client ID" TEXT,
    "Transaction ID" TEXT UNIQUE,
    "Customer" TEXT,
    "Carrier Name" TEXT,
    "Policy Type" TEXT,
    "Policy Number" TEXT,
    "Transaction Type" TEXT,
    "Agent Comm (NEW 50% RWL 25%)" TEXT,
    "Policy Origination Date" TEXT,
    "Effective Date" TEXT,
    "X-DATE" TEXT,
    "NEW BIZ CHECKLIST COMPLETE" TEXT,
    "Premium Sold" TEXT,
    "Policy Gross Comm %" TEXT,
    "STMT DATE" TEXT,
    "Agency Estimated Comm/Revenue (AZ)" TEXT,
    "Agency Gross Comm Received" TEXT,
    "Agent Estimated Comm $" DECIMAL(10,2),
    "Paid Amount" TEXT,
    "BALANCE DUE" DECIMAL(10,2),
    "FULL OR MONTHLY PMTS" TEXT,
    "NOTES" TEXT,
    
    -- Timestamps for PostgreSQL
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for policies table
CREATE INDEX IF NOT EXISTS idx_policies_transaction_id ON policies("Transaction ID");
CREATE INDEX IF NOT EXISTS idx_policies_client_id ON policies("Client ID");
CREATE INDEX IF NOT EXISTS idx_policies_customer ON policies("Customer");
CREATE INDEX IF NOT EXISTS idx_policies_policy_number ON policies("Policy Number");
CREATE INDEX IF NOT EXISTS idx_policies_effective_date ON policies("Effective Date");
CREATE INDEX IF NOT EXISTS idx_policies_transaction_type ON policies("Transaction Type");

-- Create commission_payments table
CREATE TABLE IF NOT EXISTS commission_payments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    policy_number TEXT,
    customer TEXT,
    payment_amount DECIMAL(10,2),
    statement_date TEXT,
    payment_timestamp TEXT,
    statement_details TEXT,
    
    -- Add foreign key relationship (will be linked by policy_number)
    policy_id UUID,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for commission_payments
CREATE INDEX IF NOT EXISTS idx_commission_payments_policy_number ON commission_payments(policy_number);
CREATE INDEX IF NOT EXISTS idx_commission_payments_customer ON commission_payments(customer);
CREATE INDEX IF NOT EXISTS idx_commission_payments_statement_date ON commission_payments(statement_date);

-- Create manual_commission_entries table
CREATE TABLE IF NOT EXISTS manual_commission_entries (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    customer TEXT,
    policy_type TEXT,
    policy_number TEXT,
    effective_date TEXT,
    transaction_type TEXT,
    commission_paid DECIMAL(10,2),
    agency_commission_received DECIMAL(10,2),
    statement_date TEXT,
    client_id TEXT,
    transaction_id TEXT,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for manual_commission_entries
CREATE INDEX IF NOT EXISTS idx_manual_entries_client_id ON manual_commission_entries(client_id);
CREATE INDEX IF NOT EXISTS idx_manual_entries_transaction_id ON manual_commission_entries(transaction_id);
CREATE INDEX IF NOT EXISTS idx_manual_entries_policy_number ON manual_commission_entries(policy_number);

-- Create renewal_history table
CREATE TABLE IF NOT EXISTS renewal_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    renewal_timestamp TEXT,
    renewed_by TEXT,
    original_transaction_id TEXT,
    new_transaction_id TEXT,
    details TEXT,
    
    -- Foreign key relationships
    original_policy_id UUID,
    new_policy_id UUID,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for renewal_history
CREATE INDEX IF NOT EXISTS idx_renewal_history_original_transaction ON renewal_history(original_transaction_id);
CREATE INDEX IF NOT EXISTS idx_renewal_history_new_transaction ON renewal_history(new_transaction_id);

-- Add foreign key constraints (only if they don't exist)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_commission_payments_policy') THEN
        ALTER TABLE commission_payments 
            ADD CONSTRAINT fk_commission_payments_policy 
            FOREIGN KEY (policy_id) 
            REFERENCES policies(id) 
            ON DELETE SET NULL;
    END IF;
END $$;

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_renewal_original_policy') THEN
        ALTER TABLE renewal_history 
            ADD CONSTRAINT fk_renewal_original_policy 
            FOREIGN KEY (original_policy_id) 
            REFERENCES policies(id) 
            ON DELETE SET NULL;
    END IF;
END $$;

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_renewal_new_policy') THEN
        ALTER TABLE renewal_history 
            ADD CONSTRAINT fk_renewal_new_policy 
            FOREIGN KEY (new_policy_id) 
            REFERENCES policies(id) 
            ON DELETE SET NULL;
    END IF;
END $$;

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at columns (with IF NOT EXISTS logic)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_policies_updated_at') THEN
        CREATE TRIGGER update_policies_updated_at 
            BEFORE UPDATE ON policies
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    END IF;
END $$;

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_commission_payments_updated_at') THEN
        CREATE TRIGGER update_commission_payments_updated_at 
            BEFORE UPDATE ON commission_payments
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    END IF;
END $$;

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_manual_entries_updated_at') THEN
        CREATE TRIGGER update_manual_entries_updated_at 
            BEFORE UPDATE ON manual_commission_entries
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    END IF;
END $$;

-- Create views for common queries
CREATE OR REPLACE VIEW active_policies AS
SELECT * FROM policies
WHERE "Transaction Type" != 'CAN'
AND ("X-DATE" IS NULL OR TO_DATE("X-DATE", 'MM/DD/YYYY') >= CURRENT_DATE);

CREATE OR REPLACE VIEW commission_summary AS
SELECT 
    "Customer",
    COUNT(*) as policy_count,
    SUM("Agent Estimated Comm $") as total_estimated_commission,
    SUM(CASE 
        WHEN "Paid Amount" ~ '^[0-9.,]+$' 
        THEN REPLACE(REPLACE("Paid Amount", '$', ''), ',', '')::DECIMAL
        ELSE 0 
    END) as total_paid,
    SUM("BALANCE DUE") as total_balance_due
FROM policies
GROUP BY "Customer";

-- Helper function to clean currency strings
CREATE OR REPLACE FUNCTION clean_currency(text) RETURNS DECIMAL AS $$
BEGIN
    RETURN CASE 
        WHEN $1 IS NULL OR $1 = '' THEN 0
        ELSE REPLACE(REPLACE(REPLACE($1, '$', ''), ',', ''), ' ', '')::DECIMAL
    END;
EXCEPTION WHEN OTHERS THEN
    RETURN 0;
END;
$$ LANGUAGE plpgsql;

-- Row Level Security (RLS) policies can be added here for Supabase
-- Example (uncomment to enable):
-- ALTER TABLE policies ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Enable all access for authenticated users" ON policies
--     FOR ALL USING (auth.role() = 'authenticated');

-- Add comments for documentation
COMMENT ON TABLE policies IS 'Main table storing all insurance policy records';
COMMENT ON TABLE commission_payments IS 'Records of commission payments made to agents';
COMMENT ON TABLE manual_commission_entries IS 'Manual commission entries for special cases';
COMMENT ON TABLE renewal_history IS 'Audit trail of policy renewals';

COMMENT ON COLUMN policies."Transaction ID" IS 'Unique identifier for each transaction';
COMMENT ON COLUMN policies."X-DATE" IS 'Expiration date of the policy';
COMMENT ON COLUMN policies."Transaction Type" IS 'NEW=New Business, RWL=Renewal, CAN=Cancellation, etc.';

-- Grant permissions for Supabase (adjust based on your needs)
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres;
-- GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO postgres;
-- GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO postgres;