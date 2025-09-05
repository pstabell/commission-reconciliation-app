# X-DATE Reports Fix Rollback Plan

## Backup Created
- **Backup File**: `commission_app_20250808_192000_BEFORE_XDATE_REPORTS_FIX.py`
- **Date**: August 8, 2025 @ 7:20 PM

## Changes Being Made
Fixing X-DATE boundary comparisons in Policy Revenue Ledger Reports to match the individual Policy Revenue Ledger page.

### Exact Changes:
1. **Line 14688**: Change `<= term_x_date` to `< term_x_date`
   - Context: END transactions within term dates
   
2. **Line 14694**: Change `<= term_x_date` to `< term_x_date`
   - Context: STMT/VOID transactions within term
   
3. **Line 14698**: Change `<= term_x_date` to `< term_x_date`
   - Context: Other transactions (CAN, PMT, etc.) within term dates

## Rollback Instructions
If this fix causes any issues, restore the backup:
```bash
cp commission_app_20250808_192000_BEFORE_XDATE_REPORTS_FIX.py commission_app.py
```

## Expected Result
Transactions with Effective Date = X-DATE will become orphans and NOT appear in the expiring term's report.