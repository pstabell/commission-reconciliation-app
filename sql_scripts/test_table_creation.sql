-- Minimal test to identify the exact error
-- Run each statement one by one to see which fails

-- Test 1: Create simple table with quoted column names
CREATE TABLE test_policies (
    id SERIAL PRIMARY KEY,
    "Client ID" TEXT,
    "Transaction ID" TEXT
);

-- Test 2: Try to select from it
SELECT "Client ID" FROM test_policies;

-- Test 3: Create index on quoted column
CREATE INDEX idx_test_client ON test_policies("Client ID");

-- Test 4: Drop test table
DROP TABLE test_policies;

-- Test 5: Create the real policies table without any views or foreign keys
CREATE TABLE policies (
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

-- Test 6: Verify columns exist
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'policies' 
AND column_name = 'Client ID';