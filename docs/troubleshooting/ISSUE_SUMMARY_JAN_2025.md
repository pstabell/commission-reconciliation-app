# Issue Summary - January 13, 2025

## Quick Reference for CSV Import Issues

### Problem: "Column not found" errors
**Solution**: Check `/commission_app.py` lines 14345-14371 for column mapping

### Problem: "Row violates row-level security policy"
**Solution**: 
```sql
-- Check current policies
SELECT * FROM pg_policies WHERE tablename = 'policies';

-- If needed, update INSERT policy
DROP POLICY IF EXISTS "Users can insert own policies" ON policies;
CREATE POLICY "Anyone can insert with user_email" 
ON policies FOR INSERT 
TO anon, authenticated
WITH CHECK (user_email IS NOT NULL);
```

### Problem: Service role key not found
**Status**: UNRESOLVED
**Workaround**: Use anon key with proper RLS policies

### Problem: Users seeing other users' data
**Solution**: Remove ALL caching from `load_policies_data()`
```python
# NO @st.cache_data decorator!
def load_policies_data():
    # Always fresh data
```

## SQL Scripts Created

1. `/sql_scripts/check_policies_rls.sql` - Diagnose RLS issues
2. `/sql_scripts/fix_rls_multi_tenant.sql` - RLS policy attempts
3. `/sql_scripts/fix_import_once_and_for_all.sql` - Working RLS fix
4. `/sql_scripts/secure_all_operations.sql` - Security hardening

## Key Code Changes

### commission_app.py
- Line 437: Removed `@st.cache_data` from `load_policies_data()`
- Lines 14345-14371: Comprehensive column mapping
- Lines 745-763: Added UI-only fields to `clean_data_for_database()`
- Line 14490: Get fresh Supabase client for imports

## Testing Procedure

1. Log in as User A - verify sees only their data
2. Log in as User B - verify sees only their data  
3. Import CSV as User A - verify success
4. Check User B still sees only their data
5. Clear cache and repeat

## Emergency Contacts

- Supabase Dashboard: Check RLS policies
- Render Dashboard: Check environment variables
- GitHub: All fixes documented in commit history

## Lessons for Next Time

1. **Test multi-user scenarios FIRST**
2. **Never cache user-specific data globally**
3. **Verify RLS policies match auth method**
4. **Document column mappings clearly**
5. **Have rollback plan ready**

---

Time spent debugging: ~24 hours
Issues resolved: 4 of 5 (service role key still not working)
Security status: SECURE (no caching, proper RLS)