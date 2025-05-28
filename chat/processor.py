# Function to clean user question
import re
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from textblob import TextBlob
import streamlit as st


def clean_command(pandas_command):
   return pandas_command.replace('```python\n', '').replace('\n```', '').strip()
# Function to generate query
def generate_query(data_summary, user_question,llm,df):
    template="""
        You are an AI specialized in generating pandas commands from natural language questions.
        Given a user question, provide a valid pandas command.
        
        - UNDERSTAND THE data_summary WELL
        - The available sammary in the data frame "df" are: {data_summary}
        - Return ONLY THE COMMAND.
        - The data frame name is "df".
        - IF the User asks you in Arabic, reply with the command.
        - DO NOT REPLY TO ANY QUESTION THAT DOESN'T RELATE TO THE DATA OR PANDAS COMMANDS.
        - THE USER COULD ASK YOU TO RETURN MORE THAN ONE COMAND RETURN .
        - if No single pandas command can directly calculate the answer to the question, you must return multiple commands.
        - if A more complex solution is needed, you must involve multiple steps.
        - using any functions like groupby, mean, sum, count, etc. is allowed. you must return commandas that be suitable for the question.
        - IMPORTANT if the question is related to visualization, you must return the pandas command that return the data that can be used to draw the graph.
        - YOU MUST NOT return any code related to visualization, just return the pandas command.

        return code in this format :
        ```python
        #your code here
        ```
        example:
        what is the mean of age ?
        ```python
        df['age'].mean()
        ```

        Question: {question}
        Pandas Command:

        """
   
    prompt = PromptTemplate(input_variables=["question","data_summary"],template=template)
    llm_chain = LLMChain(prompt=prompt,llm=llm)

    cleaned_command = ""
    command_output = ""
    execution_output = ""
    result = None  # Initialize result to None
    try:
        # Use the existing llm_chain to get the pandas command
        pandas_command = llm_chain.run({
            "question": user_question,
            "data_summary": str(data_summary)
        })
        # Clean the command
        cleaned_command = clean_command(pandas_command)

        command_output = f"Formatted Pandas Command:\n{cleaned_command}"

        # Execute the command
        exec_locals = {'df': df}
        exec(f"result = {cleaned_command}", globals(), exec_locals)
        result = exec_locals.get('result', 'No result found')

        execution_output = f"Execution Result:\n{result}"
       
    except Exception as e:
        command_output = cleaned_command
        execution_output = f"Error in executing command: {str(e)}"

    # Return command_output and execution_output
    return command_output, execution_output
  

# Decision making function - Classifies user input as question (1) or preprocessing instruction (2)
def decision_making(user_input, llm):
    template = """
        You are a decision-making assistant.

        Your task is to classify the following user input into one of these two categories:

        - Return **1** if the input is a **question about the data** or a **data query** or **any input related to visulization**.
        📌 Example:
            - "What is the average sales per month?"
            - "Show me the number of missing values in the dataset."
            - "How many records do we have for 2023?"
            - "What is the total sales for each city?"
            - "draw pie chart for the 'Category' column."

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
        
        # print(f"Error executing code:\n{e}")
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