import streamlit as st
import pandas as pd
from ui.styles_predictive import style_custom_predictive
from utils.setup import initialize_session_state
from machine_learning.static_predict import static_ml
import pickle
# Set full-screen layout
st.set_page_config(page_title="Chat with Your Data", layout="wide")


style_custom_predictive()
initialize_session_state()

# UI Constants
classification_models = [
    "LogisticRegression", "RandomForestClassifier", "DecisionTreeClassifier", "SVC",
    "KNeighborsClassifier", "GradientBoostingClassifier", "AdaBoostClassifier", "ExtraTreesClassifier"
]

regression_models = [
    "LinearRegression", "RandomForestRegressor", "DecisionTreeRegressor", "SVR",
    "KNeighborsRegressor", "ElasticNet", "GradientBoostingRegressor", "AdaBoostRegressor"
]

clustering_models = [
    "KMeans", "X_scaled", "DBSCAN", "X_scaled", "CMeans"
]

# Main logic
if st.session_state.df is None:
    st.warning("Please upload data from the Dashboard page first.")
else:
    try:
        columns = st.session_state.df.columns.tolist()
        all_options = columns + ["no target"]

        # Target column selection
        with st.expander("Select a target column"):
            target_column = st.selectbox("Choose a target column:", all_options, key="target_column")

        # Conditional display of next expander
        if target_column:
            with st.expander("Select a problem type"):
                problem_type = st.selectbox(
                    "Choose the type of ML problem:",
                    ["Classification", "Regression", "Clustering"],
                    key="problem_type"
                )

            if problem_type:
                with st.expander("Select a model"):
                    if problem_type == "Classification":
                        model_name = st.selectbox("Choose a classification model:", classification_models, key="model_choice")
                    elif problem_type == "Regression":
                        model_name = st.selectbox("Choose a regression model:", regression_models, key="model_choice")
                    elif problem_type == "Clustering":
                        model_name = st.selectbox("Choose a clustering model:", clustering_models, key="model_choice")
                    else:
                        model_name = None

                # Test size input
                split_ratio = st.number_input("Test size (optional)", min_value=0.0, max_value=1.0, value=0.2, step=0.05, key="split_ratio")

                # Train button
                if st.button("Train"):
                    st.success(f"Model `{model_name}` trained successfully on `{target_column}` with test size = {split_ratio}.")

                    # Placeholder for result
                    st.subheader("Model Results")
                    st.text("Accuracy, Score, or Summary would appear here after actual training logic.")

                    model, matrics = static_ml(
                        data=st.session_state.df,
                        target_column=target_column,
                        problem_type=problem_type,
                        model_name=model_name,
                        split_ratio=split_ratio
                    )


                    # Convert to DataFrame safely
                    df_result = pd.json_normalize(matrics).T
                    df_result.columns = ["Value"]
                    df_result.index = df_result.index.str.replace(r"^classification_report\.", "", regex=True)
                    df_result = df_result.reset_index()
                    df_result.columns = ["Metric", "Value"]

                    # Display the cleaned DataFrame
                    st.dataframe(df_result)



                    st.text("Model trained successfully. You can now test it with new data.")

                    st.session_state.model = model
                    st.session_state.matrics = matrics
                    
                if st.session_state.model is not None  and st.session_state.matrics is not None:   # Test input section
                    with st.expander("📝 Optional: test your model "):
                        st.markdown("### Provide test value")
                        st.info("You can provide a value for each column. This helps the model to train.")

                        for col in st.session_state.df.columns:
                            if col != target_column:
                                val = st.text_input(
                                    f"value for '{col}'",
                                    value=st.session_state.test_sample.get(col, ""),
                                    key=f"input_{col}"
                                )
                                st.session_state.test_sample[col] = val

                if st.button("Test Model"):
                    if not st.session_state.test_sample:
                        st.error("Please provide values for the test sample.")
                    else:
                        test_sample = st.session_state.test_sample
                        # Example: prediction = model.predict([test_sample])    
                        prediction = st.session_state.model.predict([list(test_sample.values())])
                        st.subheader("Test Results")
                        st.write("Prediction:", prediction)
                        # For demonstration, we will just show a placeholder result
                        st.success("Model tested successfully with the provided values.")

                    # # Placeholder for test result
                    # st.subheader("Test Results")
                    # st.text("Model prediction will appear here based on your input.")
                model_bytes = pickle.dumps(st.session_state.model)
                # Download button
                st.download_button(
                    label="Download Trained Model",
                    data=model_bytes,  # Replace with actual model binary
                    file_name="trained_model.pkl",
                    mime="application/octet-stream",
                    key="download_model"
                )

    except Exception as e:
        st.error(f"Error: {e}")
