# Debugging Webhook to Supabase Issues

## The Problem
Stripe events are successful but no users are being created in Supabase.

## Steps to Check Render Webhook Logs

1. **Go to your Render Dashboard**
   - Navigate to https://dashboard.render.com
   - Click on your webhook service

2. **Check the Logs Tab**
   - Look for recent webhook executions around 11:25pm
   - Search for these key phrases:
     - "WEBHOOK TRIGGERED"
     - "Creating new user"
     - "Database error"
     - "Error setting up password flow"

3. **Common Issues to Look For**

   a) **RLS (Row Level Security) Error**:
   ```
   Error: new row violates row-level security policy
   ```
   **Solution**: Run this SQL in Supabase:
   ```sql
   -- Disable RLS on password_reset_tokens table
   ALTER TABLE password_reset_tokens DISABLE ROW LEVEL SECURITY;
   ```

   b) **Missing Environment Variables**:
   ```
   Warning: Supabase credentials not configured
   ```
   **Solution**: Check these variables in Render:
   - `PRODUCTION_SUPABASE_URL`
   - `PRODUCTION_SUPABASE_ANON_KEY`

   c) **Table Not Found**:
   ```
   Error: relation "password_reset_tokens" does not exist
   ```
   **Solution**: The table needs to be created (see SQL below)

## Quick Fixes

### 1. Create Missing Table (if needed)
Run this in Supabase SQL Editor:
```sql
-- Create password_reset_tokens table if it doesn't exist
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Disable RLS for MVP
ALTER TABLE password_reset_tokens DISABLE ROW LEVEL SECURITY;
```

### 2. Verify Environment Variables
In Render, ensure these are set:
- `PRODUCTION_SUPABASE_URL`: Your Supabase project URL
- `PRODUCTION_SUPABASE_ANON_KEY`: Your Supabase anon key
- `STRIPE_WEBHOOK_SECRET`: Your webhook signing secret

### 3. Test Webhook Manually
After fixing, trigger a test event in Stripe:
1. Go to Stripe Dashboard > Webhooks
2. Click your webhook endpoint
3. Click "Send test webhook"
4. Select "checkout.session.completed"
5. Send test

## What Should Happen
When working correctly, you'll see in Render logs:
1. "WEBHOOK TRIGGERED"
2. "Creating new user..."
3. "Setup token stored for [email]"
4. "Password setup email sent successfully!"

And in Supabase:
- New row in `users` table
- New row in `password_reset_tokens` table