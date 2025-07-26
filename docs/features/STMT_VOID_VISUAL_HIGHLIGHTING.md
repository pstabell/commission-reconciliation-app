# STMT and VOID Transaction Visual Highlighting

## Date: 2025-01-26

### Overview
Added special visual highlighting for STMT (statement/reconciliation) and VOID transactions throughout the application to make them immediately identifiable in any data table.

### Feature Details

#### Color Scheme
- **STMT Transactions** (contains "-STMT-" in Transaction ID): Light blue background (#e6f3ff)
- **VOID Transactions** (contains "-VOID-" in Transaction ID): Light red background (#ffe6e6)

#### Implementation
A new utility function `style_special_transactions()` was created to apply consistent styling across all dataframes that display Transaction IDs.

```python
def style_special_transactions(df):
    """Apply special styling to STMT and VOID transactions in a dataframe.
    
    Args:
        df: pandas DataFrame with a 'Transaction ID' column
    
    Returns:
        Styled DataFrame with colored rows for STMT and VOID transactions
    """
    def highlight_transaction_type(row):
        if 'Transaction ID' in row:
            trans_id = str(row['Transaction ID'])
            if '-STMT-' in trans_id:
                # Light blue background for STMT transactions
                return ['background-color: #e6f3ff'] * len(row)
            elif '-VOID-' in trans_id:
                # Light red background for VOID transactions
                return ['background-color: #ffe6e6'] * len(row)
        return [''] * len(row)
    
    # Check if DataFrame has Transaction ID column
    if 'Transaction ID' in df.columns:
        return df.style.apply(highlight_transaction_type, axis=1)
    else:
        return df
```

### Locations Updated

The visual highlighting has been applied to the following sections:

1. **Dashboard**
   - Recent Activity table (lines 4260-4268)

2. **All Policy Transactions**  
   - Main transaction display table (lines 4580-4588)

3. **Search & Filter Results**
   - Filtered transaction results (lines 6478-6487)

4. **Policy Revenue Ledger Reports**
   - Report preview table (lines 12021-12025)

5. **Reconciliation**
   - Matched transactions display (lines 2079-2091)
   - Unreconciled transactions display (lines 7435-7453)
   - Reconciliation History (already had custom VOID styling)

6. **Policy Revenue Ledger (Editable)**
   - Added visual indicator column with emojis (lines 10977-10984)
   - Added legend above the table (lines 11191-11200)
   - Since st.data_editor doesn't support row styling, implemented emoji indicators instead

### Technical Notes

- The styling is applied using pandas DataFrame styling functionality for st.dataframe() displays
- For st.data_editor() displays (like Policy Revenue Ledger), visual indicator column with emojis is used instead
- Gracefully handles DataFrames without Transaction ID column
- Performance impact is minimal as styling is applied only at display time
- Visual indicators in Policy Revenue Ledger:
  - 💙 STMT = Statement/Reconciliation Entry
  - 🔴 VOID = Voided Transaction
  - 📄 = Regular Transaction

### User Benefits

1. **Immediate Visual Recognition**: Users can instantly identify reconciliation and void entries
2. **Improved Audit Trail**: Makes it easier to track payment history and voided transactions
3. **Reduced Errors**: Visual distinction helps prevent accidental modifications to reconciliation entries
4. **Better Navigation**: When scrolling through large datasets, special entries stand out
5. **Consistent Experience**: Same visual cues across all parts of the application

### Future Considerations

- Could extend to include other special transaction types (e.g., -ADJ- for adjustments)
- Could add icons in addition to colors for better accessibility
- Consider making colors configurable in settings