-- Create table to store deleted policies for recovery
CREATE TABLE IF NOT EXISTS deleted_policies (
    deletion_id SERIAL PRIMARY KEY,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Original policy data (same columns as policies table)
    _id INTEGER,
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
    "Premium Sold" DOUBLE PRECISION,
    "Policy Gross Comm %" DOUBLE PRECISION,
    "STMT DATE" TEXT,
    "Agency Estimated Comm/Revenue (CRM)" DOUBLE PRECISION,
    "Agency Gross Comm Received" DOUBLE PRECISION,
    "Agent Estimated Comm $" DOUBLE PRECISION,
    "Paid Amount" DOUBLE PRECISION,
    "BALANCE DUE" DOUBLE PRECISION,
    "FULL OR MONTHLY PMTS" TEXT,
    "NOTES" TEXT
);

-- Create index for faster queries
CREATE INDEX idx_deleted_policies_deleted_at ON deleted_policies(deleted_at DESC);
CREATE INDEX idx_deleted_policies_transaction_id ON deleted_policies("Transaction ID");