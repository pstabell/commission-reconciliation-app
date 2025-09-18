# Demo User MGA Visibility Fix

**Date:** January 18, 2025
**Issue:** Demo user sees "No MGAs found" despite having 16 MGAs in database
**Status:** RESOLVED

## Problem Description

The demo user was unable to see any MGAs (Managing General Agencies) in the Contacts page, showing "No MGAs found" message despite having 16 MGAs in the database.

## Root Cause

The issue was caused by inconsistent case sensitivity handling for the demo user's email address:

1. **Database Storage**: MGAs are stored with user_email = `'Demo@AgentCommissionTracker.com'` (capital D and camel case)
2. **Session State**: User might log in with different case variations (e.g., `'demo@agentcommissiontracker.com'`)
3. **Special Case Handling**: The policies loading function had case correction logic, but MGA/carrier loading did not

The queries for MGAs, carriers, and commission rules were using `st.session_state['user_email']` directly without normalizing the case for the demo user, causing the database queries to return no results.

## Solution Implemented

1. **Created a centralized function** `get_normalized_user_email()` that:
   - Returns the user's email from session state
   - Applies case correction for demo user (always returns `'Demo@AgentCommissionTracker.com'`)
   
2. **Updated all database queries** that filter by user_email to use this normalized function:
   - Carriers loading query
   - MGAs loading query  
   - Commission rules loading query
   - Carrier-MGA relationships query
   - Deleted policies query
   - Various other user-filtered queries

3. **Updated `add_user_email_to_data()`** helper function to use normalized email

## Code Changes

### New Function Added:
```python
def get_normalized_user_email():
    """Get the current user's email with proper case handling for demo user."""
    if "user_email" not in st.session_state:
        return None
    
    user_email = st.session_state['user_email']
    # Special handling for Demo user case sensitivity
    if user_email.lower() == 'demo@agentcommissiontracker.com':
        return 'Demo@AgentCommissionTracker.com'
    return user_email
```

### Query Pattern Updated:
Before:
```python
response = supabase.table('mgas').select("*").eq('user_email', st.session_state['user_email']).execute()
```

After:
```python
user_email = get_normalized_user_email()
response = supabase.table('mgas').select("*").eq('user_email', user_email).execute()
```

## Files Modified

- `/commission_app.py` - Added `get_normalized_user_email()` function and updated all user_email queries

## Testing Instructions

1. Log in as demo user (any case variation of demo@agentcommissiontracker.com)
2. Navigate to Admin Panel > Contacts
3. Verify that:
   - Carriers are displayed in "Recent Carriers" section
   - MGAs are displayed in "Recent MGAs" section
   - Commission rules are visible when viewing carriers/MGAs
   - All filtering and searching works correctly

## Prevention

To prevent similar issues:

1. **Consistent Case Handling**: Always normalize user emails when querying the database
2. **Centralized Functions**: Use helper functions for common operations like getting user email
3. **Database Constraints**: Consider adding database-level case-insensitive unique constraints
4. **Testing**: Test with various case combinations of user emails

## Related Issues

- Similar case sensitivity issues may exist in other parts of the application
- Consider implementing case-insensitive email handling at the authentication level
- May want to add database triggers to ensure consistent case storage