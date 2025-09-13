# Mobile Data Visibility Issue - January 2025

## Issue Description
Demo user sees 430 records on desktop but 0 records on mobile device.

## Debug Steps Added

### 1. Enhanced Dashboard Debug Info
- Direct database count check
- Sample transaction IDs display
- Mobile device detection
- Session persistence tracking
- Page load counter
- Session creation timestamp

### 2. Enhanced load_policies_data() Logging
- Comprehensive debug info on each call
- Session state inspection
- Case-insensitive email fallback
- Record count logging

### 3. Authentication Flow Debug
- Login success logging
- Session state inspection after auth
- Fallback auth logging

## SQL Debug Script
Run `/sql_scripts/debug_mobile_demo_issue.sql` to verify:
- Exact email matches
- Case variations
- RLS policy status
- What anon role can see
- Recent data changes

## Possible Causes

### 1. Session State Not Persisting
Mobile browsers may handle session state differently. Check:
- Page loads counter increasing
- Session created timestamp consistency
- Auth keys present in session

### 2. Case Sensitivity
Email might be stored differently. The code now:
- Tries exact match first
- Falls back to case-insensitive search
- Logs both attempts

### 3. RLS Policy Issues
Check if mobile uses different auth context:
- Verify anon key is being used
- Check RLS policies allow anon role
- Verify user_email filter is applied

### 4. Browser/Cookie Issues
Mobile browsers may:
- Block cookies
- Clear session on tab switch
- Have different security settings

## Next Steps

1. **Deploy & Test**: Have user check mobile debug info
2. **Check Logs**: Review console logs for debug output
3. **Verify Data**: Run SQL script to confirm data exists
4. **Session Test**: Check if session persists across page loads
5. **Browser Test**: Try different mobile browsers

## Resolution Tracking
- Issue reported: January 13, 2025
- Debug code added: January 13, 2025
- Status: Pending user testing with debug info