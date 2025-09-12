# Stripe 100% Off Coupon Issue

## Problem
When using a 100% off coupon, Stripe still requires a payment method to be set up for future charges. If the payment method setup fails, the subscription is not created.

## What Happened
1. Customer "Demo@AgentCommissionTracker.com" was created in Stripe
2. INTERNAL-DEMO-TEST coupon (100% off) was applied
3. SetupIntent was created to collect payment method
4. Payment method setup **failed** twice
5. No subscription was created
6. No webhook was triggered (checkout.session.completed never fired)
7. No user was created in Supabase

## Solutions

### Option 1: Allow Checkout Without Payment Method (Recommended for 100% off)
Add `payment_method_collection: 'if_required'` to checkout session:

```python
checkout_session = stripe.checkout.Session.create(
    line_items=[{
        'price': os.getenv("STRIPE_PRICE_ID"),
        'quantity': 1,
    }],
    mode='subscription',
    customer_email=email,
    subscription_data={
        'trial_period_days': 14,
    },
    payment_method_collection='if_required',  # Only collect if needed
    allow_promotion_codes=True,
    success_url=os.getenv("RENDER_APP_URL") + "/?session_id={CHECKOUT_SESSION_ID}",
    cancel_url=os.getenv("RENDER_APP_URL"),
)
```

### Option 2: Create User on Customer Creation
Handle the `customer.created` webhook event to create users immediately when they start checkout.

### Option 3: Manual User Creation
For demo/internal users, manually create them in Supabase:

```sql
INSERT INTO users (email, subscription_status, subscription_tier, created_at)
VALUES ('demo@agentcommissiontracker.com', 'active', 'legacy', NOW());
```

## Recommendation
Implement Option 1 to allow 100% off coupons to complete without payment method, which is common for internal/demo accounts.