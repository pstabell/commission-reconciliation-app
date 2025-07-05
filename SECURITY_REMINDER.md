# 🔐 Security Best Practices & Daily Reminder

**Created**: July 4, 2025  
**Purpose**: Daily security reminder for working with AI assistants

## ⚠️ CRITICAL SECURITY REMINDERS

### 1. Never Display Sensitive Files in Chat
**AVOID READING THESE FILES:**
- `.env` - Contains passwords and API keys
- `config.json` with credentials
- Any file with passwords, tokens, or keys
- Database connection strings
- Private certificates

**INSTEAD:**
- Use `.env.example` with placeholder values
- Describe what you need without showing secrets
- Say "my .env file has..." rather than displaying it

### 2. Treat AI Chats as Semi-Public
- Conversations may be reviewed for quality/safety
- Not end-to-end encrypted like Signal/WhatsApp
- Similar privacy level to email - secure but not private

### 3. Immediate Actions if Credentials Exposed
1. **Regenerate all exposed API keys**
2. **Change all exposed passwords**
3. **Update production environments**
4. **Check for unauthorized access**

## 🛡️ Safe Practices

### DO:
✅ Create `.example` files for configuration discussions  
✅ Use placeholders like `YOUR_API_KEY_HERE`  
✅ Discuss structure without showing values  
✅ Keep credentials in password managers  
✅ Use environment variables for secrets  

### DON'T:
❌ Use Read tool on `.env` files  
❌ Copy/paste credentials into chat  
❌ Share production passwords  
❌ Display API keys or tokens  
❌ Show database URLs with passwords  

## 📅 Daily Checklist

When starting a coding session:
- [ ] Check if any credentials need rotating
- [ ] Ensure `.env` is in `.gitignore`
- [ ] Use `.env.example` for discussions
- [ ] Never display actual secrets

## 🔄 Credential Rotation Schedule

Consider rotating credentials:
- **Monthly**: Application passwords
- **Quarterly**: API keys
- **Immediately**: Any exposed credentials

## 💡 Remember

> "The best secret is one that's never shared. The second best is one that's immediately changed after sharing."

---

**Note to AI Assistant**: Please remind the user of these security practices at the start of each new day's conversation or when security-sensitive operations are about to be performed.