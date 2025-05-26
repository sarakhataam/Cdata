import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from ui.styles_dashboard import apply_custom_styles
from utils.setup import initialize_session_state


st.set_page_config(page_title="EDA Report", layout="wide")
initialize_session_state()

apply_custom_styles()


def main():
    st.title("📋 Exploratory Data Analysis Report")

    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("Please upload data from the Dashboard page first.")
        return

    try:
        if not st.session_state.generate_eda:
            st.session_state.profile = ProfileReport(st.session_state.df, explorative=True)
            st.session_state.generate_eda = True
        st_profile_report(st.session_state.profile)
    except Exception as e:
        st.error(f"Error generating report: {e}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("app.py")
    
    with col2:
        if st.button("💬 Open ChatBot", use_container_width=True):
            st.switch_page("chatbot.py")
    
    with col3:
        if st.button("🔄 Regenerate", use_container_width=True):
            st.session_state.generate_eda = False
            st.rerun()
                
  
if __name__ == "__main__":
    main()