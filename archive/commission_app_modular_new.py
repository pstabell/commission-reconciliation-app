"""
Commission Management Application - Modular Architecture
Main entry point with bulletproof page routing and error handling.
"""

import streamlit as st
st.set_page_config(layout="wide")

import traceback
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import utilities with error handling
try:
    from utils.database import load_policies_data, get_database_engine
    from utils.styling import apply_css
    from utils.helpers import safe_page_execution
    from pages.page_router import route_to_page
    from column_mapping_config import (
        column_mapper, get_mapped_column, get_ui_field_name, 
        is_calculated_field, safe_column_reference
    )
except ImportError as e:
    st.error(f"  Critical error loading application modules: {e}")
    st.error("Please ensure all required files are present and try refreshing.")
    st.stop()


def initialize_app():
    """Initialize the application with error handling."""
    try:
        # Apply CSS styling
        apply_css()
        
        # Load data with caching
        all_data = load_policies_data()
        engine = get_database_engine()
        
        return all_data, engine
        
    except Exception as e:
        st.error(f"  Error initializing application: {e}")
        st.error("The application cannot start properly. Please contact support.")
        
        with st.expander("=' Technical Details"):
            st.code(traceback.format_exc())
        
        st.stop()


def create_navigation():
    """Create the sidebar navigation with error handling."""
    try:
        page = st.sidebar.radio(
            "Navigation", [
                "Dashboard",
                "Reports",
                "All Policies in Database",
                "Edit Policies in Database", 
                "Add New Policy Transaction",
                "Search & Filter",
                "Admin Panel",
                "Tools",
                "Accounting",
                "Help",
                "Policy Revenue Ledger",
                "Policy Revenue Ledger Reports",
                "Pending Policy Renewals"
            ]
        )
        return page
        
    except Exception as e:
        st.error(f"Error creating navigation: {e}")
        return "Dashboard"  # Fallback to Dashboard


def display_app_status():
    """Display application status and health information."""
    with st.sidebar:
        st.divider()
        
        # App status
        st.success("=â Modular Architecture Active")
        
        # Debug info (only show if debug mode is enabled)
        if st.session_state.get('debug_mode', False):
            st.write("**Debug Info:**")
            st.write(f"" Python modules loaded: ")
            st.write(f"" Database connection: ")
            st.write(f"" Error handling: ")
            
        # Toggle debug mode
        if st.checkbox("Enable Debug Mode", key="debug_mode_toggle"):
            st.session_state['debug_mode'] = True
        else:
            st.session_state['debug_mode'] = False


def main():
    """Main application entry point with comprehensive error handling."""
    
    # Initialize session state for error tracking
    if 'app_errors' not in st.session_state:
        st.session_state.app_errors = []
    
    # Global error handler
    try:
        # Initialize the application
        all_data, engine = initialize_app()
        
        # Create navigation
        page = create_navigation()
        
        # Display app status
        display_app_status()
        
        # Route to the selected page with error isolation
        if page:
            route_to_page(page, all_data, engine)
        else:
            st.error("No page selected")
            
    except Exception as e:
        # Global error handler - should never reach here if individual modules work correctly
        st.error("=¨ **Critical Application Error**")
        st.error("The application encountered an unexpected error.")
        
        error_details = {
            'error': str(e),
            'traceback': traceback.format_exc(),
            'timestamp': str(st.session_state.get('current_time', 'unknown'))
        }
        
        st.session_state.app_errors.append(error_details)
        
        st.write("**Error Recovery Options:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("= Refresh App"):
                st.rerun()
                
        with col2:
            if st.button("<à Go to Dashboard"):
                st.session_state.clear()
                st.rerun()
                
        with col3:
            if st.button("=Þ Contact Support"):
                st.write("Please report this error to your system administrator.")
        
        # Show error details for debugging
        with st.expander("=' Error Details (for technical support)"):
            st.code(error_details['traceback'])
            
        # Prevent complete app crash
        st.stop()


if __name__ == "__main__":
    main()