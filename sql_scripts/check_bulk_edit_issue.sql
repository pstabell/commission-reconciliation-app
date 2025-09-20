-- CHECK BULK EDIT ISSUES - Why count went 425 → 500s → 383

-- 1. Timeline of record counts
SELECT 'Record count timeline:' as analysis;
SELECT 
    DATE_TRUNC('hour', updated_at) as hour,
    COUNT(*) as records_updated,
    COUNT(DISTINCT "Transaction ID") as unique_transactions,
    COUNT(*) - COUNT(DISTINCT "Transaction ID") as duplicates_in_hour
FROM policies
WHERE updated_at > NOW() - INTERVAL '6 hours'
GROUP BY DATE_TRUNC('hour', updated_at)
ORDER BY hour DESC;

-- 2. Find records that might have been deleted
-- Compare transaction types before and after
SELECT 'Transaction type changes:' as analysis;
WITH recent_changes AS (
    SELECT 
        "Transaction Type",
        COUNT(*) as current_count
    FROM policies
    GROUP BY "Transaction Type"
)
SELECT 
    "Transaction Type",
    current_count,
    CASE 
        WHEN "Transaction Type" = 'NEW' THEN current_count - 111  -- Expected 111 NEW
        WHEN "Transaction Type" = 'RWL' THEN current_count - 11   -- Expected 11 RWL
        WHEN "Transaction Type" = 'END' THEN current_count - 22   -- Expected 22 END
        WHEN "Transaction Type" = 'PMT' THEN current_count - 22   -- Expected 22 PMT
        ELSE 0
    END as difference_from_expected
FROM recent_changes
ORDER BY "Transaction Type";

-- 3. Check if certain customers are missing entirely
SELECT 'Customer record counts:' as analysis;
SELECT 
    CASE 
        WHEN "Customer" = 'Perfect Lanais LLC' THEN 'Perfect Lanais LLC (should be 13)'
        WHEN "Customer" = 'Deborah Cordette' THEN 'Deborah Cordette (should be 11)'
        WHEN "Customer" = 'Quantum 26 Enterprises, Inc.' THEN 'Quantum 26 (should be 8)'
        ELSE "Customer"
    END as customer_check,
    COUNT(*) as actual_count
FROM policies
WHERE "Customer" IN ('Perfect Lanais LLC', 'Deborah Cordette', 'Quantum 26 Enterprises, Inc.')
GROUP BY "Customer"
ORDER BY COUNT(*) DESC;

-- 4. Look for patterns in what's missing
SELECT 'Missing pattern analysis:' as analysis;
SELECT 
    "Transaction Type",
    "Carrier Name",
    COUNT(*) as count
FROM policies
GROUP BY "Transaction Type", "Carrier Name"
ORDER BY "Transaction Type", count DESC
LIMIT 20;

-- 5. Check if bulk edits created then deleted records
SELECT 'Bulk edit detection:' as analysis;
SELECT 
    "Customer",
    COUNT(*) as record_count,
    MIN(updated_at) as first_update,
    MAX(updated_at) as last_update,
    EXTRACT(EPOCH FROM (MAX(updated_at) - MIN(updated_at))) as seconds_between_updates
FROM policies
WHERE updated_at > NOW() - INTERVAL '2 hours'
GROUP BY "Customer"
HAVING COUNT(*) > 1
ORDER BY last_update DESC
LIMIT 20;