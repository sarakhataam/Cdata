import streamlit as st
from utils.setup import initialize_session_state
from ui.dashboard_2 import  render_data_metrics
from ui.visualizations import execute_visualization_code
from core.crew import run_crew_analysis
from utils.data_utils import create_data_summary
import io 
import plotly.io as pio
from ui.styles_dashboard import apply_custom_styles
st.set_page_config(page_title="Dashboard", layout="wide")

initialize_session_state()
apply_custom_styles()
def main():
    
    if st.session_state.df is not None:
        st.subheader("📊 Data Overview")
        render_data_metrics(st.session_state.df)
        
        st.subheader("🚀 AI-Powered Visualizations")
        if not st.session_state.crew_analysis_done:
            df_summary = create_data_summary(st.session_state.df)
            questions, viz_code = run_crew_analysis(df_summary)
            st.session_state.questions = questions
            st.session_state.viz_code = viz_code
            st.session_state.crew_analysis_done = True

        execute_visualization_code(st.session_state.viz_code, st.session_state.df)

        
        col1, col2, col3,col4 = st.columns(4)
        with col1:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.switch_page("app.py")
        
        with col2:
            if st.button("💬 Open ChatBot", use_container_width=True):
                st.switch_page(r"chatbot.py")
        
        with col3:
            if st.button("🔄 Regenerate", use_container_width=True):
                html_buf = io.StringIO()
                st.session_state.figs = []
                st.session_state.crew_analysis_done = False
                st.rerun()

        pio.templates.default = "seaborn"        
        with col4:
            html_buf = io.StringIO()
            for fig in st.session_state.figs:
                fig.update_layout(template="presentation") 
                html_buf.write(pio.to_html(fig, full_html=False, include_plotlyjs='cdn'))
            html_content = f"""
                            <html>
                            <head>
                                <meta charset="utf-8">
                                <title>Visualizations</title>
                            </head>
                            <body>
                                {html_buf.getvalue()}
                            </body>
                            </html>
                            """
            st.download_button(
                label="⬇️ Download (HTML)",
                data=html_content,
                file_name="visualizations.html",
                mime="text/html",
            )
                
    else:
        st.warning("⚠️ No data found! Please upload your dataset first.")
        st.info("👆 Go to the main page to upload your CSV or Excel file.")
        
        if st.button("🏠 Go to Upload Page", use_container_width=True):
            st.switch_page("app.py")

if __name__ == "__main__":
    main()