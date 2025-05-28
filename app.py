import streamlit as st
import pandas as pd
from pathlib import Path
from streamlit_option_menu import option_menu
from PIL import Image
from utils.data_utils import load_data
from utils.setup import initialize_session_state
from ui.style_app import styling_app ,render_app_header

initialize_session_state()
styling_app()
try:
    hero_image_path = Path("logo6.png")
    if hero_image_path.exists():
        hero_image = Image.open(hero_image_path)
    else:
        hero_image = None
except:
    hero_image = None

# Hero section
with st.container():
    col1, col2 = st.columns([3, 2])
    with col1:
        if hero_image:
            st.markdown('<div class="hero-image">', unsafe_allow_html=True)
            resized_image = hero_image.resize((800, 600))
            st.image(resized_image)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Add logo.jpg to your project folder for the hero image")
    with col2:
        st.markdown("""
            <div class="hero-text">
                <h1 style="font-family: 'Poppins', sans-serif; font-weight: 700; color: #548BA2;">
                    <span style="font-size: 6.5rem;">Smart</span><span style="font-size: 6rem;"> Analyzer</span>
                </h1>
                <p style="font-family: 'Poppins', sans-serif; font-size: 1.2rem; color: white;">
                    Upload your e-commerce or logistics data. Let AI uncover hidden insights in seconds.
                </p>
                <a href="#upload-section" style="
                    display: inline-block; padding: 10px 20px; margin-top: 10px;
                    font-family: 'Poppins', sans-serif; font-size: 1rem;
                    background-color: #6254d2; color: white; text-decoration: none;
                    border-radius: 8px;
                ">Try it</a>
            </div>
        """, unsafe_allow_html=True)

# Anchor for scrolling
st.markdown('<div id="upload-section"></div>', unsafe_allow_html=True)
st.markdown("---")



# ✅ Upload Section
st.markdown("### 📤 Upload your dataset")
uploaded_file = st.file_uploader("", type=["csv", "xlsx", "xls", "json", "parquet","jpg", "jpeg", "png"], label_visibility="collapsed")

# with st.sidebar:
#     st.markdown("### 📸 (Optional) Upload a Photo")
#     photo = st.file_uploader("Upload a photo (optional)", type=["jpg", "jpeg", "png"])
    

# if photo is not None:
#     st.image(photo, caption="Your photo", use_column_width=True)

if uploaded_file:  
    try:
        if st.session_state.df is None:
            with st.spinner("Loading your data..."):
                st.session_state.df = load_data(uploaded_file)
                st.session_state.original_df = st.session_state.df.copy()
                # if photo is not None:
                #     st.session_state.df = load_img(photo)
                #     st.session_state.original_df = st.session_state.df.copy()
               
                # Reset analysis state when new data is uploaded
                st.session_state.crew_analysis_done = False
            
            st.success("✅ Data uploaded successfully! You can now access it from other pages.")

        # Collapsible Data Preview
        # Collapsible Data Preview
        if st.session_state["df"] is not None:
            df = st.session_state["df"]
            # 🔍 Data Preview Expander
            with st.expander("🔍 Click to Preview Your Data"):
                st.write("### Data Preview")
                st.dataframe(df.head())

            # 📝 Optional Column Descriptions Expander
            with st.expander("📝 Optional: Describe Your Data Columns"):
                st.markdown("### Provide Column Descriptions")
                st.info("You can provide a brief description for each column. This helps AI understand the context.")

                for col in df.columns:
                    desc = st.text_input(
                        f"Description for '{col}'",
                        value=st.session_state.column_descriptions.get(col, "")
                    )
                    st.session_state.column_descriptions[col] = desc
                    

        else:
            st.warning("⚠️ No data available. Please upload or load a DataFrame first.")


    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
# Show current data status
if st.session_state.df is not None:
    st.info(f"📊 Current dataset has {st.session_state.df.shape[0]} rows and {st.session_state.df.shape[1]} columns")

# UI Header
render_app_header()
