-- PostgreSQL schema that EXACTLY matches the SQLite database structure
-- This preserves all column names and types as they exist in the source database

-- Enable UUID extension for ID generation (optional)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- POLICIES TABLE
-- ============================================
-- Note: SQLite doesn't have a primary key on this table, but we'll add one for PostgreSQL
CREATE TABLE IF NOT EXISTS policies (
    -- Add PostgreSQL ID (since SQLite table has no primary key)
    _id SERIAL PRIMARY KEY,
    
    -- All original columns with exact names and appropriate PostgreSQL types
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
    "Agency Estimated Comm/Revenue (CRM)" TEXT,
    "Agency Gross Comm Received" TEXT,
    "Agent Estimated Comm $" DOUBLE PRECISION,  -- FLOAT in SQLite = DOUBLE PRECISION in PostgreSQL
    "Paid Amount" TEXT,
    "BALANCE DUE" DOUBLE PRECISION,  -- FLOAT in SQLite = DOUBLE PRECISION in PostgreSQL
    "FULL OR MONTHLY PMTS" TEXT,
    "NOTES" TEXT
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_policies_client_id ON policies("Client ID");
CREATE INDEX IF NOT EXISTS idx_policies_transaction_id ON policies("Transaction ID");
CREATE INDEX IF NOT EXISTS idx_policies_customer ON policies("Customer");
CREATE INDEX IF NOT EXISTS idx_policies_policy_number ON policies("Policy Number");

-- ============================================
-- COMMISSION_PAYMENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS commission_payments (
    id SERIAL PRIMARY KEY,  -- INTEGER PRIMARY KEY in SQLite = SERIAL in PostgreSQL
    policy_number TEXT,
    customer TEXT,
    payment_amount REAL,  -- REAL in SQLite = REAL in PostgreSQL
    statement_date TEXT,
    payment_timestamp TEXT,
    statement_details TEXT
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_commission_payments_policy_number ON commission_payments(policy_number);
CREATE INDEX IF NOT EXISTS idx_commission_payments_customer ON commission_payments(customer);

-- ============================================
-- MANUAL_COMMISSION_ENTRIES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS manual_commission_entries (
    id SERIAL PRIMARY KEY,  -- INTEGER PRIMARY KEY in SQLite = SERIAL in PostgreSQL
    customer TEXT,
    policy_type TEXT,
    policy_number TEXT,
    effective_date TEXT,
    transaction_type TEXT,
    commission_paid REAL,  -- REAL in SQLite = REAL in PostgreSQL
    agency_commission_received REAL,  -- REAL in SQLite = REAL in PostgreSQL
    statement_date TEXT,
    client_id TEXT,
    transaction_id TEXT
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_manual_entries_client_id ON manual_commission_entries(client_id);
CREATE INDEX IF NOT EXISTS idx_manual_entries_transaction_id ON manual_commission_entries(transaction_id);
CREATE INDEX IF NOT EXISTS idx_manual_entries_policy_number ON manual_commission_entries(policy_number);

-- ============================================
-- RENEWAL_HISTORY TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS renewal_history (
    id SERIAL PRIMARY KEY,  -- INTEGER PRIMARY KEY in SQLite = SERIAL in PostgreSQL
    renewal_timestamp TEXT,
    renewed_by TEXT,
    original_transaction_id TEXT,
    new_transaction_id TEXT,
    details TEXT
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_renewal_history_original_tid ON renewal_history(original_transaction_id);
CREATE INDEX IF NOT EXISTS idx_renewal_history_new_tid ON renewal_history(new_transaction_id);

-- ============================================
-- DATA TYPE NOTES
-- ============================================
-- SQLite Type -> PostgreSQL Type mapping used:
-- INTEGER (PRIMARY KEY) -> SERIAL PRIMARY KEY
-- TEXT -> TEXT
-- REAL -> REAL
-- FLOAT -> DOUBLE PRECISION

-- ============================================
-- OPTIONAL: Add constraints if desired
-- ============================================
-- Add unique constraint on Transaction ID if needed
-- ALTER TABLE policies ADD CONSTRAINT uk_transaction_id UNIQUE ("Transaction ID");

-- ============================================
-- OPTIONAL: Helper views for data conversion
-- ============================================
-- View to parse dates from MM/DD/YYYY format
CREATE OR REPLACE VIEW policies_with_parsed_dates AS
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

-- ============================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================
COMMENT ON TABLE policies IS 'Main table storing all insurance policy records - imported from SQLite with original column names preserved';
COMMENT ON TABLE commission_payments IS 'Records of commission payments made to agents';
COMMENT ON TABLE manual_commission_entries IS 'Manual commission entries for special cases';
COMMENT ON TABLE renewal_history IS 'Audit trail of policy renewals';

COMMENT ON COLUMN policies."Transaction ID" IS 'Unique identifier for each transaction';
COMMENT ON COLUMN policies."X-DATE" IS 'Expiration date of the policy (stored as text in MM/DD/YYYY format)';
COMMENT ON COLUMN policies."Agent Estimated Comm $" IS 'Estimated commission amount in dollars';
COMMENT ON COLUMN policies."BALANCE DUE" IS 'Balance due amount';