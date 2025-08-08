# STMT DATE Filtering Analysis - Ensuring STMT Transactions Stay with Their Policies

## Executive Summary

This document analyzes how STMT DATE is used for filtering throughout the Sales Commission App and provides recommendations for ensuring STMT transactions are ALWAYS included with their related policy, regardless of date filters.

## Current STMT Transaction Filtering Locations

### 1. Policy Revenue Ledger (Individual Policy View)
**Location**: `commission_app.py` lines 13300-13474

**Current Behavior**:
- When viewing a specific policy, the system fetches ALL transactions for that policy
- Special handling exists for STMT transactions with missing/different Client IDs
- X-DATE filtering is applied for policy terms
- STMT transactions are included based on:
  - Transaction ID containing "-STMT-"
  - STMT DATE falling within term boundaries (term_eff_date <= stmt_date <= term_x_date)
  - OR if the STMT transaction's Effective Date matches the term's Effective Date

**Key Code**:
```python
# Include STMT/VOID transactions within term
elif "-STMT-" in str(row.get("Transaction ID", "")) or "-VOID-" in str(row.get("Transaction ID", "")):
    # Include if Effective Date falls within term
    if pd.notna(trans_eff_date) and term_eff_date <= trans_eff_date <= term_x_date:
        filtered_rows.append(idx)
```

### 2. Policy Revenue Ledger Reports (Monthly Filtering)
**Location**: `commission_app.py` lines 14600-14701

**Current Behavior**:
- When filtering by month, the system finds NEW/RWL transactions in that month
- For each term, it includes STMT transactions based on:
  - STMT DATE falling within term boundaries
  - OR if the STMT transaction's Effective Date equals the term's Effective Date

**Key Code**:
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

## Issues with Current Implementation

### 1. STMT DATE Dependency
The filtering logic heavily relies on STMT DATE to determine if a STMT transaction belongs to a term. This can cause issues when:
- STMT DATE is missing or incorrect
- STMT DATE falls outside term boundaries (e.g., late payments)
- STMT transactions are imported with dates that don't align with policy terms

### 2. Client ID Mismatches
STMT transactions sometimes have missing or different Client IDs, which can cause them to be excluded from policy groupings.

### 3. Term Boundary Strictness
The current logic strictly enforces term boundaries, which might exclude legitimate STMT transactions that occur after the policy term expires (late payments).

## Recommendations for Ensuring STMT Inclusion

### 1. Primary Association by Policy Number
**Recommendation**: Always include STMT transactions based on Policy Number match first, then apply date filtering as a secondary criterion.

```python
# Proposed logic
if "-STMT-" in trans_id:
    # First, check if Policy Number matches
    if trans_row['Policy Number'] == policy_num:
        # Then check dates, but be more lenient
        stmt_date = pd.to_datetime(trans_row.get('STMT DATE'), errors='coerce')
        eff_date = pd.to_datetime(trans_row.get('Effective Date'), errors='coerce')
        
        # Include if ANY of these conditions are true:
        # 1. STMT DATE within term boundaries
        # 2. Effective Date matches term start
        # 3. Transaction occurred within 90 days after term end (for late payments)
        if (pd.notna(stmt_date) and term_eff_date <= stmt_date <= term_x_date) or \
           (pd.notna(eff_date) and eff_date == term_eff_date) or \
           (pd.notna(stmt_date) and stmt_date <= term_x_date + pd.Timedelta(days=90)):
            include_transaction = True
```

### 2. Enhanced Client ID Handling
**Current Code** (lines 13326-13339) already handles this well:
```python
# ALSO check for STMT transactions that might have missing/different Client IDs
stmt_rows = all_data_trimmed[
    (all_data_trimmed["Policy Number"] == selected_policy.strip()) & 
    (all_data_trimmed["Transaction ID"].astype(str).str.contains("-STMT-", na=False))
]
```

**Recommendation**: Apply this pattern consistently across all filtering locations.

### 3. Add STMT Transaction Reconciliation Flag
**Recommendation**: Add a field to link STMT transactions explicitly to their policy term.

```python
# When importing STMT transactions, add term identification
def link_stmt_to_term(stmt_transaction, all_policies):
    policy_num = stmt_transaction['Policy Number']
    stmt_date = pd.to_datetime(stmt_transaction['STMT DATE'])
    
    # Find the term this STMT belongs to
    policy_terms = all_policies[all_policies['Policy Number'] == policy_num]
    for _, term in policy_terms.iterrows():
        if term['Transaction Type'] in ['NEW', 'RWL']:
            term_start = pd.to_datetime(term['Effective Date'])
            term_end = pd.to_datetime(term['X-DATE'])
            
            # Check if STMT falls within or shortly after term
            if term_start <= stmt_date <= term_end + pd.Timedelta(days=90):
                stmt_transaction['Policy Term Reference'] = term['Transaction ID']
                break
    
    return stmt_transaction
```

### 4. Grace Period for Late Payments
**Recommendation**: Allow a grace period (e.g., 90 days) after term expiration for STMT transactions.

### 5. Fallback Logic
**Recommendation**: Implement a fallback hierarchy for STMT inclusion:
1. Exact term match (STMT DATE within boundaries)
2. Grace period match (STMT DATE within 90 days after term)
3. Policy Number match with reasonable date range
4. Manual override capability

## Implementation Priority

### High Priority Changes
1. **Update Policy Revenue Ledger term filtering** (lines 13443-13459)
   - Add grace period for STMT transactions
   - Ensure Policy Number matching takes precedence

2. **Update Reports monthly filtering** (lines 14661-14667)
   - Apply same grace period logic
   - Add fallback for STMT transactions without dates

### Medium Priority Changes
1. **Add configuration for grace period**
   - Allow administrators to adjust the 90-day grace period
   - Store in config_files/app_settings.json

2. **Enhance STMT import process**
   - Auto-link STMT transactions to their terms during import
   - Add validation warnings for STMT transactions that can't be linked

### Low Priority Changes
1. **Add manual override UI**
   - Allow users to manually assign STMT transactions to terms
   - Add audit trail for manual assignments

## Testing Scenarios

### Test Case 1: Late Payment STMT
- Policy Term: 01/01/2024 - 01/01/2025
- STMT DATE: 02/15/2025 (45 days late)
- **Expected**: STMT should be included with the 2024 term

### Test Case 2: Missing STMT DATE
- Policy Term: 01/01/2024 - 01/01/2025
- STMT DATE: NULL
- Effective Date: 01/01/2024
- **Expected**: STMT should be included based on Effective Date match

### Test Case 3: Different Client ID
- Policy Number: POL123
- Main Client ID: CL001
- STMT Client ID: NULL or different
- **Expected**: STMT should be included based on Policy Number match

### Test Case 4: Cross-Term STMT
- Term 1: 01/01/2024 - 01/01/2025
- Term 2: 01/01/2025 - 01/01/2026
- STMT DATE: 01/15/2025 (could apply to either term)
- **Expected**: STMT should be included with Term 2 (most recent active term)

## Code Locations Summary

1. **Policy Revenue Ledger Individual View**
   - File: `commission_app.py`
   - Lines: 13300-13474
   - Function: Individual policy transaction filtering

2. **Policy Revenue Ledger Reports**
   - File: `commission_app.py`
   - Lines: 14600-14701
   - Function: Monthly statement filtering

3. **STMT Transaction Import**
   - Various locations handle STMT import
   - Should be enhanced to pre-link STMT to terms

## Conclusion

The current STMT DATE filtering is functional but can be improved to ensure STMT transactions are never separated from their policies. The key improvements are:

1. **Policy Number matching as primary criterion**
2. **Grace periods for late payments**
3. **Better handling of missing/incorrect dates**
4. **Explicit term linking during import**

These changes will make the system more robust and user-friendly, ensuring commission tracking remains accurate even with real-world payment timing variations.