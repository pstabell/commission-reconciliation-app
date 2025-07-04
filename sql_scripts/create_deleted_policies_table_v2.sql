-- Drop the old table if it exists
DROP TABLE IF EXISTS deleted_policies;

-- Create a more flexible deleted_policies table that stores data as JSONB
CREATE TABLE deleted_policies (
    deletion_id SERIAL PRIMARY KEY,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_id TEXT NOT NULL,
    customer_name TEXT,
    policy_data JSONB NOT NULL
);

-- Create indexes for faster queries
CREATE INDEX idx_deleted_policies_deleted_at ON deleted_policies(deleted_at DESC);
CREATE INDEX idx_deleted_policies_transaction_id ON deleted_policies(transaction_id);
CREATE INDEX idx_deleted_policies_customer ON deleted_policies(customer_name);

-- Add a comment explaining the table
COMMENT ON TABLE deleted_policies IS 'Stores archived policy records before deletion for recovery purposes';
COMMENT ON COLUMN deleted_policies.policy_data IS 'Complete policy record stored as JSON for flexibility';