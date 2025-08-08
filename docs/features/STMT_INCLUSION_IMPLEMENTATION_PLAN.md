# STMT Transaction Inclusion - Implementation Plan

## Overview
This document provides specific code changes to ensure STMT transactions are always included with their related policies, implementing a grace period and fallback logic.

## Phase 1: Update Policy Revenue Ledger Term Filtering

### Location: `commission_app.py` lines 13443-13459

### Current Code:
```python
# Check for STMT/VOID transactions FIRST (they might have various transaction types)
if "-STMT-" in str(row.get("Transaction ID", "")) or "-VOID-" in str(row.get("Transaction ID", "")):
    # Include if Effective Date falls within term
    if pd.notna(trans_eff_date) and term_eff_date <= trans_eff_date <= term_x_date:
        filtered_rows.append(idx)
```

### Updated Code:
```python
# Check for STMT/VOID transactions FIRST (they might have various transaction types)
if "-STMT-" in str(row.get("Transaction ID", "")) or "-VOID-" in str(row.get("Transaction ID", "")):
    # Get STMT DATE for more accurate filtering
    stmt_date = pd.to_datetime(row.get("STMT DATE"), errors='coerce')
    
    # Define grace period for late payments (90 days after term end)
    grace_period = pd.Timedelta(days=90)
    term_end_with_grace = term_x_date + grace_period if pd.notna(term_x_date) else None
    
    # Include STMT transaction if ANY of these conditions are met:
    include_stmt = False
    
    # 1. STMT DATE within term boundaries (primary check)
    if pd.notna(stmt_date) and pd.notna(term_x_date):
        if term_eff_date <= stmt_date <= term_end_with_grace:
            include_stmt = True
    
    # 2. Effective Date within term (fallback for missing STMT DATE)
    if not include_stmt and pd.notna(trans_eff_date):
        if term_eff_date <= trans_eff_date <= term_x_date:
            include_stmt = True
    
    # 3. Effective Date matches term start (term association)
    if not include_stmt and pd.notna(trans_eff_date):
        if trans_eff_date == term_eff_date:
            include_stmt = True
    
    # 4. If still not included and it's for this policy, include with warning
    if not include_stmt and row.get("Policy Number") == selected_policy.strip():
        # Check if this STMT is orphaned (no clear term association)
        if pd.isna(stmt_date) and pd.isna(trans_eff_date):
            include_stmt = True  # Include orphaned STMT with the term
    
    if include_stmt:
        filtered_rows.append(idx)
```

## Phase 2: Update Reports Monthly Filtering

### Location: `commission_app.py` lines 14661-14675

### Current Code:
```python
# Include STMT/VOID transactions within term
elif '-STMT-' in trans_id or '-VOID-' in trans_id:
    stmt_date = pd.to_datetime(trans_row.get('STMT DATE'), errors='coerce')
    if pd.notna(stmt_date) and term_x_date and term_eff_date <= stmt_date <= term_x_date:
        include_transaction = True
    # Also check if they reference the same term based on effective date
    elif trans_eff_date == term_eff_date:
        include_transaction = True
```

### Updated Code:
```python
# Include STMT/VOID transactions within term (with grace period)
elif '-STMT-' in trans_id or '-VOID-' in trans_id:
    stmt_date = pd.to_datetime(trans_row.get('STMT DATE'), errors='coerce')
    
    # Define grace period for late payments (90 days after term end)
    grace_period = pd.Timedelta(days=90)
    term_end_with_grace = term_x_date + grace_period if pd.notna(term_x_date) else None
    
    # Multiple inclusion criteria for STMT transactions
    include_transaction = False
    
    # 1. STMT DATE within term boundaries OR grace period
    if pd.notna(stmt_date) and pd.notna(term_end_with_grace):
        if term_eff_date <= stmt_date <= term_end_with_grace:
            include_transaction = True
            # Add indicator if it's in grace period
            if pd.notna(term_x_date) and stmt_date > term_x_date:
                # Could add a flag here for UI indication
                pass
    
    # 2. Effective Date matches term start (term association)
    if not include_transaction and pd.notna(trans_eff_date):
        if trans_eff_date == term_eff_date:
            include_transaction = True
    
    # 3. Effective Date within term (fallback)
    if not include_transaction and pd.notna(trans_eff_date) and pd.notna(term_x_date):
        if term_eff_date <= trans_eff_date <= term_x_date:
            include_transaction = True
    
    # 4. Policy Number match with reasonable dates (last resort)
    if not include_transaction and trans_row.get('Policy Number') == policy_num:
        # If STMT has no dates or dates are way off, still include if it's recent
        if pd.isna(stmt_date) or (pd.notna(stmt_date) and stmt_date >= term_eff_date - pd.Timedelta(days=30)):
            include_transaction = True
```

## Phase 3: Add Configuration for Grace Period

### New File: `config_files/stmt_settings.json`
```json
{
    "stmt_grace_period_days": 90,
    "stmt_inclusion_rules": {
        "use_grace_period": true,
        "include_orphaned_stmt": true,
        "pre_term_allowance_days": 30
    },
    "stmt_warnings": {
        "show_grace_period_indicator": true,
        "show_orphaned_stmt_warning": true
    }
}
```

### Add Configuration Loading:
```python
# Add at the top of commission_app.py with other imports
def load_stmt_settings():
    """Load STMT transaction handling settings"""
    settings_file = "config_files/stmt_settings.json"
    default_settings = {
        "stmt_grace_period_days": 90,
        "stmt_inclusion_rules": {
            "use_grace_period": True,
            "include_orphaned_stmt": True,
            "pre_term_allowance_days": 30
        }
    }
    
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r') as f:
                return json.load(f)
        except:
            return default_settings
    return default_settings

# Load settings at startup
STMT_SETTINGS = load_stmt_settings()
GRACE_PERIOD_DAYS = STMT_SETTINGS.get("stmt_grace_period_days", 90)
```

## Phase 4: Enhanced STMT Import Process

### Add Term Linking During Import

```python
def link_stmt_to_policy_term(stmt_transaction, all_policies):
    """
    Link a STMT transaction to its appropriate policy term.
    Returns the transaction with added term reference metadata.
    """
    policy_num = stmt_transaction.get('Policy Number')
    stmt_date = pd.to_datetime(stmt_transaction.get('STMT DATE'), errors='coerce')
    eff_date = pd.to_datetime(stmt_transaction.get('Effective Date'), errors='coerce')
    
    # Find all terms for this policy
    policy_terms = all_policies[
        (all_policies['Policy Number'] == policy_num) & 
        (all_policies['Transaction Type'].isin(['NEW', 'RWL']))
    ].sort_values('Effective Date')
    
    if policy_terms.empty:
        return stmt_transaction
    
    # Try to find the best matching term
    best_match = None
    match_quality = 0  # 0 = no match, 1 = grace period, 2 = within term, 3 = exact match
    
    for _, term in policy_terms.iterrows():
        term_start = pd.to_datetime(term['Effective Date'])
        term_end = pd.to_datetime(term['X-DATE'])
        grace_period = pd.Timedelta(days=GRACE_PERIOD_DAYS)
        
        # Check STMT DATE first (most reliable)
        if pd.notna(stmt_date) and pd.notna(term_end):
            if term_start <= stmt_date <= term_end:
                best_match = term
                match_quality = 3
                break  # Perfect match
            elif term_start <= stmt_date <= term_end + grace_period:
                if match_quality < 2:
                    best_match = term
                    match_quality = 2
        
        # Check Effective Date as fallback
        if pd.notna(eff_date) and match_quality < 3:
            if eff_date == term_start:
                best_match = term
                match_quality = 3
                break  # Perfect match
            elif pd.notna(term_end) and term_start <= eff_date <= term_end:
                if match_quality < 2:
                    best_match = term
                    match_quality = 2
    
    # If no match found, link to most recent term
    if best_match is None and not policy_terms.empty:
        best_match = policy_terms.iloc[-1]  # Most recent term
        match_quality = 1
    
    # Add metadata about the term link
    if best_match is not None:
        stmt_transaction['Linked_Term_ID'] = best_match['Transaction ID']
        stmt_transaction['Linked_Term_Start'] = best_match['Effective Date']
        stmt_transaction['Link_Quality'] = match_quality
    
    return stmt_transaction
```

## Phase 5: Add UI Indicators

### Add Visual Indicators for STMT Status

```python
# In the Type indicator function (around line 13514)
def get_ledger_type_symbol(row_index):
    trans_id = str(policy_rows.iloc[row_index][transaction_id_col])
    trans_type = str(policy_rows.iloc[row_index][transaction_type_col]) if transaction_type_col in policy_rows.columns else ""
    
    # Check Transaction ID patterns first
    if "-STMT-" in trans_id:
        # Check if this STMT is in grace period
        stmt_date = pd.to_datetime(policy_rows.iloc[row_index].get('STMT DATE'), errors='coerce')
        x_date = pd.to_datetime(policy_rows.iloc[row_index].get('X-DATE'), errors='coerce')
        
        if pd.notna(stmt_date) and pd.notna(x_date) and stmt_date > x_date:
            return "💰⏰ STMT"  # Late payment indicator
        else:
            return "💰 STMT"
    elif "-VOID-" in trans_id:
        return "🔴 VOID"
    # ... rest of the function
```

## Testing Checklist

### Test Scenario 1: Normal STMT within term
- [ ] Create policy with term 01/01/2024 - 12/31/2024
- [ ] Add STMT with STMT DATE 06/15/2024
- [ ] Verify STMT appears in Policy Revenue Ledger
- [ ] Verify STMT appears in June 2024 monthly report

### Test Scenario 2: Late payment STMT
- [ ] Create policy with term 01/01/2024 - 12/31/2024
- [ ] Add STMT with STMT DATE 02/15/2025 (46 days late)
- [ ] Verify STMT appears in Policy Revenue Ledger
- [ ] Verify STMT appears with late payment indicator

### Test Scenario 3: STMT with missing dates
- [ ] Create policy with term 01/01/2024 - 12/31/2024
- [ ] Add STMT with NULL STMT DATE but Effective Date 01/01/2024
- [ ] Verify STMT appears based on Effective Date match

### Test Scenario 4: Orphaned STMT
- [ ] Add STMT with only Policy Number (no dates)
- [ ] Verify STMT appears with warning indicator
- [ ] Verify STMT is linked to most recent term

## Rollback Plan

If issues arise, the changes can be rolled back by:
1. Reverting the grace period logic to strict date boundaries
2. Removing the fallback inclusion rules
3. Restoring original filtering code from backup

## Performance Considerations

- The additional date checks add minimal overhead
- Grace period calculations are simple date arithmetic
- Policy Number matching already exists in current code
- No additional database queries required

## Next Steps

1. Implement Phase 1 changes and test
2. Deploy to test environment
3. Gather user feedback on grace period duration
4. Implement remaining phases based on feedback
5. Update user documentation