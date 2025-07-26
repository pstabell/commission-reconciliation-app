# Policy Revenue Ledger Financial Columns Enhancement

## Date: 2025-01-26

### Overview
Added comprehensive financial columns to the Policy Revenue Ledger (Editable) section to provide a complete financial view of policy transactions. These columns appear to the right of the Delete column and are accessible via horizontal scrolling.

### New Financial Columns

1. **Premium Sold** - The actual premium amount for each transaction
2. **Policy Taxes & Fees** - Additional charges on top of premium
3. **Commissionable Premium** - The base amount commissions are calculated on
4. **Broker Fee** - Any broker fees charged
5. **Broker Fee Agent Comm** - Commission earned on broker fees

### Implementation Details

#### Column Layout
```
[Type] [Transaction ID] [Effective Date] [Description] [Credit] [Debit] [Transaction Type] [Delete] → [Premium Sold] [Taxes & Fees] [Comm Premium] [Broker Fee] [Broker Comm]
```

- Core ledger columns remain visible by default
- Financial columns accessible via horizontal scroll
- No change to the default viewing area

#### Policy Financial Summary Section

Added below the Ledger Totals section with two rows of metrics:

**Row 1:**
- Total Premium Sold
- Total Taxes & Fees  
- Commissionable Premium

**Row 2:**
- Total Broker Fees
- Broker Fee Agent Comm

### Special Rules for STMT/VOID Transactions

1. **Delete Protection**
   - Delete checkbox is automatically disabled for STMT and VOID transactions
   - Tooltip indicates "STMT and VOID entries cannot be deleted"

2. **Edit Protection**
   - STMT and VOID rows are skipped during save operations
   - Prevents accidental modification of reconciliation entries

3. **Visual Indicators**
   - 💙 STMT = Statement/Reconciliation Entry
   - 🔴 VOID = Voided Transaction
   - 📄 = Regular Transaction

### Technical Implementation

#### Data Population
```python
# Financial columns use mapped column names
premium_col = get_mapped_column("Premium Sold") or "Premium Sold"
if premium_col in policy_rows.columns:
    ledger_df["Premium Sold"] = policy_rows[premium_col]
else:
    ledger_df["Premium Sold"] = 0.0
```

#### Column Configuration
```python
# Configure financial columns as currency columns
for fin_col in financial_columns:
    column_config[fin_col] = st.column_config.NumberColumn(
        fin_col,
        format="$%.2f",
        step=0.01,
        help=f"Enter {fin_col} amount"
    )
```

#### STMT/VOID Protection
```python
# Disable delete for STMT and VOID transactions
if "Type" in ledger_df_display.columns:
    stmt_void_mask = ledger_df_display["Type"].isin(["💙 STMT", "🔴 VOID"])
    ledger_df_display.loc[stmt_void_mask, "Delete"] = False

# Skip STMT and VOID during save
if "Type" in row and row["Type"] in ["💙 STMT", "🔴 VOID"]:
    continue
```

### User Benefits

1. **Complete Financial View** - All financial data for a policy in one place
2. **Horizontal Organization** - Financial details don't clutter the main view
3. **Automatic Totals** - Policy Financial Summary provides instant calculations
4. **Data Protection** - STMT/VOID entries protected from accidental changes
5. **Term-Specific Analysis** - When combined with X-DATE filter, shows financials for specific terms

### Files Modified
- `commission_app.py` - Main application file
  - Lines 10958-10965: Added financial_columns definition
  - Lines 11015-11053: Added financial column data population
  - Lines 11225-11228: Added STMT/VOID delete protection
  - Lines 11287-11301: Added column configurations
  - Lines 11356-11383: Added Policy Financial Summary section
  - Lines 11387-11395: Added STMT/VOID edit protection

### Usage Notes

1. Financial columns are editable for regular transactions
2. All financial columns display as currency with 2 decimal places
3. Totals update automatically as you edit values
4. Empty cells default to $0.00 in calculations
5. Column data persists when switching between policies