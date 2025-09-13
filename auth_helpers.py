"""Authentication helpers for the SaaS version."""
import streamlit as st
from supabase import Client
import os
from datetime import datetime
import secrets
import string
import time

def check_subscription_status(email: str, supabase: Client) -> dict:
    """Check if user has active subscription."""
    try:
        result = supabase.table('users').select('*').ilike('email', email).execute()
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
    # Add CSS for form field styling and ELIMINATE vertical spacing
    st.markdown("""
    <style>
        /* Style all input fields with gray border */
        .stTextInput > div > div > input {
            border: 2px solid #cccccc !important;
            border-radius: 4px !important;
            padding: 8px 12px !important;
        }
        
        /* Make password fields match */
        input[type="password"] {
            border: 2px solid #cccccc !important;
            border-radius: 4px !important;
            padding: 8px 12px !important;
        }
        
        /* Hover effect */
        .stTextInput > div > div > input:hover,
        input[type="password"]:hover {
            border-color: #999999 !important;
        }
        
        /* Focus effect */
        .stTextInput > div > div > input:focus,
        input[type="password"]:focus {
            border-color: #666666 !important;
            outline: none !important;
        }
        
        /* NUCLEAR OPTION - Remove ALL padding and margins */
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100%;
        }
        
        /* Target ALL Streamlit containers */
        .css-18e3th9, .css-1d391kg, .css-12oz5g7, .css-1y0tads, .css-1629p8f,
        .css-k1vhr4, .css-1v3fvcr, .css-1kyxreq, .css-z5fcl1, .css-1n76uvr,
        [class*="css-"] {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }
        
        /* Override with specific small padding for main content */
        section.main > div {
            padding-top: 20px !important;
            padding-bottom: 20px !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        /* Force app view container to have no padding */
        div[data-testid="stAppViewContainer"] {
            padding: 0 !important;
        }
        
        /* Kill the header completely */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Target block container with extreme prejudice */
        [data-testid="block-container"] {
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Remove all element spacing */
        .element-container {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Target the stVerticalBlock containers */
        div[data-testid="stVerticalBlock"] > div {
            gap: 0 !important;
        }
        
        /* Remove spacing from all divs in main */
        .main div {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }
        
        /* Reduce space around tabs */
        .stTabs {
            margin-top: 0.25rem !important;
        }
        
        /* Reduce space in tab content */
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 0.5rem !important;
        }
        
        /* Reduce spacing between form elements */
        .stForm {
            padding: 0 !important;
            border: none !important;
        }
        
        /* Remove gray background and border from form containers */
        .stForm > div {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        /* Remove any borders from form wrapper */
        div[data-testid="stForm"] {
            border: none !important;
            background-color: transparent !important;
            box-shadow: none !important;
        }
        
        /* Reduce space between inputs */
        .stTextInput {
            margin-bottom: 0.5rem !important;
        }
        
        /* Reduce subheader margins */
        h3 {
            margin-top: 0 !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Reduce info/error message spacing */
        .stAlert {
            margin: 0.5rem 0 !important;
        }
        
        /* Reduce button spacing */
        .stButton {
            margin-top: 0.25rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Display logo inline with title - properly centered
    col1, col2, col3 = st.columns([1.2, 8, 2])  # Even closer
    with col1:
        try:
            logo_path = "Logo/3pMGFb-LogoMakr-300dpi COPY.jpeg"
            if os.path.exists(logo_path):
                st.image(logo_path, width=120)  # Triple the size
        except Exception:
            st.write("🔐")  # Fallback emoji
    
    with col2:
        # Add vertical spacing to center-align with logo
        st.write("")  # Empty line for spacing
        st.write("")  # Another empty line to bring text down more
        st.markdown("# Agent Commission Tracker")
    
    # Check if we should show password reset form
    if st.session_state.get('show_password_reset'):
        show_password_reset_form()
    else:
        # Check if we should show Subscribe tab directly (no tabs)
        if st.session_state.get('show_subscribe_tab', False):
            # Show subscribe form directly without tabs
            st.info("🚀 Start your 14-day free trial!")
            show_subscribe_tab()
            
            # Add link to go back to login
            st.markdown("---")
            if st.button("← Back to Login"):
                st.session_state.show_subscribe_tab = False
                st.query_params.clear()  # Clear the ?subscribe=true parameter
                st.rerun()
        else:
            # Normal tabs view - removed Register tab for clarity
            tab1, tab2 = st.tabs(["Login", "Start Free Trial"])
            
            with tab1:
                show_login_form()
            
            with tab2:
                show_subscribe_tab()
        
        # Add compact footer with legal links
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8em; padding: 5px 0; margin-top: 0.5rem;">
            <a href="?page=terms" style="color: #666;">Terms of Service</a> • 
            <a href="?page=privacy" style="color: #666;">Privacy Policy</a><br>
            © 2025 Metro Technology Solutions LLC. All rights reserved.<br>
            Agent Commission Tracker™ is a trademark of Metro Technology Solutions LLC.
        </div>
        """, unsafe_allow_html=True)

def show_login_form():
    """Show email/password login form."""
    st.subheader("Login to Your Account")
    
    # Use columns to control form width
    col1, col2 = st.columns([2, 3])
    with col1:
        with st.form("production_login_form"):
            email = st.text_input("Email", key="login_email", autocomplete="username")
            password = st.text_input("Password", type="password", key="login_password", autocomplete="current-password")
            
            submit = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submit:
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
                        
                        # First check if email exists in users table (case-insensitive)
                        try:
                            result = supabase.table('users').select('*').ilike('email', email).execute()
                            if result.data and len(result.data) > 0:
                                user = result.data[0]
                                # Use the email from database to preserve case
                                correct_email = user.get('email', email)
                                
                                # Check if user has set a password
                                if user.get('password_set', False) and user.get('password_hash'):
                                    # Verify password (for MVP, simple comparison - should hash in production!)
                                    if password == user.get('password_hash'):
                                        if user.get('subscription_status') == 'active':
                                            st.session_state["password_correct"] = True
                                            st.session_state["user_email"] = correct_email  # Use correct case from DB
                                            # Debug logging for mobile issue
                                            print(f"DEBUG auth_helpers: Login successful for {email}, stored as {correct_email}")
                                            print(f"DEBUG auth_helpers: Session state keys after login: {list(st.session_state.keys())}")
                                            st.success("Login successful!")
                                            st.rerun()
                                        else:
                                            st.error("No active subscription found. Please subscribe to continue.")
                                            st.info("Your subscription status: " + user.get('subscription_status', 'none'))
                                    else:
                                        st.error("Incorrect password. Please try again.")
                                else:
                                    # User hasn't set password yet
                                    st.error("Please set your password first. Check your email for the setup link.")
                                    st.info("If you haven't received it, use the 'Forgot Password?' button below.")
                            else:
                                st.error("Email not found. Please check your email address and try again.")
                                st.info("💡 **Tip**: Make sure you're using the same email address you used during signup. If you're still having trouble, use the 'Forgot Password?' button below.")
                                # Check if there's a similar email with different case
                                try:
                                    case_check = supabase.table('users').select('email').ilike('email', email).execute()
                                    if case_check.data:
                                        st.warning(f"Found account with email: {case_check.data[0]['email']} - Please use this exact email to login.")
                                except:
                                    pass  # Ignore errors in case check
                        except Exception as e:
                            st.error("Database connection issue. Using fallback authentication.")
                            st.caption(f"Technical details: {str(e)}")
                            # Fallback to demo password
                            if password == os.getenv("PRODUCTION_PASSWORD", "SaaSDemo2025!"):
                                # For demo, use the proper case
                                if email.lower() == 'demo@agentcommissiontracker.com':
                                    correct_email = 'Demo@AgentCommissionTracker.com'
                                else:
                                    correct_email = email
                                
                                st.session_state["password_correct"] = True
                                st.session_state["user_email"] = correct_email
                                # Debug logging for mobile issue
                                print(f"DEBUG auth_helpers: Fallback login successful for {email}, stored as {correct_email}")
                                print(f"DEBUG auth_helpers: Session state after fallback: {dict(st.session_state)}")
                                st.success("Login successful (demo mode)!")
                                st.rerun()
                else:
                    st.error("Please manually enter both email and password")
    
        # Forgot password button in same column as form
        if st.button("Forgot Password?", use_container_width=True, key="forgot_button"):
            st.session_state['show_password_reset'] = True
            st.rerun()

# Register form removed - users should use Start Free Trial instead
# def show_register_form():
#     """Show registration form."""
#     st.subheader("Create New Account")
#     
#     # Use columns to control form width - same as login form
#     col1, col2 = st.columns([2, 3])
#     with col1:
#         with st.form("register_form"):
#             email = st.text_input("Email", key="register_email")
#             password = st.text_input("Password", type="password", key="register_password")
#             confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm")
#             
#             st.info("After registering, you'll need to subscribe to access the app.")
#             
#             submit = st.form_submit_button("Register", type="primary", use_container_width=True)
#             
#             if submit:
#                 if email and password and confirm_password:
#                     if password == confirm_password:
#                         st.success("Registration successful! Please check your email to verify your account.")
#                         st.info("Once verified, switch to the Subscribe tab to activate your account.")
#                     else:
#                         st.error("Passwords do not match")
#                 else:
#                     st.error("Please fill in all fields")

def show_subscribe_tab():
    """Show subscription options."""
    # Left-aligned content, no centering columns
    st.subheader("Subscribe to Agent Commission Tracker")
    st.write("Unlock all features of Agent Commission Tracker")
    
    # Feature list
    st.markdown("""
    ✅ **Unlimited Policy Tracking**  
    ✅ **Advanced Reporting & Analytics**  
    ✅ **Multi-User Collaboration**  
    ✅ **Automated Reconciliation**  
    ✅ **Excel Import/Export**  
    ✅ **Priority Support**  
    """)
    
    st.markdown("### Start Your 14-Day Free Trial")
    st.markdown("Then $19.99/month")
    st.caption("No charge for 14 days. Cancel anytime. Secure payment via Stripe.")
    
    # Import Stripe only in production
    if os.getenv("APP_ENVIRONMENT") == "PRODUCTION":
        import stripe
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        
        # Email input and button in narrow column for consistent width
        col1, col2 = st.columns([2, 3])
        with col1:
            # Use form to properly capture autofilled values
            with st.form("subscribe_form"):
                # Always show email input for autofill/password manager compatibility
                email = st.text_input(
                    "Enter your email to subscribe:", 
                    value=st.session_state.get("user_email", ""),  # Pre-fill if logged in
                    key="subscribe_email",
                    autocomplete="email"  # Enable browser/password manager autofill
                )
                
                submit = st.form_submit_button("🚀 Start Free Trial", type="primary", use_container_width=True)
                
                if submit:
                    if email:
                        try:
                            # Create checkout session with 14-day free trial
                            checkout_session = stripe.checkout.Session.create(
                                line_items=[{
                                    'price': os.getenv("STRIPE_PRICE_ID"),
                                    'quantity': 1,
                                }],
                                mode='subscription',
                                customer_email=email,
                                subscription_data={
                                    'trial_period_days': 14,  # 14-day free trial
                                },
                                # Remove payment_method_collection - default behavior requires payment method
                                success_url=os.getenv("RENDER_APP_URL", "https://commission-tracker-app.onrender.com") + "/?session_id={CHECKOUT_SESSION_ID}",
                                cancel_url=os.getenv("RENDER_APP_URL", "https://commission-tracker-app.onrender.com"),
                                allow_promotion_codes=True,  # Enable coupon code field in checkout
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

def generate_reset_token(length=32):
    """Generate a secure random token for password reset."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_setup_token(length=32):
    """Generate a secure random token for initial password setup."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def show_password_reset_form():
    """Show password reset request form."""
    st.subheader("🔐 Reset Your Password")
    
    st.write("Enter your email address and we'll send you a link to reset your password.")
    
    # Use columns to control form width - same as other forms
    col1, col2 = st.columns([2, 3])
    with col1:
        with st.form("password_reset_form"):
            email = st.text_input("Email Address", key="reset_email")
            
            submit = st.form_submit_button("Send Reset Link", type="primary", use_container_width=True)
            
            if submit:
                if email:
                    # Create Supabase client
                    from supabase import create_client
                    url = os.getenv("PRODUCTION_SUPABASE_URL", os.getenv("SUPABASE_URL"))
                    key = os.getenv("PRODUCTION_SUPABASE_ANON_KEY", os.getenv("SUPABASE_ANON_KEY"))
                    
                    if not url or not key:
                        st.error("Database not configured.")
                        return
                        
                    supabase = create_client(url, key)
                    
                    # Check if email exists in users table (case-insensitive)
                    try:
                        result = supabase.table('users').select('email').ilike('email', email).execute()
                        
                        if result.data:
                            # Generate reset token
                            reset_token = generate_reset_token()
                            
                            # Store token in database (expires in 1 hour)
                            from datetime import datetime, timedelta
                            expires_at = (datetime.utcnow() + timedelta(hours=1)).isoformat()
                            
                            token_data = {
                                'email': email.lower(),  # Store lowercase to match users table
                                'token': reset_token,
                                'expires_at': expires_at
                            }
                            
                            try:
                                supabase.table('password_reset_tokens').insert(token_data).execute()
                                
                                # Generate reset link
                                app_url = os.getenv("RENDER_APP_URL", "https://commission-tracker-app.onrender.com")
                                reset_link = f"{app_url}?reset_token={reset_token}"
                                
                                # Try to send email
                                try:
                                    from email_utils import send_password_reset_email
                                    email_sent = send_password_reset_email(email, reset_link)
                                    
                                    if email_sent:
                                        st.success("✅ Password reset link sent! Check your email.")
                                        st.info("The link will expire in 1 hour.")
                                    else:
                                        # Fallback: show the link if email fails
                                        st.warning("Email service not configured. Use this link to reset your password:")
                                        st.code(reset_link)
                                        st.caption("This link will expire in 1 hour.")
                                except Exception as e:
                                    # Fallback: show the link if email fails
                                    st.warning("Email service not configured. Use this link to reset your password:")
                                    st.code(reset_link)
                                    st.caption("This link will expire in 1 hour.")
                                    
                            except Exception as e:
                                st.error(f"Error creating reset token: {e}")
                                st.info("Please ensure the password_reset_tokens table exists in your database.")
                        else:
                            # Don't reveal if email exists or not (security best practice)
                            st.success("✅ If that email exists in our system, you'll receive a reset link shortly.")
                            
                    except Exception as e:
                        st.error(f"Database error: {e}")
                else:
                    st.error("Please enter your email address.")
        
        # Back button in same column as form
        if st.button("← Back to Login", key="back_to_login"):
            del st.session_state['show_password_reset']
            st.rerun()

def show_password_reset_completion(reset_token: str):
    """Show form to complete password reset."""
    st.title("🔐 Set New Password")
    
    # Verify token is valid
    from supabase import create_client
    url = os.getenv("PRODUCTION_SUPABASE_URL", os.getenv("SUPABASE_URL"))
    key = os.getenv("PRODUCTION_SUPABASE_ANON_KEY", os.getenv("SUPABASE_ANON_KEY"))
    
    if not url or not key:
        st.error("Database not configured.")
        return
        
    supabase = create_client(url, key)
    
    try:
        # Check if token is valid
        result = supabase.table('password_reset_tokens').select('*').eq('token', reset_token).eq('used', False).execute()
        
        if result.data and len(result.data) > 0:
            token_data = result.data[0]
            
            # Check if expired
            from datetime import datetime
            expires_at = datetime.fromisoformat(token_data['expires_at'].replace('Z', '+00:00'))
            if expires_at < datetime.now(expires_at.tzinfo):
                st.error("This reset link has expired. Please request a new one.")
                if st.button("Back to Login"):
                    st.query_params.clear()
                    st.rerun()
                return
            
            # Show password reset form
            email = token_data['email']
            st.info(f"Setting new password for: {email}")
            
            # Use columns to control form width - same as other forms
            col1, col2 = st.columns([2, 3])
            with col1:
                with st.form("reset_completion_form"):
                    new_password = st.text_input("New Password", type="password", key="new_password")
                    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
                    
                    submit = st.form_submit_button("Set New Password", type="primary", use_container_width=True)
                    
                    if submit:
                        if new_password and confirm_password:
                            if new_password == confirm_password:
                                # In a real app, you'd hash the password here
                                # For MVP, we'll just store it (NOT SECURE - fix before production!)
                                try:
                                    # First check if user exists
                                    user_check = supabase.table('users').select('email').eq('email', email).execute()
                                    
                                    if not user_check.data:
                                        st.error("User account not found. Please contact support.")
                                        st.info("It appears your user account was deleted or not created properly.")
                                        return
                                    
                                    # Update user's password
                                    supabase.table('users').update({
                                        'password_hash': new_password,  # TODO: Hash this!
                                        'password_set': True
                                    }).eq('email', email).execute()
                                    
                                    # Mark token as used
                                    supabase.table('password_reset_tokens').update({
                                        'used': True
                                    }).eq('token', reset_token).execute()
                                    
                                    st.success("✅ Password updated successfully! You can now login with your new password.")
                                    # Auto redirect after success
                                    st.query_params.clear()
                                    time.sleep(2)
                                    st.rerun()
                                        
                                except Exception as e:
                                    st.error(f"Error updating password: {e}")
                            else:
                                st.error("Passwords do not match.")
                        else:
                            st.error("Please enter and confirm your new password.")
        else:
            st.error("Invalid or expired reset link. Please request a new password reset.")
            if st.button("Back to Login"):
                st.query_params.clear()
                st.rerun()
                
    except Exception as e:
        st.error(f"Error validating reset token: {e}")

def show_password_setup_form(setup_token: str):
    """Show form for new users to set their initial password."""
    st.title("🎉 Welcome to Agent Commission Tracker!")
    st.subheader("Set Your Password")
    
    # Verify token is valid
    from supabase import create_client
    url = os.getenv("PRODUCTION_SUPABASE_URL", os.getenv("SUPABASE_URL"))
    key = os.getenv("PRODUCTION_SUPABASE_ANON_KEY", os.getenv("SUPABASE_ANON_KEY"))
    
    if not url or not key:
        st.error("Database not configured.")
        return
        
    supabase = create_client(url, key)
    
    try:
        # Check if token is valid (using same table as password reset for simplicity)
        result = supabase.table('password_reset_tokens').select('*').eq('token', setup_token).eq('used', False).execute()
        
        if result.data and len(result.data) > 0:
            token_data = result.data[0]
            
            # Check if expired
            from datetime import datetime
            expires_at = datetime.fromisoformat(token_data['expires_at'].replace('Z', '+00:00'))
            if expires_at < datetime.now(expires_at.tzinfo):
                st.error("This setup link has expired. Please contact support.")
                return
            
            # Show password setup form
            email = token_data['email']
            st.info(f"Setting up account for: {email}")
            
            # Use columns to control form width - same as other forms
            col1, col2 = st.columns([2, 3])
            with col1:
                with st.form("password_setup_form"):
                    new_password = st.text_input("Create Password", type="password", key="setup_password")
                    confirm_password = st.text_input("Confirm Password", type="password", key="setup_confirm")
                    
                    st.caption("Password must be at least 8 characters long.")
                    
                    submit = st.form_submit_button("Set Password & Continue", type="primary", use_container_width=True)
                    
                    if submit:
                        if new_password and confirm_password:
                            if len(new_password) < 8:
                                st.error("Password must be at least 8 characters long.")
                            elif new_password == confirm_password:
                                # In a real app, you'd hash the password here
                                # For MVP, we'll just store it (NOT SECURE - fix before production!)
                                try:
                                    # First check if user exists
                                    user_check = supabase.table('users').select('email').eq('email', email).execute()
                                    
                                    if not user_check.data:
                                        st.error("User account not found. Please contact support.")
                                        st.info("It appears your user account was not created properly during signup.")
                                        return
                                    
                                    # Update user's password
                                    update_result = supabase.table('users').update({
                                        'password_hash': new_password,  # TODO: Hash this!
                                        'password_set': True
                                    }).eq('email', email).execute()
                                    
                                    # Mark token as used
                                    supabase.table('password_reset_tokens').update({
                                        'used': True
                                    }).eq('token', setup_token).execute()
                                    
                                    # Set session state to log them in automatically
                                    st.session_state["password_correct"] = True
                                    st.session_state["user_email"] = email
                                    
                                    st.success("✅ Password set successfully! Logging you in...")
                                    st.balloons()
                                    
                                    # Clear the setup token from URL and redirect to main app
                                    time.sleep(2)  # Brief pause to show success message
                                    st.query_params.clear()
                                    st.rerun()
                                        
                                except Exception as e:
                                    st.error(f"Error setting password: {e}")
                            else:
                                st.error("Passwords do not match.")
                        else:
                            st.error("Please enter and confirm your password.")
        else:
            st.error("Invalid or expired setup link.")
            st.info("If you're having trouble, please contact support.")
                
    except Exception as e:
        st.error(f"Error validating setup token: {e}")