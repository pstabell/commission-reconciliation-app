# Troubleshooting: Contacts Data Visibility Issues
**Last Updated**: January 19, 2025

## Common Issues and Solutions

### Issue 1: "No carriers found" Despite Data in Database

**Symptoms**:
- Contacts page shows "No carriers found. Use Quick Add to create your first carrier."
- Database queries confirm carriers exist with correct user_email
- Happens particularly with demo account

**Common Causes**:

1. **Search Mode Active**
   - Check if search box has any text (even spaces)
   - Search mode filters all results if no matches found
   - Solution: Clear search box completely

2. **Email Case Sensitivity**
   - Demo user: Must be `Demo@AgentCommissionTracker.com` (exact case)
   - App uses `get_normalized_user_email()` to handle this
   - Login email doesn't matter, but database must have exact case

3. **Session State Caching**
   - Old data cached in session
   - Solution: Logout completely and login again

**Debug Steps**:
```python
# Add to commission_app.py temporarily for demo user
if st.session_state.get('user_email', '').lower().startswith('demo'):
    st.info(f"Debug: Found {len(carriers_data)} carriers")
```

### Issue 2: Wrong Carriers/MGAs in Account

**Symptoms**:
- Seeing generic carriers (State Farm, Allstate) instead of your actual carriers
- Missing specific carriers like Burlington
- MGA count doesn't match expected

**Cause**: 
- Wrong data imported during setup
- Generic carrier list used instead of user's actual data

**Solution**:
1. Use Tools → Contacts Import/Export → Export to backup current data
2. In "Replace all" mode, import correct data
3. Verify counts match expected

### Issue 3: Data Visible in UI but Not in Queries

**Symptoms**:
- Can see carrier/MGA in Contacts page
- SQL queries don't find the same data
- Export missing some items

**Possible Causes**:
- Data linked through commission rules without MGA table entry
- Display logic showing derived data
- Orphaned relationships

**Solution**:
- Use new Contacts Import/Export feature
- Export what you can see in UI
- Re-import to clean database

## Quick Fixes

### Enable Debug Mode for Demo User
Add after line 13340 in commission_app.py:
```python
if 'user_email' in st.session_state and st.session_state['user_email'].lower().startswith('demo'):
    st.info(f"🔍 Debug Mode - User: {st.session_state['user_email']}")
```

### Check Data Isolation
```sql
-- Run in Supabase SQL Editor
SELECT DISTINCT user_email, COUNT(*) as count
FROM carriers
GROUP BY user_email
ORDER BY count DESC;
```

### Verify RLS is Disabled
```sql
-- Check RLS status
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('carriers', 'mgas', 'commission_rules');

-- If enabled, disable it
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;
ALTER TABLE commission_rules DISABLE ROW LEVEL SECURITY;
```

## Prevention

1. **Regular Backups**: Use Contacts Import/Export to backup your data
2. **Verify After Import**: Always check counts and spot-check specific items
3. **Clear Browser State**: If issues persist, try incognito mode
4. **Check Environment**: Ensure APP_ENVIRONMENT=PRODUCTION in .env file

## Related Documentation
- [User Isolation and Security Model](../fortification-plan-2025.md)
- [Demo Account Setup](../changelogs/2025-01-18-demo-user-contacts-import.md)
- [Missing Carriers/MGAs Issue](./MISSING_CARRIERS_MGAS_2025.md)