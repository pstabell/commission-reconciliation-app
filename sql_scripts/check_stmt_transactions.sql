-- Check STMT transaction patterns

-- 1. How many STMT transactions exist?
SELECT 'STMT Transaction Count:' as check;
SELECT 
    CASE 
        WHEN "Transaction ID" LIKE '%-STMT-%' THEN 'STMT Transactions'
        WHEN "Transaction ID" LIKE '%-VOID-%' THEN 'VOID Transactions'
        WHEN "Transaction ID" LIKE '%-ADJ-%' THEN 'ADJ Transactions'
        WHEN "Transaction ID" LIKE '%-IMPORT%' THEN 'IMPORT Transactions'
        ELSE 'Regular Transactions'
    END as transaction_category,
    COUNT(*) as count
FROM policies
GROUP BY transaction_category
ORDER BY count DESC;

-- 2. Sample STMT transactions
SELECT 'Sample STMT Transactions:' as check;
SELECT 
    "Transaction ID",
    "Customer",
    "Transaction Type",
    updated_at
FROM policies
WHERE "Transaction ID" LIKE '%-STMT-%'
LIMIT 10;

-- 3. Check if STMT transactions have duplicates
SELECT 'STMT Duplicates:' as check;
SELECT 
    "Transaction ID",
    COUNT(*) as copies
FROM policies
WHERE "Transaction ID" LIKE '%-STMT-%'
GROUP BY "Transaction ID"
HAVING COUNT(*) > 1
LIMIT 10;

-- 4. Your sample IDs
SELECT 'Your Sample IDs Analysis:' as check;
SELECT 
    "Transaction ID",
    "Customer",
    "Transaction Type",
    COUNT(*) OVER (PARTITION BY "Transaction ID") as copies_of_this_id
FROM policies
WHERE "Transaction ID" IN ('C8HL176-ST', 'ME5D1Q6-ST', '0POM131-IM');