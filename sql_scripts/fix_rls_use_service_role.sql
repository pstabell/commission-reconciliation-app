-- IMMEDIATE FIX: Re-enable RLS to protect user data
ALTER TABLE policies ENABLE ROW LEVEL SECURITY;

-- The app should use the service role key to bypass RLS
-- This way the app can control access through its own authentication
-- Each user only sees data where user_email matches their session

-- First, check if service role policy exists
SELECT * FROM pg_policies 
WHERE tablename = 'policies' 
AND policyname = 'Service role has full access to policies';

-- The service role key bypasses ALL RLS policies
-- So we just need to make sure the app is using it

-- For now, as an emergency fix, create policies that enforce user_email matching
-- But these will only work if we're NOT using the service role key

-- Allow users to see only their own data based on user_email column
CREATE POLICY "Users can only see own data" 
ON policies FOR SELECT 
USING (user_email = current_setting('app.current_user_email', true));

-- But wait, this won't work because we're not setting app.current_user_email

-- The real fix is to ensure the app uses the service role key
-- Then filter data in the application layer based on st.session_state['user_email']