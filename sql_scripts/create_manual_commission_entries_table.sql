-- Create manual_commission_entries table for storing reconciliation entries
-- This table is used by the Accounting page to store commission statement data

CREATE TABLE IF NOT EXISTS manual_commission_entries (
    id SERIAL PRIMARY KEY,
    customer TEXT NOT NULL,
    policy_type TEXT,
    policy_number TEXT NOT NULL,
    effective_date TEXT,
    transaction_type TEXT,
    commission_paid DOUBLE PRECISION DEFAULT 0,
    agency_commission_received DOUBLE PRECISION DEFAULT 0,
    statement_date TEXT,
    client_id TEXT,
    transaction_id TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_manual_entries_transaction_id ON manual_commission_entries(transaction_id);
CREATE INDEX IF NOT EXISTS idx_manual_entries_policy_number ON manual_commission_entries(policy_number);
CREATE INDEX IF NOT EXISTS idx_manual_entries_statement_date ON manual_commission_entries(statement_date);

-- Add comment explaining the table
COMMENT ON TABLE manual_commission_entries IS 'Stores manual commission entries for reconciliation in the Accounting section';