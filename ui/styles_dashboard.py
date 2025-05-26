import streamlit as st

def apply_custom_styles():
    """Apply custom styles to the Streamlit app."""
    st.markdown("""
    <style>
        body {
            background-color: #010b14; /* Dark navy */
            color: white;
        }
        .main-container {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: #010b14;
            padding: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# Full-Screen Container
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
