import streamlit as st

def apply_custom_styles_chat():
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
        .chat-container {
            flex-grow: 1;
            overflow-y: auto;
            padding: 20px;
            background-color: #010b14;
            border-radius: 10px;
        }
        .user-message {
            background-color: #0044cc;
            color: white;
            padding: 12px;
            border-radius: 8px;
            margin: 5px;
            text-align: right;
            width: fit-content;
        }
        .bot-message {
            background-color: #0055ff;
            color: white;
            padding: 12px;
            border-radius: 8px;
            margin: 5px;
            text-align: left;
            width: fit-content;
        }
        .input-container {
            width: 100%;
            padding: 15px;
            background-color: navy;
            border-radius: 8px;
            position: fixed;
            bottom: 0;
        }
        /* Make the input box text white */
        label {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Full-Screen Container
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# Title (Centered)
    st.markdown("<h1 style='text-align: center; color: white;'>Chat with Your Data</h1>", unsafe_allow_html=True)

