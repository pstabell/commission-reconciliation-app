# Policy Term-Based Transaction Filtering

## Overview
The Sales Commission App uses policy term-based grouping to show all transactions related to a policy's lifecycle. This ensures users see complete financial activity for each policy term, including endorsements, cancellations, and payment transactions.

## Date Implemented
August 5, 2025 (Version 3.9.32)

## The Core Design Principle
**Policy terms should show ALL related transactions**, not just those with dates in a specific range. When viewing a policy term or filtering by month:
- Find policies that START (NEW/RWL) in that period
- Show ALL transactions for those policies, regardless of individual transaction dates

## Problems Fixed

### 1. Policy Revenue Ledger - STMT Transaction Filtering
**Issue**: STMT transactions weren't appearing in policy terms
**Root Causes**:
- STMT transactions were being filtered by STMT DATE instead of Effective Date
- STMT transactions with Transaction Type="END" were caught by END filtering logic before STMT logic
**Solution**: 
- Changed to filter STMT transactions by Effective Date
- Reordered logic to check for "-STMT-" pattern FIRST

### 2. Policy Revenue Ledger Reports - Wrong Filtering Logic
**Issue**: Reports page was filtering individual transactions by date instead of showing complete policy terms
**Root Cause**: The page was showing only transactions with Effective Dates in the selected month
**Solution**: Changed to term-based logic:
1. Find NEW/RWL transactions in the selected month
2. Show ALL transactions for those policies

## The Correct Implementation

### Policy Term Filtering (Policy Revenue Ledger)
```python
# Check for STMT/VOID transactions FIRST (they might have various transaction types)
if "-STMT-" in str(row.get("Transaction ID", "")) or "-VOID-" in str(row.get("Transaction ID", "")):
    # Include if Effective Date falls within term
    if pd.notna(trans_eff_date) and term_eff_date <= trans_eff_date <= term_x_date:
        filtered_rows.append(idx)
```

### Month-Based Term Filtering (Policy Revenue Ledger Reports)
```python
# Find all NEW/RWL transactions effective in the selected month
new_rwl_in_month = working_data[
    (working_data['Transaction Type'].isin(['NEW', 'RWL'])) & 
    (working_data['Year-Month'] == selected_ym)
]

# Get ALL transactions for these policies
for _, row in policy_identifiers.iterrows():
    policy_transactions = working_data[
        (working_data['Client ID'] == client_id) & 
        (working_data['Policy Number'] == policy_num)
    ]
    month_data = pd.concat([month_data, policy_transactions])
```

## Example Scenarios

### Scenario 1: Policy Term View
- Policy Term: 08/28/2024 to 02/28/2025
- Transactions:
  - NEW: Effective Date 08/28/2024
  - END: Effective Date 09/01/2024 (endorsement)
  - STMT: Effective Date 08/28/2024 (payment for original premium)
  - STMT: Effective Date 09/01/2024 (payment for endorsement)

**Result**: ALL transactions appear in the term view

### Scenario 2: Month Filter (August 2024)
- User selects August 2024 in Reports page
- System finds policies with NEW/RWL in August
- Shows ALL transactions for those policies, including:
  - September endorsements
  - October reconciliations
  - Any future activity

**Result**: Complete policy lifecycle visible

## Key Learnings

### 1. Transaction ID Patterns Matter
STMT transactions are identified by "-STMT-" in their Transaction ID, not by Transaction Type field

### 2. Order of Operations
Check for special transaction patterns (STMT, VOID) before evaluating transaction types

### 3. Term-Based vs Date-Based Filtering
- **Wrong**: Filter each transaction by its date
- **Right**: Find policies in a period, show all their transactions

## Benefits
1. **Complete Financial Picture**: See all activity for policies in your portfolio
2. **Accurate Balances**: All payments and adjustments included
3. **Consistent Views**: Both Ledger pages show same data
4. **Logical Grouping**: Transactions grouped by policy lifecycle, not arbitrary dates

## Related Documentation
- [RECONCILIATION_SYSTEM.md](RECONCILIATION_SYSTEM.md) - How reconciliation creates STMT transactions
- [CLAUDE.md](../operations/CLAUDE.md) - Issue #31 for technical details
- [CHANGELOG.md](../core/CHANGELOG.md) - Version 3.9.32 release notes