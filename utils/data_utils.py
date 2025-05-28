import pandas as pd
import io
from core.photos import extracted_table
import streamlit as st

def load_data(uploaded_file):
    try:
        # Determine file type and read
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.xls'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            df = pd.read_json(uploaded_file)
        elif uploaded_file.name.endswith('.parquet'):
            df = pd.read_parquet(uploaded_file)
        elif uploaded_file.name.endswith('.feather'):
            df = pd.read_feather(uploaded_file)
        elif uploaded_file.name.endswith('.pkl'):
            df = pd.read_pickle(uploaded_file)
        elif uploaded_file.name.endswith('.pickle'):
            df = pd.read_pickle(uploaded_file)
        elif uploaded_file.name.endswith('.png') or uploaded_file.name.endswith('.jpg') or uploaded_file.name.endswith('.jpeg'):
            df = extracted_table(uploaded_file)

        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
        
        return df
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")

# def load_img(img):
#     try:
#         if img.name.endswith('.png') or img.name.endswith('.jpg') or img.name.endswith('.jpeg'):
#             df = extracted_table(img)     
#         else:
#             raise ValueError("Unsupported file format. Please upload a png ,jpg or jpeg .")    
#         return df
#     except Exception as e:
#         raise Exception(f"Error loading data: {str(e)}")

def create_data_summary(df):
    
    info_buffer = io.StringIO()
    df.info(buf=info_buffer)
    info_summary = info_buffer.getvalue()
    exact_columns = list(df.columns)
    description_column =st.session_state.column_descriptions
    print("Column Descriptions:", description_column)
    summary = {
        "info": info_summary,
        "description": {
            "numerical": df.describe(include='number').to_dict() if not df.select_dtypes(include='number').empty else {},
            "categorical": df.describe(include='object').to_dict() if not df.select_dtypes(include='object').empty else {}
        },
        "head": df.head(5).to_dict(orient="records"),
        "columns": exact_columns,
        "column_descriptions": description_column
    }
    return summary