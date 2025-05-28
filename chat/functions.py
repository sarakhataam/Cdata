import streamlit as st
import pandas as pd
import plotly.express as px
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Import custom modules
from ui.dashboard import render_dashboard_header
from ui.styles_chatbot import apply_custom_styles_chat
from utils.data_utils import load_data, create_data_summary
from core.crew import run_crew_analysis
from chat.processor import (
    generate_query, 
    decision_making, 
    execute_preprocessing_code, 
    non_serious_response
)
from chat.explorer import explore_data
from chat.generator import (
    generate_preprocessing_code, 
    generate_graph, 
    extract_data_code_and_insights
)
from utils.data_utils import load_data, create_data_summary
def process_chat_input(user_input, llm):
    """Process user chat input and generate response"""
    if not user_input or st.session_state.df is None:
        return
    
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Determine input type
    input_type = decision_making(user_input, llm)
    
    if input_type == "1":  # Question about data
        with st.spinner("🤔 Analyzing your question..."):
            try:
                # Get data columns
                data_summary = create_data_summary(st.session_state.df)
                # Generate query results

                query_output, query_execution = generate_query(data_summary, user_input, llm, st.session_state.df)
                # Generate graph and insights
                print("Query Output:", query_output)
                # print("Query Execution:", query_execution)
                graph_output = generate_graph(query_execution, user_input, llm)
                print("Graph Output:", graph_output)
                data_string, code_string, insights_string = extract_data_code_and_insights(graph_output)
                # Prepare response
                if insights_string != 'No insights found.':
                    response = f"### Analysis Results\n\n{data_string}\n\n### Insights\n\n{insights_string}"
                else:
                    response = f"### Analysis Results\n\n{data_string}"

                message_data = {"role": "assistant", "content": response}
                if code_string:
                    message_data["visualization_code"] = code_string
                
                st.session_state.chat_history.append(message_data)
                
            except Exception as e:
                error_msg = f"❌ Error analyzing your question: {str(e)}"
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
    
    elif input_type == "2":  # Preprocessing instruction
        with st.spinner("⚙️ Processing your instruction..."):
            try:
                # Generate preprocessing code
                preprocessing_code = generate_preprocessing_code(user_input, llm)
                # print("Generated Preprocessing Code:", preprocessing_code)
                # Execute preprocessing code
                st.session_state.df = execute_preprocessing_code(st.session_state.df,st.session_state.df2, preprocessing_code)
                st.session_state.preprocessing_df = True
                
            except Exception as e:
                error_msg = f"❌ **Error in preprocessing:** {str(e)}\n\nPlease try rephrasing your request or check your data."
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
    
    elif input_type == "3":  # Non-serious response
        with st.spinner("🤖 Soltan is thinking..."):
            try:
                response = non_serious_response(user_input, llm)
                formatted_response = f"🎭  {response}"
                st.session_state.chat_history.append({"role": "assistant", "content": formatted_response})
            except Exception as e:
                st.session_state.chat_history.append({"role": "assistant", "content": "🤖 I'm having trouble understanding that. Can you ask about your data instead?"})
    
    else:
        error_msg = "🤔 I couldn't understand your request. Please ask a question about your data or request a preprocessing operation."
        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
