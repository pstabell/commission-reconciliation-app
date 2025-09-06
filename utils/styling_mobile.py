"""
Mobile-friendly CSS styling for Commission Management Application
"""

import streamlit as st


@st.cache_data(ttl=60)  # Short cache to allow updates
def get_custom_css():
    """Get cached CSS for better performance with mobile support."""
    return """<style>
        /* Base styles for all devices */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        
        .main .block-container h1 {
            margin-bottom: 0.5rem;
        }
        
        /* Desktop styles - fixed sidebar */
        @media (min-width: 769px) {
            .main .block-container {
                padding-left: 1.5rem;
                padding-right: 1.5rem;
            }
            
            /* Keep sidebar visible on desktop */
            section[data-testid="stSidebar"] {
                width: 240px !important;
                min-width: 240px !important;
            }
        }
        
        /* Mobile styles - collapsible sidebar */
        @media (max-width: 768px) {
            /* Smaller padding on mobile */
            .main .block-container {
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
            
            /* Make data tables scrollable */
            .stDataFrame {
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
            }
            
            /* Prevent zoom on iOS when focusing inputs */
            input, select, textarea {
                font-size: 16px !important;
            }
            
            /* Full width buttons on mobile */
            .stButton > button {
                width: 100% !important;
            }
            
            /* Stack columns vertically on mobile */
            [data-testid="column"] {
                width: 100% !important;
                flex: 0 0 100% !important;
            }
        }
        
        /* Form styling - yellow inputs */
        .stForm input:not([disabled]), 
        .stForm select:not([disabled]), 
        .stForm textarea:not([disabled]),
        .stTextInput > div > input:not([disabled]), 
        .stNumberInput > div > input:not([disabled]), 
        .stDateInput > div > input:not([disabled]),
        .stTextArea > div > textarea:not([disabled]),
        .stSelectbox > div[data-baseweb="select"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        
        /* Remove focus outlines from styled elements */
        .stSelectbox > div[data-baseweb="select"]:focus,
        .stSelectbox > div[data-baseweb="select"]:active {
            border: 2px solid #e6a800 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        </style>"""


def apply_css():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)