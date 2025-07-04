# ⚠️ Troubleshooting Guide

## 🚨 Common Issues & Solutions

### Data Not Appearing

**Problem**: Added data doesn't show up in reports or dashboard

**Solutions**:
1. **Refresh the page** - Use browser refresh (F5 or Ctrl+R)
2. **Check column mapping** - Go to Admin Panel to verify column mapping
3. **Verify data entry** - Return to "All Policies in Database" to confirm data was saved
4. **Clear browser cache** - Restart browser if issues persist

**Prevention**: Always click save buttons and wait for confirmation messages

---

### Calculation Errors

**Problem**: Commission calculations seem incorrect

**Solutions**:
1. **Check Transaction Type** - Verify correct type (NEW=50%, RWL=25%, etc.)
2. **Verify Percentages** - Ensure commission percentages are entered correctly
3. **Review Formula** - Check Help → Formulas tab for calculation logic
4. **Recalculate** - Use "Edit Policies" save function to trigger recalculation

**Prevention**: Always double-check transaction types and percentage fields

---

### File Upload Issues

**Problem**: Cannot upload or import files

**Solutions**:
1. **Check File Format** - Use .xlsx, .csv, or .pdf files only
2. **File Size** - Ensure file is under 200MB
3. **Column Headers** - Verify headers match expected format
4. **File Permissions** - Ensure file isn't open in another program

**Prevention**: Keep import files in standard formats with clear headers

---

### Search Not Working

**Problem**: Search/filter returns no results

**Solutions**:
1. **Check Spelling** - Verify search terms are spelled correctly
2. **Try Partial Search** - Use partial names or numbers
3. **Clear Filters** - Reset all filters and try again
4. **Check Column Selection** - Ensure searching in the correct column

**Prevention**: Use consistent data entry practices

---

### Performance Issues

**Problem**: App runs slowly or freezes

**Solutions**:
1. **Reduce Data Size** - Use pagination or filters to limit displayed data
2. **Close Other Tabs** - Free up browser memory
3. **Restart Browser** - Clear memory and start fresh
4. **Check Internet** - Ensure stable connection

**Prevention**: Use filters and pagination for large datasets

## 🔧 Error Messages

### "Column not found" Error

**Cause**: Database column names don't match app expectations

**Solution**: 
1. Go to Admin Panel
2. Review column mapping
3. Map database columns to app functions
4. Save mapping configuration

### "Permission denied" Error

**Cause**: File access or database write issues

**Solution**:
1. Close any Excel files with the same name
2. Check file permissions on the database folder
3. Run as administrator if necessary
4. Contact system administrator

### "Invalid date format" Error

**Cause**: Date entered in wrong format

**Solution**:
1. Use MM/DD/YYYY format only
2. Check for typos in date fields
3. Use date picker when available
4. Clear field and re-enter if needed

## 🆘 Emergency Recovery

### Data Loss Recovery

**If data appears to be lost**:
1. **Don't panic** - Data is likely recoverable
2. **Go to Admin Panel** → Database Recovery Center
3. **Check available backups** - System creates automatic backups
4. **Restore from backup** - Select most recent backup before issue
5. **Contact support** if backups don't resolve the issue

### Database Corruption

**If database won't open**:
1. **Use Admin Panel** → Enhanced Backup System
2. **Try multiple backup files** - Start with most recent
3. **Check backup log** - Review when backups were created
4. **Restore step-by-step** - Test each backup file

### App Won't Start

**If application doesn't load**:
1. **Check browser compatibility** - Use Chrome, Firefox, or Edge
2. **Clear browser cache** - Delete temporary files
3. **Disable browser extensions** - Test in incognito/private mode
4. **Try different browser** - Rule out browser-specific issues

## 📞 Getting Additional Help

### Self-Help Resources
1. **Debug Checkbox** - Enable in sidebar for technical details
2. **Error Messages** - Screenshot and note exact text
3. **Browser Console** - Press F12 → Console tab for error details
4. **Backup Files** - Check what backup files are available

### Contacting Support

**Before contacting support, gather**:
- Exact error message or description of issue
- Steps that led to the problem
- Browser type and version
- Screenshot of the issue
- Recent changes made to data or settings

**Information to provide**:
- What you were trying to do
- What happened instead
- Any error messages displayed
- Whether issue is consistent or intermittent

### Preventive Measures

**Daily**:
- Save work frequently
- Check for confirmation messages
- Use consistent data entry practices

**Weekly**:
- Create manual backup
- Review data for accuracy
- Check available disk space

**Monthly**:
- Review column mapping
- Clean up test data
- Update browser if needed