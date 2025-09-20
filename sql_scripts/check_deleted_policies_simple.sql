-- Simple check of deleted_policies table

-- 1. Does the table have any rows at all?
SELECT COUNT(*) as total_rows FROM deleted_policies;

-- 2. Show first 5 rows (all columns)
SELECT * FROM deleted_policies LIMIT 5;

-- 3. Check audit_logs table instead
SELECT 'Checking audit_logs table:' as check;
SELECT COUNT(*) as audit_count FROM audit_logs;

-- 4. Sample from audit_logs
SELECT * FROM audit_logs 
WHERE action LIKE '%delete%' 
   OR action LIKE '%remove%'
   OR table_name = 'policies'
LIMIT 10;

-- 5. Check renewal_history for any clues
SELECT 'Checking renewal_history:' as check;
SELECT COUNT(*) as renewal_count FROM renewal_history;

-- 6. The math check - we know we should have 466 total
SELECT 'Current policies + deleted should = 466:' as check;
SELECT 
    (SELECT COUNT(*) FROM policies) as current_policies,
    (SELECT COUNT(*) FROM deleted_policies) as deleted_policies,
    (SELECT COUNT(*) FROM policies) + (SELECT COUNT(*) FROM deleted_policies) as total;