"""
Minimal CSS styling for mobile compatibility
"""

import streamlit as st


def get_custom_css():
    """Get minimal CSS that doesn't interfere with mobile."""
    return """<style>
        /* Form styling - yellow inputs */
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea,
        .stDateInput input,
        .stSelectbox > div[data-baseweb="select"] {
            background-color: #fff3b0 !important;
            border: 2px solid #e6a800 !important;
            border-radius: 6px !important;
        }
        
        /* Mobile improvements */
        @media (max-width: 768px) {
            /* Scrollable tables */
            .stDataFrame {
                overflow-x: auto !important;
            }
            
            /* Prevent iOS zoom */
            input, select, textarea {
                font-size: 16px !important;
            }
        }
        </style>"""


def apply_css():
    """Apply minimal CSS styling."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)