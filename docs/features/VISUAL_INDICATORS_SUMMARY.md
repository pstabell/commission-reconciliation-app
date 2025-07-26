# Visual Indicators Throughout the App

## Overview
The Sales Commission App uses visual indicators to help users quickly identify different transaction types. This is implemented in two ways depending on the display type.

## Color-Based Highlighting (st.dataframe displays)

In sections that use `st.dataframe()`, transactions are highlighted with background colors:

- **STMT Transactions**: Light blue background (#e6f3ff)
- **VOID Transactions**: Light red background (#ffe6e6)
- **Regular Transactions**: No background color

### Where You'll See Colors:
1. **Dashboard** - Recent Activity section
2. **All Policy Transactions** - Main transaction table
3. **Search & Filter Results** - When filtering data
4. **Policy Revenue Ledger Reports** - Report preview
5. **Reconciliation** - Matched and unreconciled transaction tables

## Emoji Indicators (st.data_editor displays)

In editable sections that use `st.data_editor()`, a Type column with emoji indicators is used:

- 💙 STMT = Statement/Reconciliation Entry
- 🔴 VOID = Voided Transaction
- 📄 = Regular Transaction

### Where You'll See Emojis:
1. **Policy Revenue Ledger (Editable)** - First column shows transaction type
2. **Edit Policy Transactions** - Note: This section filters out STMT/VOID transactions, so you won't see them here

## Benefits

1. **Quick Recognition**: Instantly identify reconciliation and void entries
2. **Audit Trail**: Easily track payment history and voided transactions
3. **Error Prevention**: Visual distinction helps prevent accidental modifications
4. **Consistent Experience**: Similar visual cues across all parts of the application

## Technical Implementation

The app uses a utility function `style_special_transactions()` that checks the Transaction ID for patterns:
- Contains "-STMT-" → Statement transaction
- Contains "-VOID-" → Voided transaction
- Otherwise → Regular transaction

This ensures consistent identification across all displays.