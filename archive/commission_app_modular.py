"""
Modular Commission App - Main Application File
This is the refactored main application that imports and coordinates all page modules.
"""
import streamlit as st
import logging
import traceback

# Configure Streamlit page
st.set_page_config(
    page_title="Sales Commission Tracker", 
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('commission_app.log'),
        logging.StreamHandler()
    ]
)

# Import utility modules
try:
    from utils.database import initialize_database, load_all_data
    from utils.styling import apply_css
    from utils.helpers import load_help_content
    from column_mapping_config import column_mapper, get_mapped_column, get_ui_field_name, is_calculated_field, safe_column_reference
except ImportError as e:
    st.error(f"Failed to import utility modules: {e}")
    st.stop()

# Import page modules
try:
    from pages.dashboard import show_dashboard
    from pages.reports import show_reports
    from pages.all_policies import show_all_policies
    from pages.edit_policies import show_edit_policies
    from pages.add_policy import show_add_policy
    from pages.search_filter import show_search_filter
    from pages.admin_panel import show_admin_panel
    from pages.accounting import show_accounting
    from pages.help import show_help
    from pages.policy_revenue_ledger import show_policy_revenue_ledger
    from pages.policy_revenue_reports import show_policy_revenue_reports
    from pages.pending_renewals import show_pending_renewals
except ImportError as e:
    st.error(f"Failed to import page modules: {e}")
    st.info("Please ensure all page modules are properly installed.")
    st.stop()

def main():
    """Main application function."""
    try:
        # Initialize database
        initialize_database()
        
        # Apply CSS styling
        apply_css()
        
        # App header
        st.title("💰 Sales Commission Tracker")
        st.markdown("*Modular Architecture - Professional Commission Management System*")
        
        # Sidebar navigation
        st.sidebar.markdown("### 🧭 Navigation")
        
        # Page selection
        page = st.sidebar.radio(
            "Select Page:",
            [
                "Dashboard",
                "Reports", 
                "All Policies in Database",
                "Edit Policies in Database",
                "Add New Policy Transaction",
                "Search & Filter",
                "Admin Panel",
                "Accounting",
                "Help",
                "Policy Revenue Ledger",
                "Policy Revenue Ledger Reports", 
                "Pending Policy Renewals"
            ],
            key="main_navigation"
        )
        
        # Debug information (optional)
        show_debug = st.sidebar.checkbox("Show Debug Info", value=False)
        if show_debug:
            all_data = load_all_data()
            st.sidebar.markdown("### 🐛 Debug Info")
            st.sidebar.write(f"Data shape: {all_data.shape}")
            st.sidebar.write(f"Selected page: {page}")
            st.sidebar.write(f"Session state keys: {list(st.session_state.keys())}")
        
        # Page routing with error handling
        st.sidebar.markdown("---")
        
        try:
            if page == "Dashboard":
                show_dashboard()
            elif page == "Reports":
                show_reports()
            elif page == "All Policies in Database":
                show_all_policies()
            elif page == "Edit Policies in Database":
                show_edit_policies()
            elif page == "Add New Policy Transaction":
                show_add_policy()
            elif page == "Search & Filter":
                show_search_filter()
            elif page == "Admin Panel":
                show_admin_panel()
            elif page == "Accounting":
                show_accounting()
            elif page == "Help":
                show_help()
            elif page == "Policy Revenue Ledger":
                show_policy_revenue_ledger()
            elif page == "Policy Revenue Ledger Reports":
                show_policy_revenue_reports()
            elif page == "Pending Policy Renewals":
                show_pending_renewals()
            else:
                st.error(f"Unknown page: {page}")
                
        except Exception as page_error:
            st.error(f"❌ Error loading page '{page}': {str(page_error)}")
            
            if show_debug:
                st.markdown("### 🔍 Error Details")
                st.code(traceback.format_exc())
            
            st.info("💡 Try refreshing the page or contact support if the problem persists.")
            logging.error(f"Page error in {page}: {str(page_error)}")
            logging.error(traceback.format_exc())
        
        # Footer information
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ℹ️ App Info")
        st.sidebar.caption("**Version:** 2.0 Modular")
        st.sidebar.caption("**Architecture:** Bulletproof Modular Design")
        st.sidebar.caption("**Last Updated:** 2025-07-01")
        
        # Quick stats in sidebar
        try:
            all_data = load_all_data()
            if not all_data.empty:
                st.sidebar.markdown("### 📊 Quick Stats")
                st.sidebar.metric("Total Policies", f"{len(all_data):,}")
                
                customer_col = get_mapped_column("Customer") or "Customer"
                if customer_col in all_data.columns:
                    unique_customers = all_data[customer_col].nunique()
                    st.sidebar.metric("Unique Customers", f"{unique_customers:,}")
        except Exception:
            pass  # Silently fail for quick stats
            
    except Exception as main_error:
        st.error(f"❌ Critical application error: {str(main_error)}")
        st.info("Please check the application logs and contact support.")
        logging.critical(f"Critical error in main(): {str(main_error)}")
        logging.critical(traceback.format_exc())

def handle_page_errors(page_function, page_name):
    """Error handler wrapper for page functions."""
    try:
        page_function()
    except Exception as e:
        st.error(f"❌ Error in {page_name}: {str(e)}")
        logging.error(f"Error in {page_name}: {str(e)}")
        logging.error(traceback.format_exc())
        
        with st.expander("🔍 Error Details", expanded=False):
            st.code(traceback.format_exc())

if __name__ == "__main__":
    # Application entry point
    try:
        # Log application startup
        logging.info("Commission App (Modular) starting up...")
        
        # Run main application
        main()
        
        # Log successful startup
        logging.info("Commission App (Modular) started successfully")
        
    except Exception as startup_error:
        st.error("❌ Failed to start the application")
        st.error(f"Error: {str(startup_error)}")
        logging.critical(f"Startup error: {str(startup_error)}")
        logging.critical(traceback.format_exc())
        
        # Emergency fallback
        st.markdown("### 🚨 Emergency Information")
        st.markdown("""
        The application failed to start properly. Here are some troubleshooting steps:
        
        1. **Check Dependencies**: Ensure all required packages are installed
        2. **Database Connection**: Verify the database file is accessible
        3. **File Permissions**: Check that the application has proper file permissions
        4. **Module Imports**: Ensure all page modules are in the correct directories
        
        **Directory Structure Expected:**
        ```
        commission_app_modular.py
        utils/
        ├── __init__.py
        ├── database.py
        ├── helpers.py
        └── styling.py
        pages/
        ├── __init__.py
        ├── dashboard.py
        ├── reports.py
        ├── all_policies.py
        ├── edit_policies.py
        ├── add_policy.py
        ├── search_filter.py
        ├── admin_panel.py
        ├── accounting.py
        ├── help.py
        ├── policy_revenue_ledger.py
        ├── policy_revenue_reports.py
        └── pending_renewals.py
        column_mapping_config.py
        ```
        
        **Contact Support**: If issues persist, check the logs in `commission_app.log`
        """)