-- PostgreSQL schema with debugging - Execute step by step to identify the error

-- STEP 1: Enable extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- STEP 2: Drop any existing views that might reference the tables
DROP VIEW IF EXISTS policies_with_parsed_dates CASCADE;
DROP VIEW IF EXISTS active_policies CASCADE;
DROP VIEW IF EXISTS commission_summary CASCADE;

-- STEP 3: Create policies table
CREATE TABLE IF NOT EXISTS policies (
    _id SERIAL PRIMARY KEY,
    "Client ID" TEXT,
    "Transaction ID" TEXT,
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
    "Agent Estimated Comm $" DOUBLE PRECISION,
    "Paid Amount" TEXT,
    "BALANCE DUE" DOUBLE PRECISION,
    "FULL OR MONTHLY PMTS" TEXT,
    "NOTES" TEXT
);

-- STEP 4: Verify table was created
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'policies' 
ORDER BY ordinal_position;

-- STEP 5: Create indexes (only after confirming table exists)
CREATE INDEX IF NOT EXISTS idx_policies_client_id ON policies("Client ID");
CREATE INDEX IF NOT EXISTS idx_policies_transaction_id ON policies("Transaction ID");
CREATE INDEX IF NOT EXISTS idx_policies_customer ON policies("Customer");
CREATE INDEX IF NOT EXISTS idx_policies_policy_number ON policies("Policy Number");

-- STEP 6: Create other tables
CREATE TABLE IF NOT EXISTS commission_payments (
    id SERIAL PRIMARY KEY,
    policy_number TEXT,
    customer TEXT,
    payment_amount REAL,
    statement_date TEXT,
    payment_timestamp TEXT,
    statement_details TEXT
);

CREATE TABLE IF NOT EXISTS manual_commission_entries (
    id SERIAL PRIMARY KEY,
    customer TEXT,
    policy_type TEXT,
    policy_number TEXT,
    effective_date TEXT,
    transaction_type TEXT,
    commission_paid REAL,
    agency_commission_received REAL,
    statement_date TEXT,
    client_id TEXT,
    transaction_id TEXT
);

CREATE TABLE IF NOT EXISTS renewal_history (
    id SERIAL PRIMARY KEY,
    renewal_timestamp TEXT,
    renewed_by TEXT,
    original_transaction_id TEXT,
    new_transaction_id TEXT,
    details TEXT
);

-- STEP 7: Create indexes for other tables
CREATE INDEX IF NOT EXISTS idx_commission_payments_policy_number ON commission_payments(policy_number);
CREATE INDEX IF NOT EXISTS idx_commission_payments_customer ON commission_payments(customer);
CREATE INDEX IF NOT EXISTS idx_manual_entries_client_id ON manual_commission_entries(client_id);
CREATE INDEX IF NOT EXISTS idx_manual_entries_transaction_id ON manual_commission_entries(transaction_id);
CREATE INDEX IF NOT EXISTS idx_manual_entries_policy_number ON manual_commission_entries(policy_number);
CREATE INDEX IF NOT EXISTS idx_renewal_history_original_tid ON renewal_history(original_transaction_id);
CREATE INDEX IF NOT EXISTS idx_renewal_history_new_tid ON renewal_history(new_transaction_id);

-- STEP 8: Create views (only after all tables exist)
CREATE VIEW policies_with_parsed_dates AS
SELECT 
    _id,
    "Client ID",
    "Transaction ID",
    "Customer",
    "Carrier Name",
    "Policy Type",
    "Policy Number",
    "Transaction Type",
    "Agent Comm (NEW 50% RWL 25%)",
    "Policy Origination Date",
    CASE 
        WHEN "Policy Origination Date" ~ '^\d{2}/\d{2}/\d{4}$' 
        THEN TO_DATE("Policy Origination Date", 'MM/DD/YYYY')
        ELSE NULL 
    END as policy_origination_date_parsed,
    "Effective Date",
    CASE 
        WHEN "Effective Date" ~ '^\d{2}/\d{2}/\d{4}$' 
        THEN TO_DATE("Effective Date", 'MM/DD/YYYY')
        ELSE NULL 
    END as effective_date_parsed,
    "X-DATE",
    CASE 
        WHEN "X-DATE" ~ '^\d{2}/\d{2}/\d{4}$' 
        THEN TO_DATE("X-DATE", 'MM/DD/YYYY')
        ELSE NULL 
    END as x_date_parsed,
    "NEW BIZ CHECKLIST COMPLETE",
    "Premium Sold",
    CASE 
        WHEN "Premium Sold" ~ '^\$?[0-9,]+\.?\d*$' 
        THEN REPLACE(REPLACE("Premium Sold", '$', ''), ',', '')::NUMERIC
        ELSE NULL 
    END as premium_sold_numeric,
    "Policy Gross Comm %",
    "STMT DATE",
    CASE 
        WHEN "STMT DATE" ~ '^\d{2}/\d{2}/\d{4}$' 
        THEN TO_DATE("STMT DATE", 'MM/DD/YYYY')
        ELSE NULL 
    END as stmt_date_parsed,
    "Agency Estimated Comm/Revenue (AZ)",
    "Agency Gross Comm Received",
    "Agent Estimated Comm $",
    "Paid Amount",
    "BALANCE DUE",
    "FULL OR MONTHLY PMTS",
    "NOTES"
FROM policies;

-- STEP 9: Add comments
COMMENT ON TABLE policies IS 'Main table storing all insurance policy records - imported from SQLite with original column names preserved';
COMMENT ON TABLE commission_payments IS 'Records of commission payments made to agents';
COMMENT ON TABLE manual_commission_entries IS 'Manual commission entries for special cases';
COMMENT ON TABLE renewal_history IS 'Audit trail of policy renewals';