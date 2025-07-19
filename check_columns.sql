-- Check what columns exist in the policies table
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'policies'
ORDER BY column_name;