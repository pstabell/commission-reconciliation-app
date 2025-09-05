"""
Streamlit tool to populate missing Policy Origination Dates
This can be integrated into the Tools page of the main app
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def find_origination_date_for_tool(policy_num, all_data, visited=None):
    """
    Recursively find the origination date by tracing back to the original NEW transaction.
    """
    if visited is None:
        visited = set()
    
    if policy_num in visited:
        return None, None, "Circular reference detected"
    visited.add(policy_num)
    
    # Find transactions for this policy number
    policy_transactions = all_data[all_data['Policy Number'] == policy_num].copy()
    
    if not policy_transactions.empty:
        # Sort by effective date to get earliest
        if 'Effective Date' in policy_transactions.columns:
            policy_transactions = policy_transactions.sort_values('Effective Date')
        
        # Check for NEW transaction
        new_transactions = policy_transactions[policy_transactions['Transaction Type'] == 'NEW']
        if len(new_transactions) > 1:
            return None, None, "Multiple NEW transactions found"
        elif len(new_transactions) == 1:
            # Found the NEW transaction
            orig_date = new_transactions.iloc[0].get('Policy Origination Date')
            if orig_date and pd.notna(orig_date):
                return orig_date, new_transactions.iloc[0].get('Transaction ID'), "Found from NEW transaction"
            # If NEW transaction has no origination date, use its effective date
            eff_date = new_transactions.iloc[0].get('Effective Date')
            if eff_date and pd.notna(eff_date):
                return eff_date, new_transactions.iloc[0].get('Transaction ID'), "Found from NEW transaction's Effective Date"
        
        # No NEW transaction, check for Prior Policy Number
        for _, trans in policy_transactions.iterrows():
            prior_policy = trans.get('Prior Policy Number')
            if prior_policy and pd.notna(prior_policy) and str(prior_policy).strip():
                # Recursively follow the chain
                result_date, source_trans_id, result_msg = find_origination_date_for_tool(prior_policy, all_data, visited)
                if result_date:
                    return result_date, source_trans_id, f"{result_msg} (via Prior Policy: {prior_policy})"
    
    return None, None, "No NEW transaction found in chain"

def populate_origination_dates_tool(all_data, supabase):
    """
    Tool to populate missing Policy Origination Dates.
    Can be called from the Tools page.
    """
    st.subheader("🗓️ Populate Missing Policy Origination Dates")
    
    st.info("""
    This tool will automatically populate missing Policy Origination Dates using the following logic:
    - **NEW transactions**: Use the Effective Date
    - **BoR transactions**: Use the Effective Date (new relationship)
    - **Other transactions**: Trace back through policy history to find the original NEW transaction
    """)
    
    # Find transactions missing Policy Origination Date
    missing_origination = all_data[
        (all_data['Policy Origination Date'].isna()) | 
        (all_data['Policy Origination Date'] == '')
    ].copy()
    
    st.metric("Transactions Missing Origination Date", len(missing_origination))
    
    if len(missing_origination) == 0:
        st.success("✅ All transactions already have Policy Origination Date populated!")
        return
    
    # Show preview of what will be updated
    if st.checkbox("Show transactions that need origination dates"):
        st.dataframe(
            missing_origination[['Transaction ID', 'Customer', 'Policy Number', 'Transaction Type', 'Effective Date']].head(20),
            use_container_width=True
        )
        if len(missing_origination) > 20:
            st.caption(f"Showing first 20 of {len(missing_origination)} transactions")
    
    # Process button
    if st.button("🔍 Analyze Missing Dates", type="primary"):
        updates = []
        errors = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Process each missing transaction
        for idx, row in missing_origination.iterrows():
            progress = (idx + 1) / len(missing_origination)
            progress_bar.progress(progress)
            
            transaction_id = row.get('Transaction ID')
            transaction_type = row.get('Transaction Type')
            policy_number = row.get('Policy Number')
            effective_date = row.get('Effective Date')
            customer = row.get('Customer', 'Unknown')
            
            status_text.text(f"Processing {idx+1}/{len(missing_origination)}: {transaction_id}")
            
            auto_populated_date = None
            reason = ""
            
            # Apply the same logic as the form
            if transaction_type == 'NEW':
                if effective_date and pd.notna(effective_date):
                    auto_populated_date = effective_date
                    reason = "NEW transaction - using Effective Date"
            
            elif transaction_type == 'BoR':
                if effective_date and pd.notna(effective_date):
                    auto_populated_date = effective_date
                    reason = "BoR transaction - using Effective Date"
            
            elif transaction_type in ['RWL', 'END', 'PCH', 'CAN', 'XCL', 'REWRITE', 'NBS', 'STL'] and policy_number:
                found_date, source_trans_id, message = find_origination_date_for_tool(policy_number, all_data)
                if found_date:
                    auto_populated_date = found_date
                    reason = f"{transaction_type} - {message}"
            
            # Store results
            if auto_populated_date:
                updates.append({
                    'Transaction ID': transaction_id,
                    'Customer': customer,
                    'Policy Number': policy_number,
                    'Type': transaction_type,
                    'New Origination Date': auto_populated_date,
                    'Reason': reason
                })
            else:
                errors.append({
                    'Transaction ID': transaction_id,
                    'Customer': customer,
                    'Policy Number': policy_number,
                    'Type': transaction_type,
                    'Reason': 'No origination date found'
                })
        
        progress_bar.empty()
        status_text.empty()
        
        # Show results
        col1, col2 = st.columns(2)
        with col1:
            st.metric("✅ Can Update", len(updates))
        with col2:
            st.metric("❌ Cannot Update", len(errors))
        
        # Store results in session state
        st.session_state['origination_updates'] = updates
        st.session_state['origination_errors'] = errors
        
        # Show preview of updates
        if updates:
            st.success(f"Found {len(updates)} transactions that can be updated")
            
            # Convert dates to strings for display
            updates_df = pd.DataFrame(updates)
            updates_df['New Origination Date'] = pd.to_datetime(updates_df['New Origination Date']).dt.date
            
            st.dataframe(updates_df.head(10), use_container_width=True)
            if len(updates) > 10:
                st.caption(f"Showing first 10 of {len(updates)} updates")
        
        if errors:
            with st.expander(f"⚠️ {len(errors)} transactions cannot be updated"):
                errors_df = pd.DataFrame(errors)
                st.dataframe(errors_df, use_container_width=True)
    
    # Update button (only shows after analysis)
    if 'origination_updates' in st.session_state and st.session_state['origination_updates']:
        st.divider()
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("💾 Update Database", type="primary", use_container_width=True):
                updates = st.session_state['origination_updates']
                success_count = 0
                error_count = 0
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for idx, update in enumerate(updates):
                    progress = (idx + 1) / len(updates)
                    progress_bar.progress(progress)
                    status_text.text(f"Updating {idx+1}/{len(updates)}: {update['Transaction ID']}")
                    
                    try:
                        # Update the record
                        supabase.table('policies').update({
                            'Policy Origination Date': update['New Origination Date']
                        }).eq('Transaction ID', update['Transaction ID']).execute()
                        
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        st.error(f"Error updating {update['Transaction ID']}: {str(e)}")
                
                progress_bar.empty()
                status_text.empty()
                
                # Clear the updates from session state
                del st.session_state['origination_updates']
                if 'origination_errors' in st.session_state:
                    del st.session_state['origination_errors']
                
                # Show results
                st.success(f"✅ Successfully updated {success_count} transactions!")
                if error_count > 0:
                    st.error(f"❌ Failed to update {error_count} transactions")
                
                # Clear cache to show updated data
                if hasattr(st, 'cache_data'):
                    st.cache_data.clear()
                
                st.balloons()
                
                # Generate report
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_data = []
                for update in updates:
                    report_data.append({
                        'Transaction ID': update['Transaction ID'],
                        'Customer': update['Customer'],
                        'Policy Number': update['Policy Number'],
                        'Transaction Type': update['Type'],
                        'New Origination Date': update['New Origination Date'],
                        'Reason': update['Reason'],
                        'Status': 'Updated'
                    })
                
                report_df = pd.DataFrame(report_data)
                csv = report_df.to_csv(index=False)
                
                st.download_button(
                    label="📥 Download Update Report",
                    data=csv,
                    file_name=f"origination_date_updates_{timestamp}.csv",
                    mime="text/csv"
                )