-- Investigate the Edit Bug Creating Duplicates

-- 1. Check if we have exact duplicate Transaction IDs
SELECT 
    "Transaction ID",
    COUNT(*) as occurrences,
    STRING_AGG(DISTINCT "Customer", ', ') as customer_names,
    STRING_AGG(DISTINCT CAST(_id AS VARCHAR), ', ') as record_ids
FROM policies
GROUP BY "Transaction ID"
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC
LIMIT 10;

-- 2. Look specifically at Katie's policy
SELECT 
    _id,
    "Transaction ID",
    "Customer",
    "Policy Number",
    updated_at,
    created_at
FROM policies
WHERE "Policy Number" = '443939914'
ORDER BY updated_at DESC;

-- 3. Check if auto-save is creating duplicates by looking at update timestamps
WITH recent_updates AS (
    SELECT 
        "Transaction ID",
        "Customer",
        updated_at,
        LAG(updated_at) OVER (PARTITION BY "Transaction ID" ORDER BY updated_at) as prev_update
    FROM policies
    WHERE updated_at > NOW() - INTERVAL '1 hour'
)
SELECT 
    "Transaction ID",
    "Customer",
    updated_at,
    prev_update,
    EXTRACT(EPOCH FROM (updated_at - prev_update)) as seconds_between_updates
FROM recent_updates
WHERE prev_update IS NOT NULL
ORDER BY updated_at DESC
LIMIT 20;