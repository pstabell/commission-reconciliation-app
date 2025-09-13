-- Check all current policies
SELECT 
    policyname,
    cmd,
    qual as using_clause,
    with_check
FROM pg_policies
WHERE tablename = 'policies'
ORDER BY cmd;

-- Make sure UPDATE policy prevents changing user_email
DROP POLICY IF EXISTS "Users can update own policies" ON policies;
CREATE POLICY "Users can update own policies" 
ON policies 
FOR UPDATE 
USING (user_email = auth.email())  -- Can only update if you own it
WITH CHECK (
    user_email = auth.email() AND  -- Still yours after update
    user_email = OLD.user_email     -- Can't change the user_email field!
);

-- Make sure DELETE only works on your own records
DROP POLICY IF EXISTS "Users can delete own policies" ON policies;
CREATE POLICY "Users can delete own policies" 
ON policies 
FOR DELETE 
USING (user_email = auth.email());

-- The complete secure setup:
-- INSERT: Must have user_email (app provides it)
-- SELECT: Only see your own data  
-- UPDATE: Only your own data, can't change user_email
-- DELETE: Only your own data