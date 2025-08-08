# Transaction Filtering Analysis - STMT DATE vs Effective Date

## Overview
This document analyzes all places in the commission_app.py that filter transactions for policy terms, identifying which use STMT DATE vs Effective Date and inconsistencies that need to be addressed.

## Key Findings

### 1. Dashboard Metrics (calculate_dashboard_metrics function)
- **YTD 2025 Reconciled Metrics**:
  - Uses `STMT DATE` for filtering -STMT- transactions (line 349): `df_stmt_all['STMT DATE'].dt.year == 2025`
  - Falls back to `Effective Date` if STMT DATE is not available
  - **Reasoning**: STMT DATE represents when payment was actually made

- **YTD 2025 Unreconciled Metrics**:
  - Uses `Effective Date` for filtering original transactions (line 329): `df_originals['Effective Date'].dt.year == 2025`
  - **Reasoning**: For unpaid transactions, effective date is the relevant date

- **Current Month Transactions**:
  - Uses `Effective Date` (lines 296-297): `df['Effective Date'].dt.month == current_month`

### 2. Policy Revenue Ledger Reports
- **Statement Month Filter** (lines 14590-14597):
  - Uses `Effective Date` to find NEW/RWL transactions in selected month
  - Then includes ALL transactions for those policies regardless of dates
  - **Note**: Recent change removed date-based filtering within policy terms (line 14629 comment: "MODIFIED: Include ALL transactions regardless of dates")

### 3. Pending Renewals (get_pending_renewals function)
- **Expiration Tracking**:
  - Uses `X-DATE` (expiration date) for filtering (line 1697): `pd.to_datetime(renewal_candidates[get_mapped_column("X-DATE")])`
  - Filters for policies expiring within 90 days or already expired (line 1711)
  - Does NOT use STMT DATE or Effective Date for filtering

### 4. Edit Policy Transactions
- **Attention Filter** (lines 5528-5536):
  - Filters transactions with payments but no commission
  - Uses `Agent Paid Amount (STMT)` > 0 but doesn't filter by date
  - No date-based filtering applied

### 5. Reconciliation History
- **Date Range Filter** (lines 8697-8698):
  - Uses `STMT DATE` for filtering reconciliation entries: `recon_entries['STMT DATE'].dt.date >= start_date`
  - **Reasoning**: Statement date represents when the reconciliation occurred

### 6. Reports Section
- No specific date filtering found in the Reports tab
- Relies on the full dataset loaded from `load_policies_data()`

## Inconsistencies Found

1. **Dashboard vs Policy Revenue Ledger**:
   - Dashboard uses STMT DATE for reconciled transactions
   - Policy Revenue Ledger uses Effective Date for all filtering
   - This could lead to different counts/amounts between pages

2. **Transaction Type Filtering**:
   - Some places use Transaction ID patterns (e.g., `-STMT-`, `-VOID-`)
   - Others use Transaction Type field (e.g., `NEW`, `RWL`, `CAN`)
   - Mixed approach can cause confusion

3. **Date Column Usage**:
   - STMT DATE: Used for payment/reconciliation timing
   - Effective Date: Used for policy term identification
   - X-DATE: Used for renewal tracking
   - No consistent rule for which to use when

## Recommendations

### 1. Establish Clear Rules
Define when to use each date field:
- **STMT DATE**: For payment/reconciliation timing and financial reporting
- **Effective Date**: For policy term identification and grouping
- **X-DATE**: For renewal tracking and expiration alerts

### 2. Create a Centralized Filtering Function
```python
def filter_transactions_by_date(df, date_type='effective', start_date=None, end_date=None, year=None, month=None):
    """
    Centralized function for date-based transaction filtering.
    
    Args:
        df: DataFrame with transactions
        date_type: 'stmt', 'effective', or 'expiration'
        start_date, end_date: Date range filters
        year, month: Specific period filters
    
    Returns:
        Filtered DataFrame
    """
    date_columns = {
        'stmt': 'STMT DATE',
        'effective': 'Effective Date',
        'expiration': 'X-DATE'
    }
    
    date_col = date_columns.get(date_type, 'Effective Date')
    # Apply filters...
```

### 3. Document the Logic
Add comments in each filtering location explaining:
- Which date field is used and why
- What the filter is trying to achieve
- Any special cases or exceptions

### 4. Consistency Updates Needed
1. **Dashboard Metrics**: Document why STMT DATE is used for reconciled metrics
2. **Policy Revenue Ledger**: Consider using STMT DATE for statement month filter when looking at payments
3. **All Pages**: Add clear labels indicating which date is being used for filtering

### 5. Testing Recommendations
Create test cases that verify:
- Same policy counts across different pages
- Correct date filtering for various scenarios
- Edge cases (e.g., transactions with missing dates)

## Implementation Priority
1. **High**: Fix Dashboard vs Policy Revenue Ledger inconsistency
2. **Medium**: Standardize transaction type filtering approach
3. **Low**: Add centralized filtering function for future consistency

## Affected Files
- `/mnt/c/Users/Patri/OneDrive/STABELL DOCUMENTS/STABELL FILES/TECHNOLOGY/PROGRAMMING/SALES COMMISSIONS APP/commission_app.py`

## Next Steps
1. Review this analysis with the team
2. Decide on standardized approach for each use case
3. Implement changes incrementally with testing
4. Update documentation for future developers