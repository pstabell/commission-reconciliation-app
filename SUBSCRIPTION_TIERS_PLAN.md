# Commission Tracker Pro - Subscription Tiers Plan

## Overview
This document outlines the planned subscription tier structure for Commission Tracker Pro. All users who sign up before tier implementation will be grandfathered as "legacy" users with full access.

## Tier Structure

### 💙 Basic - $19.99/month
**Target User:** Individual agents just starting out
**Value Prop:** Core functionality to track policies and commissions

**Page Access:**
1. ✅ Dashboard
2. ✅ Add New Policy Transaction
3. ✅ Edit Policy Transactions
4. ✅ Search & Filter
5. ❌ All Policy Transactions
6. ❌ Reports
7. ❌ Policy Revenue Ledger
8. ❌ Policy Revenue Ledger Reports
9. ❌ Pending Policy Renewals
10. ❌ Tools
11. ❌ Reconciliation
12. ❌ Admin Panel
13. ❌ Contacts
14. ✅ Help

### 💚 Plus - $29.99/month
**Target User:** Growing agencies needing reporting and bulk operations
**Value Prop:** Full policy management with reporting and import/export

**Page Access:**
1. ✅ Dashboard
2. ✅ Add New Policy Transaction
3. ✅ Edit Policy Transactions
4. ✅ Search & Filter
5. ✅ All Policy Transactions
6. ✅ Reports
7. ✅ Policy Revenue Ledger
8. ✅ Policy Revenue Ledger Reports
9. ✅ Pending Policy Renewals
10. ✅ Tools
11. ❌ Reconciliation
12. ❌ Admin Panel
13. ❌ Contacts
14. ✅ Help

### 💜 Pro - $39.99/month
**Target User:** Established agencies needing full automation
**Value Prop:** Complete commission management with reconciliation automation

**Page Access:**
1. ✅ Dashboard
2. ✅ Add New Policy Transaction
3. ✅ Edit Policy Transactions
4. ✅ Search & Filter
5. ✅ All Policy Transactions
6. ✅ Reports
7. ✅ Policy Revenue Ledger
8. ✅ Policy Revenue Ledger Reports
9. ✅ Pending Policy Renewals
10. ✅ Tools
11. ✅ Reconciliation
12. ✅ Admin Panel
13. ✅ Contacts
14. ✅ Help

## Implementation Plan

### Phase 1: Database Preparation (Current)
- Add `subscription_tier` field to users table
- Add `stripe_price_id` field to track which price they're on
- Set all existing users to `subscription_tier = 'legacy'`

### Phase 2: Stripe Setup (When Ready)
- Create 3 products in Stripe:
  - Basic: $19.99/mo
  - Plus: $29.99/mo
  - Pro: $39.99/mo
- Update webhook handler to capture price_id and set appropriate tier

### Phase 3: Implement Page Gating
- Add tier checking function in commission_app.py
- Update sidebar to only show accessible pages
- Add upgrade prompts for locked pages

### Phase 4: Update UI
- Modify subscription page to show 3 tiers
- Add current tier display in app
- Create upgrade flow for existing users

## Legacy User Handling

All users who sign up before tier implementation will be tagged as "legacy" users:
- They maintain full access at their current $19.99 price point
- Options for migration:
  1. Keep them grandfathered forever (recommended for loyalty)
  2. Offer voluntary upgrade with incentives
  3. Give 6-month notice before migration (least recommended)

## Code Snippets for Implementation

### Database Update
```sql
-- Add tier tracking fields
ALTER TABLE users ADD COLUMN subscription_tier VARCHAR(50) DEFAULT 'legacy';
ALTER TABLE users ADD COLUMN stripe_price_id VARCHAR(100);

-- Update existing users
UPDATE users SET subscription_tier = 'legacy' WHERE subscription_tier IS NULL;
```

### Page Access Function
```python
def check_page_access(page_name: str, user_tier: str) -> bool:
    """Check if user's tier has access to a specific page."""
    
    # Legacy users get full access
    if user_tier == 'legacy':
        return True
    
    tier_pages = {
        'basic': [
            'Dashboard',
            'Add New Policy Transaction',
            'Edit Policy Transactions',
            'Search & Filter',
            'Help'
        ],
        'plus': [
            'Dashboard',
            'Add New Policy Transaction',
            'Edit Policy Transactions',
            'Search & Filter',
            'All Policy Transactions',
            'Reports',
            'Policy Revenue Ledger',
            'Policy Revenue Ledger Reports',
            'Pending Policy Renewals',
            'Tools',
            'Help'
        ],
        'pro': [
            'Dashboard',
            'Add New Policy Transaction',
            'Edit Policy Transactions',
            'Search & Filter',
            'All Policy Transactions',
            'Reports',
            'Policy Revenue Ledger',
            'Policy Revenue Ledger Reports',
            'Pending Policy Renewals',
            'Tools',
            'Reconciliation',
            'Admin Panel',
            'Contacts',
            'Help'
        ]
    }
    
    allowed_pages = tier_pages.get(user_tier, [])
    return page_name in allowed_pages
```

### Sidebar Filtering
```python
# In the sidebar selection
all_pages = [
    "Dashboard",
    "Add New Policy Transaction",
    "Edit Policy Transactions",
    "Search & Filter",
    "All Policy Transactions",
    "Reports",
    "Policy Revenue Ledger",
    "Policy Revenue Ledger Reports",
    "Pending Policy Renewals",
    "Tools",
    "Reconciliation",
    "Admin Panel",
    "Contacts",
    "Help"
]

# Get user's tier from session
user_tier = st.session_state.get('user_tier', 'legacy')

# Filter pages based on access
available_pages = [p for p in all_pages if check_page_access(p, user_tier)]

# Show in sidebar
page = st.sidebar.selectbox("Select Page", available_pages)
```

## Timeline
- **Now**: Add database fields, tag all users as legacy
- **After 50-100 users**: Consider implementing tiers
- **6 months later**: Evaluate tier performance and adjust

## Notes
- Reconciliation is the key differentiator for Pro tier (high value feature)
- Admin Panel access is restricted to Pro (settings that affect billing)
- Tools (import/export) are available in Plus tier to encourage upgrades
- Basic tier has enough functionality to be useful but encourages growth