-- Check if commission_payments table exists and has the correct structure
-- If the table exists without 'customer' column, add it
-- If the table doesn't exist, create it

-- First, check if the table exists
DO $$
BEGIN
    -- Check if table exists
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'commission_payments') THEN
        -- Table exists, check if customer column exists
        IF NOT EXISTS (SELECT FROM information_schema.columns 
                      WHERE table_name = 'commission_payments' 
                      AND column_name = 'customer') THEN
            -- Add customer column if it doesn't exist
            ALTER TABLE commission_payments ADD COLUMN customer TEXT NOT NULL DEFAULT 'Unknown';
            RAISE NOTICE 'Added customer column to commission_payments table';
        END IF;
    ELSE
        -- Table doesn't exist, create it
        CREATE TABLE commission_payments (
            id SERIAL PRIMARY KEY,
            policy_number TEXT NOT NULL,
            customer TEXT NOT NULL,
            payment_amount DOUBLE PRECISION NOT NULL,
            statement_date TEXT,
            payment_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            statement_details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create indexes
        CREATE INDEX idx_commission_payments_policy_number ON commission_payments(policy_number);
        CREATE INDEX idx_commission_payments_customer ON commission_payments(customer);
        CREATE INDEX idx_commission_payments_statement_date ON commission_payments(statement_date);
        
        RAISE NOTICE 'Created commission_payments table';
    END IF;
END $$;

-- Verify the table structure
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'commission_payments'
ORDER BY ordinal_position;