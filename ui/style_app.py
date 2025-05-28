import streamlit as st
def styling_app():
   

    # Set the page configuration
    st.set_page_config(page_title="Smart Data Analyst", layout="wide")

    st.markdown("""
    <style>
        .stApp {
            background-color: #010b14;
            color: white;
        }

        .hero {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            padding: 4rem 3rem 2rem 3rem;
            background-color: #001f3f;
        }

        .hero-text {
            padding-left: 3rem;
        }

        .hero-text h1 {
            font-size: 4rem;
            font-weight: bold;
            color: white;
        }

        .hero-text p {
            font-size: 1.2rem;
            color: #e0e0e0;
            margin-top: 1rem;
            margin-bottom: 2rem;
        }

        .hero-button {
            background-color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-size: 1.1rem;
            color: 5100ff;
            cursor: pointer;
            text-decoration: none;
        }

        .hero-image img {
            width: 100%;
            max-width: 600px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(209, 0, 255, 0.3);
        }
        
        .card {
            background-color: #111;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0px 10px 20px rgba(0,255,255,0.2);
            transition: transform 0.3s ease-in-out;
        }
        .card:hover {
            transform: scale(1.05);
            box-shadow: 0px 15px 30px rgba(0, 255, 255, 0.4);
            
        }
        .card a {
            text-decoration: none;
            display: block;
            margin-top: 15px;
            padding: 10px;
            background-color: #6254d2;
            color: white;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)
    
def render_app_header():
    st.markdown("<h2 style='text-align: center; color: white;'>How it works</h2>", unsafe_allow_html=True)

# Creating One Row with Three Columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="card">
                <div style="font-size: 40px;">📊</div>
                <h3 style="color: white;">Dashboard</h3>
                <p style="color: #aaa;">See your dashboard and view real-time analytics.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Open Dashboard", key="dash_btn", use_container_width=True):
            st.switch_page(r"D:\data\data\cdata\pages\dashboard.py")

    with col2:
        st.markdown("""
            <div class="card">
                <div style="font-size: 40px;">💬</div>
                <h3 style="color: white;">ChatBot</h3>
                <p style="color: #aaa;">chat with data.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Open ChatBot", key="chat_btn", use_container_width=True):
            st.switch_page(r"D:\data\data\cdata\pages\chatbot.py")

    with col3:
        st.markdown("""
            <div class="card">
                <div style="font-size: 40px;">📤</div>
                <h3 style="color: white;">EDA</h3>
                <p style="color: #aaa;">show EDA analysis in data .</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Open EDA", key="eda_btn", use_container_width=True):
            st.switch_page(r"D:\data\data\cdata\pages\eda.py")

    # Divider before new row
    st.markdown("---")

    # New centered row for Predictive Analytics
    center1, center2, center3 = st.columns([1, 2, 1])

    with center2:
        st.markdown("""
            <div class="card">
                <div style="font-size: 40px;">🧠</div>
                <h3 style="color: white;">Predictive Analytics</h3>
                <p style="color: #aaa;">Let AI help you train and choose your model.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Open Assistant", key="predict_btn", use_container_width=True):
            st.switch_page(r"D:\data\data\cdata\pages\predictive.py")
