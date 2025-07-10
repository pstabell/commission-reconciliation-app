# Policy Term Implementation Plan

## Overview
Adding a "Policy Term" column to track whether policies are 6 months, 12 months, or other durations. This will significantly improve the accuracy of renewal calculations on the Pending Policy Renewals page.

## Current Problem
The `duplicate_for_renewal` function in commission_app.py (line 1934) currently hardcodes all renewals to 6-month terms:
```python
renewed_df['new_expiration_date'] = renewed_df['new_effective_date'] + pd.DateOffset(months=6) # Assuming 6-month terms for now
```

This causes incorrect renewal dates for 12-month policies and other term lengths.

## Implementation Steps

### 1. Database Update
Run the SQL script: `sql_scripts/add_policy_term_column.sql`
```sql
ALTER TABLE policies 
ADD COLUMN IF NOT EXISTS "Policy Term" TEXT;
```

### 2. Update Column Mapping Config
Add to `column_mapping_config.py` in the `default_ui_fields` dictionary after "Policy Type":
```python
"Policy Type": "Policy Type",
"Policy Term Months": "Policy Term",  # UI shows "Policy Term Months", DB stores as "Policy Term"
"Carrier Name": "Carrier Name",
```

### 3. Update Application Code

#### A. Add to Add New Policy Transaction Form (commission_app.py ~line 3989)
Replace the current Transaction Type row (line 3989-3990) with a two-column layout:

```python
# Row 2.5: Transaction Type and Policy Term (side by side)
col1, col2 = st.columns(2)
with col1:
    transaction_type = st.selectbox("Transaction Type", ["NEW", "RWL", "END", "PCH", "CAN", "XCL", "NBS", "STL", "BoR", "REWRITE"])
with col2:
    policy_term = st.selectbox(
        "Policy Term Months",
        options=[None, 3, 6, 9, 12],
        format_func=lambda x: "" if x is None else f"{x} months",
        help="Select policy duration in months"
    )
```

This places Policy Term on the right column next to Transaction Type, preventing Transaction Type from stretching across both columns.

#### B. Add to Edit Policy Modal (commission_app.py ~line 3074 & 3145)

1. **Update policy_fields list** (line 3074):
```python
policy_fields = ['Writing Code', 'Policy #', 'Product', 'Carrier', 
                 'Policy Type', 'Carrier Name', 'MGA Name', 'Policy Number', 
                 'Transaction Type', 'Policy Term Months',  # Add this after Transaction Type
                 'NEW BIZ CHECKLIST COMPLETE', 'FULL OR MONTHLY PMTS', 'NOTES']
```

2. **Add field handling** after Transaction Type (around line 3154):
```python
elif field == 'Policy Term Months':
    # Policy Term dropdown
    policy_terms = [3, 6, 9, 12]
    current_term = modal_data.get(field, None)
    updated_data[field] = st.selectbox(
        field,
        options=[None] + policy_terms,
        format_func=lambda x: "" if x is None else f"{x} months",
        index=0 if current_term is None else (policy_terms.index(current_term) + 1),
        key=f"modal_{field}",
        help="Select policy duration in months"
    )
```

This places Policy Term Months next to Transaction Type in the two-column layout.

#### C. Update Renewal Calculation Logic (commission_app.py line 1934)
Replace the hardcoded 6-month calculation. The logic remains the same - use the expiration date from the last transaction as the new effective date. The Policy Term just determines how far in the future the new expiration date should be:

```python
def duplicate_for_renewal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Duplicates the given policies and updates their dates for renewal.
    Uses the expiration date from the last transaction as the new effective date.
    """
    if df.empty:
        return pd.DataFrame()

    renewed_df = df.copy()
    
    # The new effective date is still the expiration date of the last transaction
    renewed_df['new_effective_date'] = renewed_df['expiration_date']
    
    # Calculate new expiration date based on Policy Term
    for idx, row in renewed_df.iterrows():
        policy_term = row.get(get_mapped_column("Policy Term Months"), None)
        
        # Policy Term is stored as an integer (months)
        if policy_term and pd.notna(policy_term):
            months_to_add = int(policy_term)
        else:
            # Default to 6 months if not specified
            months_to_add = 6
        
        # New expiration = new effective date + policy term
        renewed_df.at[idx, 'new_expiration_date'] = row['new_effective_date'] + pd.DateOffset(months=months_to_add)
    
    # Update the relevant columns
    renewed_df[get_mapped_column("Effective Date")] = renewed_df['new_effective_date'].dt.strftime('%m/%d/%Y')
    renewed_df[get_mapped_column("X-DATE")] = renewed_df['new_expiration_date'].dt.strftime('%m/%d/%Y')
    renewed_df[get_mapped_column("Transaction Type")] = "RWL"
    
    return renewed_df
```

**Important**: The `get_pending_renewals` function already handles finding the latest transaction for each policy number (line 1198):
```python
# Get the most recent transaction for each policy
latest_renewals = renewal_candidates.drop_duplicates(subset="Policy Number", keep="first")
```

This ensures we're always working with the most recent transaction's dates.

### 4. Display Policy Term in Views
Add to relevant data displays:
- All Policy Transactions page
- Search & Filter results
- Policy Revenue Ledger
- Pending Policy Renewals page

### 5. Data Migration (Optional)
After implementing, you can run the UPDATE query in the SQL script to populate Policy Term for existing records based on the date difference between Effective Date and X-DATE.

## Benefits
1. **Accurate Renewals**: Renewals will use the actual policy term instead of assuming 6 months
2. **Better Reporting**: Can filter and report by policy term
3. **Improved Forecasting**: More accurate commission projections based on correct renewal dates
4. **Audit Trail**: Clear visibility of policy terms for compliance

## Testing Checklist
- [ ] Add new policy with 6-month term
- [ ] Add new policy with 12-month term
- [ ] Edit existing policy to set term
- [ ] Check Pending Policy Renewals shows correct future dates
- [ ] Verify renewal creates correct new expiration date
- [ ] Test filtering by Policy Term
- [ ] Export data and verify Policy Term column included

## Migration Notes
- The field is optional (nullable) so existing data won't break
- The UPDATE query in the SQL script can help populate existing records
- Manual review recommended for "Other" term policies