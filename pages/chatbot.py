import streamlit as st
from ui.styles_chatbot import apply_custom_styles_chat
from chat.functions import process_chat_input
import pandas as pd
import plotly.express as px
from utils.setup import get_llm,initialize_session_state
from utils.data_utils import load_data
import time
st.set_page_config(page_title="AI Chatbot", layout="wide")

apply_custom_styles_chat()
initialize_session_state()

def render_chat_interface():
    """Render the chat interface"""
    st.subheader("🤖 AI Data Assistant")
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        if st.session_state.chat_history:
            
            for i, message in enumerate(st.session_state.chat_history):
                if message["role"] == "user":
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(message["content"])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(message["content"])
                        # Display visualization if it exists in the message
                        if "visualization_code" in message:
                            try:
                                exec_locals = {'df': st.session_state.df, 'pd': pd, 'px': px}
                                exec(message["visualization_code"], {'pd': pd, 'px': px}, exec_locals)
                                if 'fig' in exec_locals:
                                    st.plotly_chart(exec_locals['fig'], use_container_width=True,key=f"plot_{i}")
                            except Exception as e:
                                print(f"Error displaying visualization from chat: {str(e)}")
    user_input = st.chat_input("Ask about your data or request preprocessing...")
    
    return user_input

def main():

    # Collapsible Data Preview (if data exists in session state)
    if st.session_state.df is not None:
        # Create a title and reset button side by side
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown("### 🔍 Click to Preview Your Data")
        with col2:
            if st.button("🔄 Reset to Original", key="reset_data_btn"):
                st.session_state.df = st.session_state.original_df.copy()
                msg_placeholder = st.empty()
                # Show the success message
                msg_placeholder.success("✅ Done")
                time.sleep(1)
                msg_placeholder.empty()

        # The actual data preview inside an expander
        col1, col2 = st.columns(2)

        with col1:
            with st.expander("📄 Preview", expanded=False):
                st.dataframe(st.session_state["df"].head(), use_container_width=True)

        with col2:
            with st.expander("ℹ️ Data Info", expanded=False):
                buffer = st.session_state["df"].info(buf=None)
                # Capture and print the info
                import io
                buffer = io.StringIO()
                st.session_state["df"].info(buf=buffer)
                s = buffer.getvalue()
                st.text(s)
    else:
        st.info("📭 No data uploaded. Go to the Home page to upload a dataset.")


    # Sidebar: Upload file and save in session_state["df2"]
    with st.sidebar:
        st.markdown("### 📤 Upload Your second Data")
        uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls", "json", "parquet"])
        if uploaded_file is not None:
            try:
                st.session_state.df2 = load_data(uploaded_file)
                st.session_state.original_df2 = st.session_state.df2.copy()
                
                st.success(f"✅ Uploaded: `{uploaded_file.name}`")
            except Exception as e:
                st.error(f"❌ Failed to read file: {e}")
    
    if st.session_state.df2 is not None:
        st.markdown("### 🔍 Preview of second Data")
        with st.expander("📄 Click to expand"):
            print(st.session_state["df2"].head())
            st.dataframe(st.session_state["df2"].head(), use_container_width=True)


    
    user_input = render_chat_interface()
    llm = get_llm()
    if user_input:
        process_chat_input(user_input,llm)
        st.rerun()
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("app.py")
    
    with col2:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.switch_page(r"D:\data\data\cdata\pages\dashboard.py")
    
    with col3:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    main()