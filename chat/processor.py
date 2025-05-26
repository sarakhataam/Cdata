# Function to clean user question
import re
import pandas as pd
from langchain import PromptTemplate, LLMChain
from textblob import TextBlob
import streamlit as st
def clean_user_question(question: str) -> str:
    question = question.strip()
    question = str(TextBlob(question).correct())
    if not question.endswith((".", "?", "!")):
        question += "?"
    return question

# Function to extract pandas commands
def extract_pandas_commands(code_string):
    code_string = code_string.strip()
    code_string = re.sub(r"```(?:python)?", "", code_string)
    code_string = code_string.replace("```", "")
    print(code_string)
    commands = [line.strip() for line in code_string.split('\n') if line.strip()]
    return commands

def process_query(user_question, data, llm_query):
    import pandas as pd
    cleaned_commands = []
    command_output = ''
    execution_output = ''
    try:
        pandas_command = llm_query.run(question=user_question)
        cleaned_code = pandas_command.replace('python\n', '').strip()
        command_list = extract_pandas_commands(cleaned_code)
        results = []
        exec_locals = {'df': data.copy(), 'pd': pd}
        for command in command_list:
            cleaned_commands.append(command)
            try:
                if command.strip().startswith("print(") and command.strip().endswith(")"):
                    command = command.strip()[6:-1]
                try:
                    result = eval(command, {}, exec_locals)
                except SyntaxError:
                    exec(command, {}, exec_locals)
                    result = exec_locals.get('result', 'Executed')
                results.append(f"{command}:\n{result}\n")
            except Exception as cmd_error:
                results.append(f"{command}:\nError: {str(cmd_error)}\n")
        command_output = "Formatted Pandas Commands:\n" + "\n".join(cleaned_commands)
        execution_output = "Execution Results:\n" + "\n".join(results)
    except Exception as e:
        command_output = "\n".join(cleaned_commands) if cleaned_commands else cleaned_code
        execution_output = f"Unexpected error: {str(e)}"
    return command_output, execution_output

# Function to generate query
def generate_query(data_columns, user_question, df, llm):
    query_prompt = f"""
      You are an expert AI assistant for translating natural language questions into valid pandas commands.
      Your task is to understand the user's intent and generate meaningful pandas code using the available DataFrame columns.

      **Data Context:**
      - The available columns in the DataFrame `df` are: {data_columns}
      - Carefully match keywords in the question to relevant column names.
      - If the column name is not explicitly mentioned but implied (e.g., "year" might relate to a date column like "invoice_date" or "Date"), make a best guess.
      - Handle temporal comparisons when users ask about trends, changes, or predictions across time (e.g., "percentage change from 2019 to 2020").
      - If missing or inconsistent data is detected, handle it gracefully to ensure valid calculations.

      **Instructions:**
      - Respond ONLY with valid Python pandas code using DataFrame `df`.
      - Ensure missing values are handled using `.fillna(0)` or `dropna()` where appropriate.
      - Use `groupby`, `mean()`, `sum()`, `pct_change()`, or `agg()` if the question implies summary/statistics by category or time.
      - Use `.dropna()` before applying `.pct_change()` to prevent invalid results.
      - If percentage change calculations lead to missing values, default to a simple moving average or linear trend for estimation.

      **Advanced Thinking:**
      - Support logical inference such as calculating the proportion or trend from one time period to another.
      - When the user asks for 'predict', 'project', expectation, or 'forecast', apply extrapolation techniques based on valid statistical trends (e.g., moving averages).
      - If historical trends cannot be established, notify the user with: `"Not enough data to make a reliable prediction."`
      - Do not attempt machine learning prediction unless explicitly requested.


      **Edge Cases:**
      - If the question is unclear or unrelated to available columns, respond with:
        `"Sorry, I cannot process this request. Please ask a question related to data analysis."`

      **User Question:** {{question}}

      **Pandas Command:**
    """
    prompt = PromptTemplate(
        input_variables=["question"],
        template=query_prompt,
    )
    llm_chain = LLMChain(
        prompt=prompt,
        llm=llm,
    )
    corrected_question = clean_user_question(user_question)
    command_output, execution_output = process_query(corrected_question, df, llm_chain)
    return command_output, execution_output

# Decision making function - Classifies user input as question (1) or preprocessing instruction (2)
def decision_making(user_input, llm):
    template = """
        You are a decision-making assistant.

        Your task is to classify the following user input into one of these two categories:

        - Return **1** if the input is a **question about the data** or a **data query**.
        📌 Example:
            - "What is the average sales per month?"
            - "Show me the number of missing values in the dataset."
            - "How many records do we have for 2023?"
            - "What is the total sales for each city?"

        - Return **2** if the input is an **instruction to preprocess the data**.
        📌 Example:
            - "Remove any rows with missing values."
            - "Normalize the 'Age' column."
            - "Convert the 'Date' column to datetime format."
            - "Create a new column 'Year' based on the 'Date' column."

        - Return **3** if the input is an **non serious response**.
        📌 Example:
            - "Okey"
            - "How are you?"
            - "Tell me a joke"
            - "What is your name?"
            - "تمام "
            - "عامل ايه ؟"
        ---

        User Input:
        {user_input}

        Your Response (1 or 2 or 3):
        """

    prompt = PromptTemplate(input_variables=["user_input"], template=template)
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    result = llm_chain.run({
        "user_input": user_input
    })
    return result.strip()


def execute_preprocessing_code(df,df2, code_string):
    """
    Cleans and executes the given preprocessing code string on the provided DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame to preprocess.
        code_string (str): The Python code to execute.

    Returns:
        pd.DataFrame: The modified DataFrame.
    """
    import re

    # Remove code fences and extra whitespace
    code_cleaned = re.sub(r"^```python|```$", "", code_string.strip(), flags=re.MULTILINE).strip()

    # Provide df in the local scope for exec
    local_vars = {'df': df, 'df2': df2}

    try:
        exec(code_cleaned, globals(), local_vars)
        st.session_state.chat_history.append({"role": "assistant", "content": "✅ Done preprocessing on your data"})
        # st.session_state.chat_history.append("✅ Done preprocessing on your data")
    except Exception as e:
        st.session_state.chat_history.append({"role": "assistant", "content": str(e)})
        
        print(f"Error executing code:\n{e}")
        return df  # Return original df if error occurs

    # Return the possibly modified DataFrame
    return local_vars['df']

# Function to response in non serious response
def non_serious_response(user_input,llm):
    template = f"""
        YOUR NAME IS "SOLTAN"
        You are Soltan a 25 years old as a data scientist with a professional yet friendly personality. You handle both serious financial inquiries and casual questions in a way that maintains an engaging conversation with the user. You’re expected to create a seamless transition between small talk and business-related topics. When casual or non-serious questions are asked, your responses should reflect your helpful, approachable identity.
        Guidelines:
            - The Question might be in Arabic, or English, you must reply in the same question language
                * if the question in arabic the output must be in arabic.
                * if the question in english the output must be in english.
                * do not mix between arabic and english.
            - You reply to any greeting, farewell, or question about your status (e.g., "How are you?", "Goodbye", "See you", "Bye", "Hi", "Hello", "What's up?", "How's it going?").
            - For casual questions, provide friendly and engaging responses. Keep the interaction light, but maintain your identity as a data expert.
            - When switching to serious financial questions, shift to a more professional tone while remaining approachable.
            - The question can be informal or formal, but ensure that your personality remains consistent across all responses.
            - Your responses should reinforce your role as a professional data scientist, without overwhelming the user with excessive formality in casual conversations.
        Example Responses:
        - "Hello": "Hello! How can I assist you with your data today?"
        - عامل ايه ؟:انا تمام الحمدلله انت عامل ايه؟
        - عندك كام سنة ؟ : انا عندي 25 سنة
        - اسمك ايه ؟ : انا اسمي سلطان تحب اساعدك ازاي ؟
        - "How old are you?": "I’m as old as the insights I provide—timeless!"
        - "What's your name?": "I’m Soltan, your digital data scientist, ready to help you manage your data!"
        - "Tell me a joke": "Why did the accountant break up with the calculator? It just didn’t add up!" or "ﻣﺮﺓ ﻣﺤﺎﺳﺐ ﺗﺠﻮﺯ ﻣﺤﺎﺳﺒﺔ ﻛﺘﺒﻮﺍ ﻛﺘﺎﺑﻬﻢ ﻋﻠﻰ ﺩﻓﺘﺮ"
        - For a business-related question: "Let's dive into the numbers. How can I assist you with your financials today?"
        -If a user asks: “How can you help me manage my data?”
            Please respond as follows: “I can help you by analyzing your data and making a preprocessing on your data”


        Question: {user_input}
        Provide an engaging, context-appropriate response based on the question.
        """
    prompt = PromptTemplate(input_variables=["user_input"],template=template)
    llm_chain = LLMChain(prompt=prompt,llm=llm)
    response = llm_chain.run({
        "user_input": user_input
    })

    return response