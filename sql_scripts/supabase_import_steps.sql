-- SUPABASE IMPORT STEPS
-- Run each section separately in Supabase SQL Editor to identify any issues

-- ========================================
-- SECTION 1: Setup and Clean Existing Views
-- ========================================
-- Enable extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop any existing views that might cause conflicts
DROP VIEW IF EXISTS policies_with_parsed_dates CASCADE;
DROP VIEW IF EXISTS active_policies CASCADE;
DROP VIEW IF EXISTS commission_summary CASCADE;

-- ========================================
-- SECTION 2: Create Main Tables
-- ========================================
-- Create policies table
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

-- Create commission_payments table
CREATE TABLE IF NOT EXISTS commission_payments (
    id SERIAL PRIMARY KEY,
    policy_number TEXT,
    customer TEXT,
    payment_amount REAL,
    statement_date TEXT,
    payment_timestamp TEXT,
    statement_details TEXT
);

-- Create manual_commission_entries table
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

-- Create renewal_history table
CREATE TABLE IF NOT EXISTS renewal_history (
    id SERIAL PRIMARY KEY,
    renewal_timestamp TEXT,
    renewed_by TEXT,
    original_transaction_id TEXT,
    new_transaction_id TEXT,
    details TEXT
);

-- ========================================
-- SECTION 3: Verify Tables Were Created
-- ========================================
-- Check that all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('policies', 'commission_payments', 'manual_commission_entries', 'renewal_history')
ORDER BY table_name;

-- ========================================
-- SECTION 4: Create Indexes
-- ========================================
-- Policies table indexes
CREATE INDEX IF NOT EXISTS idx_policies_client_id ON policies("Client ID");
CREATE INDEX IF NOT EXISTS idx_policies_transaction_id ON policies("Transaction ID");
CREATE INDEX IF NOT EXISTS idx_policies_customer ON policies("Customer");
CREATE INDEX IF NOT EXISTS idx_policies_policy_number ON policies("Policy Number");

-- Commission payments indexes
CREATE INDEX IF NOT EXISTS idx_commission_payments_policy_number ON commission_payments(policy_number);
CREATE INDEX IF NOT EXISTS idx_commission_payments_customer ON commission_payments(customer);

-- Manual entries indexes
CREATE INDEX IF NOT EXISTS idx_manual_entries_client_id ON manual_commission_entries(client_id);
CREATE INDEX IF NOT EXISTS idx_manual_entries_transaction_id ON manual_commission_entries(transaction_id);
CREATE INDEX IF NOT EXISTS idx_manual_entries_policy_number ON manual_commission_entries(policy_number);

-- Renewal history indexes
CREATE INDEX IF NOT EXISTS idx_renewal_history_original_tid ON renewal_history(original_transaction_id);
CREATE INDEX IF NOT EXISTS idx_renewal_history_new_tid ON renewal_history(new_transaction_id);

-- ========================================
-- SECTION 5: Create Views
-- ========================================
-- Create helper view for parsed dates
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

-- ========================================
-- SECTION 6: Add Documentation
-- ========================================
COMMENT ON TABLE policies IS 'Main table storing all insurance policy records';
COMMENT ON TABLE commission_payments IS 'Records of commission payments made to agents';
COMMENT ON TABLE manual_commission_entries IS 'Manual commission entries for special cases';
COMMENT ON TABLE renewal_history IS 'Audit trail of policy renewals';

-- ========================================
-- SECTION 7: Final Verification
-- ========================================
-- Verify all objects were created successfully
SELECT 
    'Tables' as object_type,
    COUNT(*) as count
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('policies', 'commission_payments', 'manual_commission_entries', 'renewal_history')
UNION ALL
SELECT 
    'Views' as object_type,
    COUNT(*) as count
FROM information_schema.views 
WHERE table_schema = 'public' 
AND table_name = 'policies_with_parsed_dates'
UNION ALL
SELECT 
    'Indexes' as object_type,
    COUNT(*) as count
FROM pg_indexes 
WHERE schemaname = 'public' 
AND tablename IN ('policies', 'commission_payments', 'manual_commission_entries', 'renewal_history');