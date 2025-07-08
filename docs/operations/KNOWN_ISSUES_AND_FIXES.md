# Known Issues and Fixes - Consolidated
**Last Updated**: July 7, 2025  
**Purpose**: Central repository for all technical issues, bugs, and their resolutions

## Table of Contents
1. [Critical Issues (Resolved)](#critical-issues-resolved)
2. [Database Issues](#database-issues)
3. [UI/UX Issues](#uiux-issues)
4. [Reconciliation Issues](#reconciliation-issues)
5. [Terminal & Environment Issues](#terminal--environment-issues)
6. [Minor Issues](#minor-issues)
7. [Pending Issues](#pending-issues)

---

## Critical Issues (Resolved)

### 1. Phase 0 Reconciliation Protection Bug
**Date**: July 6, 2025  
**Severity**: CRITICAL  
**Status**: ✅ RESOLVED

**Issue**: Reconciliation transactions (-STMT-, -VOID-, -ADJ-) were editable in Edit Policies page
**Root Cause**: Column detection failed for "Transaction ID" (with space)
**Solution**: Implemented three-method column detection:
1. Column mapper lookup
2. Common variations check
3. Flexible normalized search

**Code Fix** (commission_app.py lines 2114-2136):
```python
# Method 1: Try using column mapper
transaction_id_col = get_mapped_column("Transaction ID")

# Method 2: Check common variations
if not transaction_id_col:
    possible_names = ["Transaction ID", "Transaction_ID", "TransactionID", ...]
    
# Method 3: Flexible search
if not transaction_id_col:
    for col in columns:
        if col.lower().replace(" ", "").replace("_", "") == "transactionid":
            transaction_id_col = col
```

### 2. NaN Error in Database Updates
**Date**: July 6, 2025  
**Severity**: HIGH  
**Status**: ✅ RESOLVED

**Issue**: "Out of range float values are not JSON compliant: nan"
**Root Cause**: NaN values in update dictionary
**Solution**: Added NaN validation before database updates
```python
if pd.isna(value):
    update_dict[field] = None
elif isinstance(value, float) and (value == float('inf') or value == float('-inf')):
    update_dict[field] = None
```

### 3. Transaction ID Format Issues
**Date**: June 2024  
**Severity**: HIGH  
**Status**: ✅ RESOLVED

**Issue**: Duplicate and improperly formatted transaction IDs
**Problems**:
- Some IDs had double prefixes (e.g., "MNL-MNL-...")
- Missing transaction IDs
- Format inconsistencies

**Solution**: Comprehensive data cleanup and validation
- Fixed 34 duplicate IDs
- Updated format validation
- Added ID generation for missing entries

---

## Database Issues

### 1. Supabase UnboundLocalError
**Date**: July 6, 2025  
**Status**: ✅ RESOLVED

**Issue**: "cannot access local variable 'supabase' where it is not associated with a value"
**Solution**: Added proper initialization:
```python
supabase = get_supabase_client()
```

### 2. Column Name Mismatches
**Date**: July 6, 2025  
**Status**: ✅ RESOLVED

**Issue**: Search using underscores but database has spaces
**Example**: Searching for "Transaction_ID" but column is "Transaction ID"
**Solution**: Updated all column references to use spaces

### 3. Data Type Conversions
**Status**: ✅ RESOLVED

**Issue**: Percentage stored as decimal (0.50 vs 50%)
**Solution**: Added conversion logic:
```python
if agent_comm_rate > 0 and agent_comm_rate < 1:
    agent_comm_rate = agent_comm_rate * 100
```

---

## UI/UX Issues

### 1. Form Submit Button Missing
**Date**: July 6, 2025  
**Status**: ✅ RESOLVED

**Issue**: Streamlit form missing submit button due to indentation
**Solution**: Fixed form context indentation

### 2. Dashboard Terminology
**Date**: July 6, 2025  
**Status**: ⚠️ DOCUMENTED

**Issue**: Shows "Total Policies: 195" but actually counting transactions
**Impact**: Misleading - one policy can have multiple transactions
**Recommendation**: Change to "Total Transactions: 195"

### 3. Column Mapping Lost on Restart
**Date**: July 6, 2025  
**Status**: ✅ RESOLVED

**Issue**: Saved column mappings only in session state
**Solution**: Implemented JSON file persistence:
```python
config_files/saved_mappings.json
```

---

## Reconciliation Issues

### 1. Name Format Matching
**Date**: July 6, 2025  
**Status**: ✅ RESOLVED

**Issue**: "Barboun, Thomas" not matching "Thomas Barboun"
**Solution**: Added name reversal logic:
```python
if ',' in name:
    parts = name.split(',', 1)
    name_reversed = f"{parts[1].strip()} {parts[0].strip()}"
```

### 2. Date Format Matching
**Date**: July 6, 2025  
**Status**: ✅ RESOLVED

**Issue**: "05/22/2024" not matching "2024-05-22"
**Solution**: Normalize all dates to YYYY-MM-DD format

---

## Terminal & Environment Issues

### 1. WSL2 Path Issues
**Status**: ✅ DOCUMENTED

**Issue**: Windows paths with spaces causing problems
**Solution**: Always quote paths with spaces:
```bash
cd "/path with spaces/folder"
```

### 2. Virtual Environment Activation
**Status**: ✅ DOCUMENTED

**Issue**: venv activation fails in some terminals
**Solution**: Use full path to activate script

---

## Minor Issues

### 1. Auto-save Triggering Too Often
**Status**: ✅ RESOLVED
**Solution**: Debounced auto-save to 3-second delay

### 2. Excel Export Memory Usage
**Status**: ✅ RESOLVED
**Solution**: Implemented streaming for large exports

### 3. Search Performance
**Status**: ✅ RESOLVED
**Solution**: Added database indexing on search columns

---

## Pending Issues

### 1. Performance with Large Datasets
**Priority**: LOW
**Description**: Slow loading with 10,000+ records
**Proposed Solution**: Implement server-side pagination

### 2. Mobile Responsiveness
**Priority**: MEDIUM
**Description**: Some forms difficult to use on mobile
**Proposed Solution**: Responsive design updates

### 3. Concurrent User Edits
**Priority**: MEDIUM
**Description**: No locking mechanism for simultaneous edits
**Proposed Solution**: Implement optimistic locking

---

## Issue Reporting Template

When reporting new issues, include:
```
Date: 
Severity: CRITICAL/HIGH/MEDIUM/LOW
Status: ACTIVE/INVESTIGATING/RESOLVED

Issue:
Steps to Reproduce:
Expected Behavior:
Actual Behavior:
Root Cause:
Solution:
Code Changes:
Testing:
```

---

*This document consolidates issues from APP_ISSUES_AND_FIXES.md, transaction_id_fixes.md, TERMINAL_PROBLEMS.md, PHASE0_CRITICAL_BUG.md, and various implementation files.*