"""
Quick check to understand why reconciliation shows small balances
when dashboard shows $9,824.29 commission due.
"""

import streamlit as st

# This would be run within the app context to debug the issue
def debug_reconciliation_display():
    """Add this function call to the reconciliation tab to debug"""
    
    # Get the data
    all_data = st.session_state.get('all_data', None)
    if all_data is None:
        st.error("No data available in session state")
        return
        
    st.write("### Debug: Reconciliation Balance Analysis")
    
    # Call the calculate_transaction_balances function
    from commission_app import calculate_transaction_balances
    
    # Get transactions with balances
    outstanding = calculate_transaction_balances(all_data)
    
    st.write(f"**Total transactions with balance > $0.01:** {len(outstanding)}")
    
    if not outstanding.empty and '_balance' in outstanding.columns:
        # Show balance distribution
        st.write("\n**Balance Distribution:**")
        balance_ranges = {
            "$0.01 - $1": ((outstanding['_balance'] > 0.01) & (outstanding['_balance'] <= 1)).sum(),
            "$1 - $10": ((outstanding['_balance'] > 1) & (outstanding['_balance'] <= 10)).sum(),
            "$10 - $50": ((outstanding['_balance'] > 10) & (outstanding['_balance'] <= 50)).sum(),
            "$50 - $100": ((outstanding['_balance'] > 50) & (outstanding['_balance'] <= 100)).sum(),
            "$100 - $500": ((outstanding['_balance'] > 100) & (outstanding['_balance'] <= 500)).sum(),
            "$500+": (outstanding['_balance'] > 500).sum()
        }
        
        for range_name, count in balance_ranges.items():
            st.write(f"- {range_name}: {count} transactions")
        
        # Show top 20 by balance
        st.write("\n**Top 20 Transactions by Balance:**")
        top_20 = outstanding.nlargest(20, '_balance')[['Transaction ID', 'Customer', 'Policy Number', 'Total Agent Comm', '_balance']]
        st.dataframe(top_20)
        
        # Total balance
        total_balance = outstanding['_balance'].sum()
        st.write(f"\n**Total Outstanding Balance: ${total_balance:,.2f}**")
        
        # Check if this matches dashboard
        st.write(f"\n**Dashboard shows: $9,824.29**")
        st.write(f"**Difference: ${9824.29 - total_balance:,.2f}**")
        
        # Check for date filtering issues
        st.write("\n### Date Range Check:")
        
        # Show all transactions (not just with balance)
        all_trans_with_balance = calculate_transaction_balances(all_data, show_all_for_reconciliation=True)
        st.write(f"**All transactions in past 18 months:** {len(all_trans_with_balance)}")
        
        # Show balance = 0 transactions
        zero_balance = all_trans_with_balance[all_trans_with_balance['_balance'] == 0]
        st.write(f"**Transactions with exactly $0 balance:** {len(zero_balance)}")
        
        # Show negative balance transactions  
        negative_balance = all_trans_with_balance[all_trans_with_balance['_balance'] < 0]
        st.write(f"**Transactions with negative balance:** {len(negative_balance)}")
        
        if len(negative_balance) > 0:
            st.write("Sample negative balance transactions:")
            st.dataframe(negative_balance.head(10)[['Transaction ID', 'Customer', 'Total Agent Comm', '_balance']])

# The issue appears to be:
# 1. The calculate_transaction_balances function filters out transactions with balance <= 0.01
# 2. This might be hiding transactions that actually have larger balances
# 3. Or there might be a data issue where Total Agent Comm is not populated correctly

# SOLUTION:
# The reconciliation page should show ALL transactions from the past 18 months,
# not just those with outstanding balances. Users need to see what has been paid
# and what hasn't. The current filter is too restrictive.