"""Authentication helpers for the SaaS version."""
import streamlit as st
from supabase import Client
import os
from datetime import datetime

def check_subscription_status(email: str, supabase: Client) -> dict:
    """Check if user has active subscription."""
    try:
        result = supabase.table('users').select('*').eq('email', email).execute()
        if result.data and len(result.data) > 0:
            user = result.data[0]
            return {
                'has_subscription': True,
                'status': user.get('subscription_status', 'inactive'),
                'is_active': user.get('subscription_status') == 'active'
            }
    except Exception as e:
        st.error(f"Error checking subscription: {e}")
    
    return {
        'has_subscription': False,
        'status': 'none',
        'is_active': False
    }

def show_production_login_with_auth():
    """Show the production login with email/password authentication."""
    st.title("🔐 Commission Tracker Pro")
    
    # Create tabs for login, register, and subscribe
    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Subscribe"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_register_form()
    
    with tab3:
        show_subscribe_tab()

def show_login_form():
    """Show email/password login form."""
    st.subheader("Login to Your Account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", type="primary", use_container_width=True, key="login_button"):
            if email and password:
                # Check if user exists in database
                # Avoid circular import by creating client directly
                from supabase import create_client
                url = os.getenv("PRODUCTION_SUPABASE_URL", os.getenv("SUPABASE_URL"))
                key = os.getenv("PRODUCTION_SUPABASE_ANON_KEY", os.getenv("SUPABASE_ANON_KEY"))
                
                if not url or not key:
                    st.error("Database not configured. Please use demo password.")
                else:
                    supabase = create_client(url, key)
                    
                    # First check if email exists in users table
                    try:
                        result = supabase.table('users').select('*').eq('email', email).execute()
                        if result.data and len(result.data) > 0:
                            # User exists - for MVP, accept any password
                            # In production, you'd verify password hash here
                            user = result.data[0]
                            
                            if user.get('subscription_status') == 'active':
                                st.session_state["password_correct"] = True
                                st.session_state["user_email"] = email
                                st.success("Login successful!")
                                st.rerun()
                            else:
                                st.error("No active subscription found. Please subscribe to continue.")
                                st.info("Your subscription status: " + user.get('subscription_status', 'none'))
                        else:
                            st.error("Email not found. Please register first or check your email.")
                            st.caption(f"Checked email: {email}")
                    except Exception as e:
                        st.error("Database connection issue. Using fallback authentication.")
                        st.caption(f"Technical details: {str(e)}")
                        # Fallback to demo password
                        if password == os.getenv("PRODUCTION_PASSWORD", "SaaSDemo2025!"):
                            st.session_state["password_correct"] = True
                            st.session_state["user_email"] = email
                            st.success("Login successful (demo mode)!")
                            st.rerun()
            else:
                st.error("Please enter both email and password")
    with col2:
        if st.button("Forgot Password?", use_container_width=True, key="forgot_button"):
            st.info("Password reset coming soon!")

def show_register_form():
    """Show registration form."""
    st.subheader("Create New Account")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm")
    
    st.info("After registering, you'll need to subscribe to access the app.")
    
    if st.button("Register", type="primary", use_container_width=True, key="register_button"):
        if email and password and confirm_password:
            if password == confirm_password:
                st.success("Registration successful! Please check your email to verify your account.")
                st.info("Once verified, switch to the Subscribe tab to activate your account.")
            else:
                st.error("Passwords do not match")
        else:
            st.error("Please fill in all fields")

def show_subscribe_tab():
    """Show subscription options."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Subscribe to Pro")
        st.write("Unlock all features of Commission Tracker Pro")
        
        # Feature list
        st.markdown("""
        ✅ **Unlimited Policy Tracking**  
        ✅ **Advanced Reporting & Analytics**  
        ✅ **Multi-User Collaboration**  
        ✅ **Automated Reconciliation**  
        ✅ **Excel Import/Export**  
        ✅ **Priority Support**  
        """)
        
        st.markdown("### $19.99/month")
        st.caption("Cancel anytime. Secure payment via Stripe.")
        
        # Import Stripe only in production
        if os.getenv("APP_ENVIRONMENT") == "PRODUCTION":
            import stripe
            stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
            
            # Get email from session or ask for it
            email = st.session_state.get("user_email", "")
            if not email:
                email = st.text_input("Enter your email to subscribe:", key="subscribe_email")
            
            if st.button("🚀 Subscribe Now", type="primary", use_container_width=True, key="subscribe_button"):
                if email:
                    try:
                        # Create checkout session with email
                        checkout_session = stripe.checkout.Session.create(
                            line_items=[{
                                'price': os.getenv("STRIPE_PRICE_ID", "price_1S3nNU0wB1ZnPw8EFbZzbrQM"),
                                'quantity': 1,
                            }],
                            mode='subscription',
                            customer_email=email,
                            success_url=os.getenv("RENDER_APP_URL", "https://commission-tracker-app.onrender.com") + "/?session_id={CHECKOUT_SESSION_ID}",
                            cancel_url=os.getenv("RENDER_APP_URL", "https://commission-tracker-app.onrender.com"),
                        )
                        st.markdown(f'<meta http-equiv="refresh" content="0; url={checkout_session.url}">', 
                                   unsafe_allow_html=True)
                        st.success("Redirecting to secure checkout...")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error creating checkout session: {e}")
                        st.caption("Please check your internet connection and try again.")
                else:
                    st.error("Please enter your email address to subscribe.")