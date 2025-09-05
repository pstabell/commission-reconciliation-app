-- Add subscription tier tracking to users table
-- Run this in your production Supabase SQL editor

-- Add tier and price_id columns
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS subscription_tier VARCHAR(50) DEFAULT 'legacy',
ADD COLUMN IF NOT EXISTS stripe_price_id VARCHAR(100);

-- Update all existing users to legacy tier
UPDATE users 
SET subscription_tier = 'legacy' 
WHERE subscription_tier IS NULL;

-- Add comment for documentation
COMMENT ON COLUMN users.subscription_tier IS 'User subscription tier: legacy, basic, plus, or pro';
COMMENT ON COLUMN users.stripe_price_id IS 'Stripe price ID to track exact subscription';

-- Create index for faster tier lookups
CREATE INDEX IF NOT EXISTS idx_users_subscription_tier ON users(subscription_tier);

-- Verify the changes
SELECT 
    email,
    subscription_status,
    subscription_tier,
    stripe_price_id,
    created_at
FROM users
ORDER BY created_at DESC;