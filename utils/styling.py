"""
CSS styling utilities for Commission Management Application
"""

import streamlit as st


@st.cache_data
def get_custom_css():
    """Get cached CSS for better performance."""
    return """<style>        /* Remove default padding and maximize main block width */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            margin-left: 240px !important;
            width: calc(100vw - 240px) !important;
            max-width: calc(100vw - 240px) !important;
        }
        
        /* Ensure main content area starts after sidebar */
        .main {
            margin-left: 240px !important;
            width: calc(100vw - 240px) !important;
            max-width: calc(100vw - 240px) !important;
        }
        
        /* Additional targeting for content wrapper */
        [data-testid="stAppViewContainer"] > .main {
            margin-left: 240px !important;
            width: calc(100vw - 240px) !important;
        }
          /* Force all main content to respect sidebar space */
        section.main {
            margin-left: 240px !important;
            width: calc(100vw - 240px) !important;
        }
        
        /* Target the root app container - this is critical! */
        [data-testid="stAppViewContainer"] {
            margin-left: 240px !important;
            width: calc(100vw - 240px) !important;
            max-width: calc(100vw - 240px) !important;
        }
        
        /* Also target the main header area */
        [data-testid="stHeader"] {
            margin-left: 240px !important;
            width: calc(100vw - 240px) !important;
        }
        
        /* Force sidebar to be permanently visible and disable all collapse functionality */
        section[data-testid="stSidebar"] {
            min-width: 240px !important;
            max-width: 240px !important;
            width: 240px !important;
            display: block !important;
            visibility: visible !important;
            position: fixed !important;
            left: 0 !important;
            top: 0 !important;
            height: 100vh !important;
            z-index: 999 !important;
            transform: translateX(0px) !important;
            margin-left: 0px !important;
        }
        
        /* Force sidebar to stay expanded even when marked as collapsed */
        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(0px) !important;
            margin-left: 0px !important;
            left: 0 !important;
        }
        
        /* Hide ALL possible collapse/hide buttons with comprehensive selectors */
        button[data-testid="collapsedControl"],
        button[kind="header"],
        [data-testid="stSidebarNav"] button[kind="header"],
        [data-testid="stSidebar"] button[kind="header"],
        [data-testid="stSidebar"] [data-testid="collapsedControl"],
        [data-testid="stSidebar"] button[title*="collapse"],
        [data-testid="stSidebar"] button[title*="hide"],
        [data-testid="stSidebar"] button[aria-label*="collapse"],
        [data-testid="stSidebar"] button[aria-label*="hide"],
        .stSidebar button[kind="header"],
        section[data-testid="stSidebar"] > div > button,
        section[data-testid="stSidebar"] button:first-child {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            width: 0 !important;
            height: 0 !important;
        }
        
        /* Ensure sidebar content is always visible */
        [data-testid="stSidebar"] > div {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        /* Force sidebar radio buttons to be visible */
        [data-testid="stSidebar"] .stRadio {
            display: block !important;
            visibility: visible !important;
        }
        
        /* Override any CSS that might hide the sidebar */
        [data-testid="stSidebar"] {
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        /* Remove extra margin from header/title */
        .main .block-container h1 {
            margin-bottom: 0.5rem;
        }
        /* Highlight all interactive input fields in Add New Policy Transaction form and Admin Panel rename headers */
        .stForm input:not([disabled]), .stForm select:not([disabled]), .stForm textarea:not([disabled]),
        .stTextInput > div > input:not([disabled]), .stNumberInput > div > input:not([disabled]), .stDateInput > div > input:not([disabled]),
        .stTextArea > div > textarea:not([disabled]) {
            background-color: #fff3b0 !important; /* Darker yellow */
            border: 2px solid #e6a800 !important; /* Darker yellow border */
            border-radius: 6px !important;
        }
        /* Make selectboxes match other fields and remove focus ring */
        .stSelectbox > div[data-baseweb="select"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        .stSelectbox > div[data-baseweb="select"]:focus,
        .stSelectbox > div[data-baseweb="select"]:active,
        .stSelectbox > div[data-baseweb="select"]:focus-visible {
            border: 2px solid #e6a800 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        /* Add yellow border to the client name search input at the top of Add New Policy Transaction */
        input[type="text"][aria-label="Type client name to search:"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Add yellow border to Premium Sold Calculator inputs */
        input[type="number"][aria-label="Existing Premium"],
        input[type="number"][aria-label="New/Revised Premium"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Add yellow border to Enter Premium Sold and see Agency Estimated Comm/Revenue (CRM) input */
        .stNumberInput input[type="number"], 
        [aria-label="Enter Premium Sold and see Agency Estimated Comm/Revenue (CRM)"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Highlight Date inputs */
        .stDateInput > div > input {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Ensure all text areas get yellow styling including void reason */
        .stTextArea textarea {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Target specific selectboxes from Add New Policy Transaction */
        [aria-label="Policy Type"] > div[data-baseweb="select"],
        [aria-label="Transaction Type"] > div[data-baseweb="select"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        /* Remove focus outline from selectboxes */
        [aria-label="Policy Type"] > div[data-baseweb="select"]:focus,
        [aria-label="Policy Type"] > div[data-baseweb="select"]:active,
        [aria-label="Policy Type"] > div[data-baseweb="select"]:focus-visible,
        [aria-label="Transaction Type"] > div[data-baseweb="select"]:focus,
        [aria-label="Transaction Type"] > div[data-baseweb="select"]:active,
        [aria-label="Transaction Type"] > div[data-baseweb="select"]:focus-visible {
            border: 2px solid #e6a800 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        </style>"""


def apply_css():
    """Apply custom CSS styling to the Streamlit app."""
    with st.container():
        st.markdown(get_custom_css(), unsafe_allow_html=True)