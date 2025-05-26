import streamlit as st

def render_dashboard_header():
    """Render the dashboard header."""
    st.markdown('<div class="dashboard-header">', unsafe_allow_html=True)
    st.title("📊 Advanced Data Analysis Dashboard")
    st.markdown("</div>", unsafe_allow_html=True)


def render_data_metrics(df):
    """Render metrics about the dataset."""
    metrics_row = st.container()
    with metrics_row:
        cols = st.columns(4)
        with cols[0]:
            st.metric("Total Rows", f"{df.shape[0]:,}")
        with cols[1]:
            st.metric("Total Columns", df.shape[1])
        with cols[2]:
            num_cols = len(df.select_dtypes(include='number').columns)
            st.metric("Numeric Columns", num_cols)
        with cols[3]:
            cat_cols = len(df.select_dtypes(include=['object', 'category']).columns)
            st.metric("Categorical Columns", cat_cols)