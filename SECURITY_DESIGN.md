# 🔐 Security Design & Management Guide

**Created**: July 4, 2025  
**Purpose**: Security implementation guide and password management procedures

## 🏗️ Current Security Architecture

### Application-Level Security
- **Password Protection**: Single password for all users
- **Session Management**: Password persists across pages until logout
- **Environment Variables**: Credentials stored in `.env` (local) and Secrets (cloud)

### Credential Storage Locations

#### Local Development (.env file)
```
APP_PASSWORD=YourPasswordHere
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

#### Streamlit Cloud (Secrets)
- Access via: App Settings → Secrets
- Format: TOML (no quotes around keys)
- Updates take effect immediately

## 🔄 How to Change Passwords

### Step 1: Update Local Password
1. Edit `.env` file
2. Change only the value after `APP_PASSWORD=`
3. **Remove any example comments** - only one APP_PASSWORD line should exist
4. Save the file

### Step 2: Restart Local App
```bash
# Stop app (Ctrl+C)
# Start app again
streamlit run commission_app.py
```
**Important**: Environment variables load at startup - MUST restart!

### Step 3: Update Live App Password
1. Go to https://share.streamlit.io/
2. Find your app → Click "..." → Settings
3. Go to Secrets section
4. Update the APP_PASSWORD value
5. Click Save (app auto-restarts)

### Step 4: Test Both Environments
- Local: http://localhost:8501
- Live: Your Streamlit Cloud URL

## ⚠️ Security Best Practices

### DO:
✅ Use strong passwords (14+ characters, mixed case, numbers, symbols)  
✅ Change passwords regularly (monthly recommended)  
✅ Keep `.env` in `.gitignore` (never commit passwords)  
✅ Use different passwords for different environments  
✅ Test password changes immediately  

### DON'T:
❌ Share passwords in chat or email  
❌ Commit `.env` files to Git  
❌ Use example/default passwords in production  
❌ Leave debug password displays in code  
❌ Store passwords in plain text files  

## 🚨 If Credentials Are Exposed

### For App Password:
1. Change password immediately in both `.env` and Streamlit Cloud
2. Restart local app
3. Verify no unauthorized access occurred

### For Supabase Keys:
1. Log into Supabase Dashboard
2. Settings → API → Regenerate keys
3. Update `.env` file with new keys
4. Update Streamlit Cloud Secrets
5. Restart all environments

## 🔍 Troubleshooting Password Issues

### "Password not working" - Local App
1. Check `.env` has only ONE `APP_PASSWORD=` line
2. Remove any duplicate entries or comments
3. Restart the app (Ctrl+C then run again)
4. Clear Streamlit cache: `streamlit cache clear`

### "Password not working" - Live App
1. Verify Secrets format in Streamlit Cloud (TOML format)
2. Check for typos or extra spaces
3. Wait 30 seconds for changes to propagate
4. Hard refresh browser (Ctrl+F5)

### Debug Mode (Temporary)
Add to code to see what password app expects:
```python
st.write(f"DEBUG: Password starts with: {correct_password[:3]}")
```
**Remember to remove after debugging!**

## 📋 Quick Reference

| Environment | Password Location | Format | Restart Required |
|-------------|------------------|--------|------------------|
| Local | `.env` file | `APP_PASSWORD=value` | Yes - always |
| Streamlit Cloud | Settings → Secrets | TOML format | No - automatic |

## 🔮 Future Security Enhancements

### Phase 2 Considerations:
- Multi-user authentication with individual accounts
- Role-based access control (admin vs viewer)
- Password complexity requirements
- Password change enforcement
- Login attempt limiting
- Two-factor authentication

### Database Security:
- Row Level Security (RLS) - ready but not enabled
- API key rotation schedule
- Encrypted connections only

---

**Remember**: Security is only as strong as your weakest password. Change them regularly!