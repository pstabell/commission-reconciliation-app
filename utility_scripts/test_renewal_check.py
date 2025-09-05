"""
Simple test to add to commission_app.py to diagnose renewal issues
Add this code to a test page in the app to check specific transactions
"""

def test_renewal_diagnosis():
    """Test function to diagnose why I0Y68NM shows in Pending Renewals"""
    
    st.header("Renewal Diagnosis Test")
    
    transaction_id = st.text_input("Enter Transaction ID to diagnose:", value="I0Y68NM")
    
    if st.button("Run Diagnosis"):
        # Get all policies
        df = load_policies_data()
        
        # Find the original transaction
        original = df[df["Transaction ID"] == transaction_id]
        
        if original.empty:
            st.error(f"Transaction {transaction_id} not found!")
            return
            
        st.subheader(f"Original Transaction: {transaction_id}")
        original_row = original.iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Customer:** {original_row['Customer']}")
            st.write(f"**Policy Number:** {original_row['Policy Number']}")
            st.write(f"**Transaction Type:** {original_row['Transaction Type']}")
        with col2:
            st.write(f"**Effective Date:** {original_row['Effective Date']}")
            st.write(f"**X-DATE:** {original_row['X-DATE']}")
            st.write(f"**Prior Policy Number:** {original_row.get('Prior Policy Number', 'None')}")
        
        # Check if this policy has been renewed
        policy_num = original_row['Policy Number']
        st.subheader(f"Checking for renewals of Policy Number: {policy_num}")
        
        # Look for transactions with this policy number in Prior Policy Number field
        renewals = df[df["Prior Policy Number"] == policy_num]
        
        if not renewals.empty:
            st.success(f"✅ Found {len(renewals)} renewal(s) for this policy:")
            for idx, renewal in renewals.iterrows():
                with st.expander(f"Renewal Transaction: {renewal['Transaction ID']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Customer:** {renewal['Customer']}")
                        st.write(f"**Policy Number:** {renewal['Policy Number']}")
                        st.write(f"**Transaction Type:** {renewal['Transaction Type']}")
                    with col2:
                        st.write(f"**Prior Policy Number:** {renewal['Prior Policy Number']}")
                        st.write(f"**Effective Date:** {renewal['Effective Date']}")
                        st.write(f"**X-DATE:** {renewal['X-DATE']}")
        else:
            st.warning("❌ No renewals found with this policy number in Prior Policy Number field")
            
            # Check for other policies by same customer
            customer = original_row['Customer']
            customer_policies = df[df['Customer'] == customer].sort_values('Effective Date', ascending=False)
            
            st.subheader(f"Other policies for customer: {customer}")
            if len(customer_policies) > 1:
                st.write(f"Found {len(customer_policies)} total policies:")
                
                # Show top 5 policies
                for idx, policy in customer_policies.head(5).iterrows():
                    if policy['Transaction ID'] == transaction_id:
                        continue  # Skip the original
                        
                    with st.expander(f"Transaction: {policy['Transaction ID']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Policy Number:** {policy['Policy Number']}")
                            st.write(f"**Transaction Type:** {policy['Transaction Type']}")
                        with col2:
                            st.write(f"**Prior Policy Number:** {policy.get('Prior Policy Number', 'None')}")
                            st.write(f"**Effective Date:** {policy['Effective Date']}")
                            st.write(f"**X-DATE:** {policy['X-DATE']}")
                        
                        # Check if this could be a renewal
                        if policy['Transaction Type'] == 'RWL' and pd.isna(policy.get('Prior Policy Number')):
                            st.warning("⚠️ This looks like a renewal but has no Prior Policy Number set!")
            
        # Show why it appears in Pending Renewals
        st.subheader("Pending Renewals Logic:")
        
        # Check expiration
        try:
            exp_date = pd.to_datetime(original_row['X-DATE'])
            today = pd.to_datetime(datetime.date.today())
            days_until_expiry = (exp_date - today).days
            
            if days_until_expiry < 60:
                st.info(f"📅 Policy expires in {days_until_expiry} days (within 60-day window)")
            else:
                st.success(f"✅ Policy expires in {days_until_expiry} days (outside 60-day window)")
        except:
            st.error("Could not parse expiration date")
        
        # Check renewal status
        if renewals.empty:
            st.warning("❌ No renewal found - will appear in Pending Renewals")
        else:
            st.success("✅ Renewal found - should NOT appear in Pending Renewals")
            
        # Also check the specific transaction 4W014EN
        if st.checkbox("Also check transaction 4W014EN"):
            other_trans = df[df["Transaction ID"] == "4W014EN"]
            if not other_trans.empty:
                other_row = other_trans.iloc[0]
                st.subheader("Transaction 4W014EN:")
                st.write(f"**Customer:** {other_row['Customer']}")
                st.write(f"**Policy Number:** {other_row['Policy Number']}")
                st.write(f"**Prior Policy Number:** {other_row.get('Prior Policy Number', 'None')}")
                
                if pd.notna(other_row.get('Prior Policy Number')):
                    st.info(f"This transaction has Prior Policy Number: {other_row['Prior Policy Number']}")
                else:
                    st.warning("This transaction has NO Prior Policy Number set!")

# Add this function call to your Streamlit app in a test section
# test_renewal_diagnosis()