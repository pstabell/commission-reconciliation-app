-- Check for recent manual commission entries
SELECT * FROM manual_commission_entries 
ORDER BY created_at DESC 
LIMIT 10;

-- Check for recent commission payments
SELECT * FROM commission_payments 
ORDER BY created_at DESC 
LIMIT 5;

-- Check for recent policies added (reconciliation adds to policies table too)
SELECT * FROM policies 
WHERE "Description" LIKE 'Reconciled Statement%'
ORDER BY created_at DESC 
LIMIT 10;