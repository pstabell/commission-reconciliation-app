-- Create a simpler commission_payments_simple table that matches what the app expects
CREATE TABLE IF NOT EXISTS commission_payments_simple (
    id SERIAL PRIMARY KEY,
    policy_number TEXT NOT NULL,
    customer TEXT NOT NULL,
    payment_amount DECIMAL(10,2) NOT NULL,
    statement_date DATE,
    payment_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    statement_details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_simple_payments_policy_number ON commission_payments_simple(policy_number);
CREATE INDEX IF NOT EXISTS idx_simple_payments_customer ON commission_payments_simple(customer);
CREATE INDEX IF NOT EXISTS idx_simple_payments_statement_date ON commission_payments_simple(statement_date);

-- Grant all permissions (no RLS)
GRANT ALL ON commission_payments_simple TO anon, authenticated;

-- Verify the table was created
SELECT 'Table created successfully' as status;