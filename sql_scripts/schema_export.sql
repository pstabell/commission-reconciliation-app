CREATE TABLE commission_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                policy_number TEXT,
                customer TEXT,
                payment_amount REAL,
                statement_date TEXT,
                payment_timestamp TEXT
            , statement_details TEXT);
CREATE TABLE manual_commission_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT,
                policy_type TEXT,
                policy_number TEXT,
                effective_date TEXT,
                transaction_type TEXT,
                commission_paid REAL,
                agency_commission_received REAL,
                statement_date TEXT
            , client_id TEXT, transaction_id TEXT);
CREATE TABLE policies (
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
	"Agent Estimated Comm $" FLOAT, 
	"Paid Amount" TEXT, 
	"BALANCE DUE" FLOAT, 
	"FULL OR MONTHLY PMTS" TEXT, 
	"NOTES" TEXT
);
CREATE TABLE renewal_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    renewal_timestamp TEXT,
                    renewed_by TEXT,
                    original_transaction_id TEXT,
                    new_transaction_id TEXT,
                    details TEXT
                );
CREATE TABLE sqlite_sequence(name,seq);
