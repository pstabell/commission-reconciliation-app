-- PostgreSQL data migration from SQLite
-- Generated on: 2025-07-02 15:14:03

-- Disable foreign key checks during import
SET session_replication_role = 'replica';

-- Re-enable foreign key checks
SET session_replication_role = 'origin';

-- Update foreign key relationships
-- This requires matching policy_id based on policy_number
UPDATE commission_payments cp
SET policy_id = p.id
FROM policies p
WHERE cp.policy_number = p.policy_number;

-- Update renewal history foreign keys
UPDATE renewal_history rh
SET original_policy_id = p1.id,
    new_policy_id = p2.id
FROM policies p1, policies p2
WHERE rh.original_transaction_id = p1.transaction_id
AND rh.new_transaction_id = p2.transaction_id;