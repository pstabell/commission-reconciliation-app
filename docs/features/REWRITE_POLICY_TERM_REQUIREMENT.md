# REWRITE Transaction as Policy Term Trigger

**Created**: August 11, 2025  
**Priority**: HIGH  
**Status**: Requirement Identified

## Business Requirement

REWRITE transactions should be treated as the start of a new policy term, exactly like NEW and RWL transactions.

## Current Issue

Currently, only NEW and RWL transactions trigger a new policy term. This causes REWRITE transactions to be incorrectly grouped with previous policy terms, leading to:
- Incorrect policy term grouping in ledgers
- REWRITE policies not appearing in Pending Renewals when due
- Confusing transaction organization for users

### Example Case
Transaction 2A92ZR7-IMPORT (REWRITE) for Ruth Ramey's policy F4033008 is being grouped with an earlier term instead of starting its own term.

## Business Logic

A REWRITE transaction represents:
- A complete rewrite of an existing policy
- Often involves carrier changes or significant policy modifications  
- Creates a new policy that replaces the old one (linked via Prior Policy Number)
- Should be treated as the beginning of a new policy lifecycle

## Affected Areas

### 1. Policy Revenue Ledger
- Term grouping logic needs to include REWRITE
- REWRITE should start a new term group
- Sort order should treat REWRITE like NEW/RWL (appears first in term)

### 2. Policy Revenue Ledger Reports  
- Effective Date filter should include REWRITE dates
- Term identification logic must recognize REWRITE as term start
- Help text should mention "NEW, RWL, and REWRITE transactions"

### 3. Pending Policy Renewals
- REWRITE policies should be eligible for renewal tracking
- get_pending_renewals() function must include REWRITE
- Renewal candidates should include REWRITE transaction types

### 4. Documentation
- Update all references to "NEW and RWL" to include REWRITE
- Update tooltips and help text
- Update user guides

## Technical Implementation

### Code Locations to Update

1. **get_pending_renewals() function**
   - Change: `df[df[get_mapped_column("Transaction Type")].isin(["NEW", "RWL"])]`
   - To: `df[df[get_mapped_column("Transaction Type")].isin(["NEW", "RWL", "REWRITE"])]`

2. **Policy Revenue Ledger - Term Grouping**
   - Update all instances where NEW/RWL are used for term identification
   - Include REWRITE in term start detection logic

3. **Policy Revenue Ledger Reports - Filtering**
   - Update Effective Date dropdown to include REWRITE transactions
   - Update all filtering logic that uses NEW/RWL

4. **Transaction Sorting**
   - Ensure REWRITE is sorted with NEW/RWL at the beginning of terms

## Implementation Priority

This is a HIGH priority fix because:
- It affects core business logic
- Current behavior doesn't match business reality
- Users are experiencing confusion with policy grouping
- Renewal tracking is incomplete without REWRITE policies

## Testing Requirements

After implementation, verify:
1. REWRITE transactions start new policy terms in ledgers
2. REWRITE policies appear in Pending Renewals
3. Effective Date filters include REWRITE dates
4. Transaction sorting places REWRITE at term start
5. All documentation reflects the change