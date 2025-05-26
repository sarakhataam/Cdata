import re
from langchain import PromptTemplate, LLMChain
import streamlit as st
def generate_preprocessing_code(user_order, llm):
 
    template = """
    You are an expert Python data preprocessing assistant.

    Your task is to:
    ✅ Read the user's instruction.
    ✅ Generate clean, executable Python code to perform the requested preprocessing operation on a DataFrame called `df` (or the dataset in context).
    ✅ You are allowed to use any appropriate Python libraries or methods (such as `pandas`, `numpy`, `sklearn.preprocessing`, or others) — whichever best suits the task.
    ✅ Perform modifications inplace when possible. If not possible, reassign `df` or the specific column/variable.
    ✅ Do not provide explanations — just output the code.
    ✅ The user may ask you to merge two datasets: the original DataFrame named `df` and another one named `df2`. You must perform the merge according to the user's instructions and save the result back into `df`.

    ---

    📌 Example 1:
    User Order: "Drop the 'Age' column." or "Remove the 'Age' column." or "Delete the 'Age' column." or "امسح العمود بتاع العمر "

    Generated Code:
    ```python
    df.drop(columns=['Age'], inplace=True)
    ```

    📌 Example 2:
    User Order: "Standardize the 'Salary' column." or "normalize the 'Salary' column by using standardscaler "

    Generated Code:
    ```python
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    df['Salary'] = scaler.fit_transform(df[['Salary']])
    ```

    📌 Example 3:
    User Order: "Remove duplicate rows." or "Delete rows that appear more than once "  or "احذف التكرار" or "احذف الصفوف التي ظهرت اكثر من مرة"

    Generated Code:
    ```python
    df.drop_duplicates(inplace=True)
    ```

    📌 Example 4:
    User Order: "Encode the 'Gender' column using one-hot encoding."

    Generated Code:
    ```python
    df = pd.get_dummies(df, columns=['Gender'])
    ```

    📌 Example 5:
    User Order: "Convert the 'Date' column to datetime format and create a new column 'Year' from it."

    Generated Code:
    ```python
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    ```

    📌 Example 6:
    User Order: "Fill missing values in the 'Salary' column with the mean value."

    Generated Code:
    ```python
    mean_salary = df['Salary'].mean()
    df['Salary'].fillna(mean_salary, inplace=True)
    ```

    📌 Example 7:
    User Order: "Encode the 'Gender' column using label encoding."

    Generated Code:
    ```python
    from sklearn.preprocessing import LabelEncoder

    label_encoder = LabelEncoder()
    df['Gender'] = label_encoder.fit_transform(df['Gender'])
    ```

    📌 Example 8:
    User Order: "split the date column into year, month, and day columns." or "قسم عمود التاريخ الي يوم وشهر وسنة"

    Generated Code:
    ```python
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    ```

    📌 Example 9:
    User Order: "Merge df and df2 based on the 'ID' column." or "ادمج جدولين حسب العمود ID"

    Generated Code:
    ```python
    df = pd.merge(df, df2, on='ID')
    ```
    📌 Example 10:
    User Order: "Left join df with df2 using the 'UserID' column." or "left join the two tables based on the UserID column" or "left join the 2 datasets using UserID" or " left join عنطريق userIDادمج الجدولين باستخدام "

    Generated Code:
    ```python
    df = pd.merge(df, df2, on='UserID', how='left')
    ```
    📌 Example 11:
    User Order: "Concatenate the 2 datasets vertically" or "merge the 2 datasets row wise" or  "ادمج الجدولين بشكل عمودي او بالنسبة للصفوف"

    Generated Code:
    ```python
    df = pd.concat([df, df2], axis=0, ignore_index=True)
    ```
    📌 Example 12:
    User Order: "Concatenate df and df2 horizontally" or "merge the 2 datasets column wise" or "ادمج الجدولين بشكل افقي او بالنسبة للعمدان"

    Generated Code:
    ```python
    df = pd.concat([df, df2], axis=1)
    ```
    📌 Example 13:
    User Order: "Right join the first data and the second on 'ProductID'."
    Generated Code:
    ```python
    df = pd.merge(df, df2, on='ProductID', how='right')
    ```

    📌 Example 14:
    User Order: "Full outer join the 2 data on 'OrderID'."

    Generated Code:
    ```python
    df = pd.merge(df, df2, on='OrderID', how='outer')
    ```
    📌 Example 15:
    User Order: "Inner join the datasets or tables using 'CustomerID'."
    Generated Code:
    ```python
    df = pd.merge(df, df2, on='CustomerID', how='inner')
    ```

    📌 Example 16:
    User Order: "merge the datasets with hierarchical keys ['2023', '2024']." or "ادمج الجدولين مع تصنيف للسنة"
    Generated Code:
    ```python
    df = pd.concat([df, df2], keys=['2023', '2024'])
    ```

    📌 Example 17:
    User Order: "Merge the 2 tables on 'ID' and 'Name' columns."
    Generated Code:
    ```python
    df = pd.merge(df, df2, on=['ID', 'Name'])
    ```
    📌 Example 18:
    User Order: "Merge df and df2 on 'OrderID' keeping only entries from df (left join)."
    Generated Code:
    ```python
    df = pd.merge(df, df2, on='OrderID', how='left', indicator=True)
    ```
    📌 Example 19:
    User Order: "Merging Two Time Series DataFrames on Date" or "ادمج الجدولين بناء علي التاريخ باستخدام outer join"
    Generated Code:
    ```python
    df = pd.merge(df, df2, on='Date', how='outer')
    # Optional: sort by Date if needed
    df.sort_values('Date', inplace=True)
    ```
    📌 Example 20:
    User Order: "Replace "?" values with NaN in the dataset"

    Generated Code:
    ```python
    df.replace('?', np.nan, inplace=True)
    ```
    📌 Example 21: "replacing any symbol (symbol) that used to descripe missing data with NaN"
    Generated Code:
    ```python
    df.replace(`the symbol that user want to change`, np.nan, inplace=True)
    ```

    📌 Example 22: "remove nulls with knn imputer"
    Generated Code:
    ```python
    from sklearn.impute import KNNImputer

    imputer = KNNImputer(n_neighbors=5)
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    ```


    ---

    Now, process this user instruction and generate the corresponding Python code:

    User Order:
    {user_order}
    columns of df: {columns_names}
    columns of df2: {columns_names_2}
    Generated Code:
    """



    prompt = PromptTemplate(input_variables=["user_order"], template=template)
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    result = llm_chain.run({
        "user_order": user_order,
        "columns_names": ", ".join(st.session_state.df.columns.tolist()),
        "columns_names_2": ", ".join(st.session_state.df2.columns.tolist() if st.session_state.df2 is not None else [])
    })
    return result.strip()

def generate_graph(query_execution, user_question, llm):
    graph_prompt = """
        You are an expert data analyst, You have been given a Question and the Answer of it in a string format:
        Based on this Data in the Question and the Answer,

        Please perform the following tasks:
        1. **Convert this data into a properly formatted table with (COLUMN NAMES).** The table should be in Markdown format, suitable for direct inclusion in documentation.
        2. **Determine the most appropriate chart type to visualize this data:**
        3. **Write Python code using `plotly.express` and `pandas` to generate the chart.** 
         - **IMPORTANT: DO NOT use `.show()` or `fig.show()` in the code. Only generate the figure object.** The code should be accurate and ready to execute colourful with legend.
        4. **Generate insights from the data**
        
        **Important Guidelines:**
        - **IMPORTANT** you must reply from the prvioded data only.
        - Do Not creat new sample data .
        - **Return only the data table in Markdown format.** Label it as ## Data:.
        - **Return only the Python code for generating the chart.** Label it as ## Code:.
        - **Draw more than one chart if needed**.
        - **Do not include the chart type** in your response.
        - Important: If the data contains only one value, **You MUST not return any code for chart.**
        - **Generate insights from the data:**
          - **Data Overview:** Summarize the dataset in one row, including details such as the number of rows and columns, column names, and data types.
          - **Trends and Patterns:** Describe significant trends or patterns in the data.
          - **Anomalies and Outliers:** Identify and explain any anomalies or outliers in the data.
          - **Actionable Insights:** Provide actionable insights based on your analysis, Provide strategic, practical suggestions based on the findings.
          - IF the Question in arabic reply in arabic ELSE reply in english.
          - if "Sorry, I cannot process this request" in query_execution
             return "Sorry, I cannot process this request. Please ask a question related to data analysis."
                  The Question might be in Arabic, or English, you must reply in the same question language
        * if the question in arabic the output must be in arabic.
        * if the question in english the output must be in english.
        * do not mix between arabic and english.
        USE ## IN THE LABELS OF THE OUTPUT.

        Question: {user_question}
        prvioded data Answer: {query_execution}
    
    """
    prompt = PromptTemplate(input_variables=["user_question", "query_execution"], template=graph_prompt)
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    final_output = llm_chain.run({
        "user_question": user_question,
        "query_execution": query_execution
    })
    print("-----------------------------")
    print("final_output is important",final_output)
    return final_output

def extract_data_code_and_insights(final_output):
    data_pattern = r'## Data:\n\n([\s\S]+?)\n\n## Code:'
    code_pattern = r'## Code:\n\n```python\n([\s\S]+?)\n```'
    insights_pattern = r'## Insights:\n\n([\s\S]+)'
    data_match = re.search(data_pattern, final_output, re.DOTALL)
    data_string = data_match.group(1).strip() if data_match else 'No data found.'
    code_match = re.search(code_pattern, final_output, re.DOTALL)
    code_string = code_match.group(1).strip() if code_match else ''
    insights_match = re.search(insights_pattern, final_output, re.DOTALL)
    insights_string = insights_match.group(1).strip() if insights_match else 'No insights found.'
    return data_string, code_string, insights_string
