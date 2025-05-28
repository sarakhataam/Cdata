from crewai import Task
import json

def create_question_generation_task(agent, df_summary):
    """Create a task for generating analytical questions."""
    return Task(
        description=f"""
        Analyze the dataset and generate 10 business-relevant data analysis questions.
        
        Dataset Summary:
        {json.dumps(df_summary, indent=2)}
        
        VERY IMPORTANT REQUIREMENTS:
        - Generate exactly 10 specific, focused data analysis questions
        - Use the EXACT column names as provided in the dataset - do not change capitalization, spacing, or punctuation
        - The column names are: {', '.join([f'"{col}"' for col in df_summary['columns']])}
        - Refer to columns using their exact names with proper quotes (e.g., if a column is named "Customer ID" or "date of birth", use those exact names)
        - Create questions that can be answered with visualizations
        - Ensure questions are specific and actionable (e.g., "What is the relationship between 'Total Sales' and 'Region'?" rather than "Analyze sales data")
        - Questions should uncover trends, distributions, outliers, and useful insights
        - Make sure each question uses the exact column names that exist in the dataset
        - Create a diverse set of questions that would benefit from different visualization types 
        - YOU MUST create the questions with meaning and simple
        - YOU MUST Avoid using non-informative identifier and index columns such as id, customer id, customer number or any similar fields that do not provide analytical value.

        Format your response as a numbered list:
        1. [Question 1]
        2. [Question 2]
        etc.
        """,
        agent=agent,
        expected_output="A numbered list of 10 analytical questions about the dataset"
    )

def create_visualization_task(agent, df_summary, dependency_task):
    """Create a task for generating visualizations."""
    return Task(
        description=f"""
        Create Plotly visualizations to answer each analysis question.
        
        Dataset Summary:
        {json.dumps(df_summary, indent=2)}
        
        Analysis Questions:
        {{generate_questions_task}}
        
        VERY IMPORTANT INSTRUCTIONS:
        - Use the EXACT column names as provided in the dataset - do not change capitalization, spacing, or punctuation
        - The columns are: {', '.join([f'"{col}"' for col in df_summary['columns']])}
        - When accessing dataframe columns, use df["column name"] syntax for ALL columns, especially those with spaces or special characters
        - NEVER use df.column_name notation as it will fail with spaces in column names
        - Choose the most appropriate chart type for each question - don't use the same chart type repeatedly
        - Include clear titles, proper axis labels
        - Each visualization must be a separate function named viz_1, viz_2, etc.
        - Each function must accept a 'df' parameter and return the figure object
        - Use only pandas, numpy, and plotly libraries
        - Do not use fig.show() as this won't work in Streamlit
        - Use subplots where appropriate to show multiple related visualizations 
        - Implement faceting (small multiples) when comparing across categories when you nead in the same visulization and handel
            - Use 'xy' for: bar, scatter, histogram, box, etc.
            - Use 'domain' for: pie charts.
            - For treemap, sunburst, heatmap: omit the type key (use an empty dictionary).
        - Use animations for time-series data when appropriate
        - Include trendlines, reference lines, and annotations to highlight insights
        - Here is the dataset structure and sample info_summary And the first few rows: head
        - never use any name out of column names
        - must check code is right or not
        - if using cut function you must use astype(str) after that or any another type
        - if using qcut function you must use astype(str) after that or any another type
        - handel null value and datatype during plot
        - Replace zero values in a column with a small number (e.g., 0.01) to prevent division by zero errors during ratio calculations.
        - If the data contains any column related to date or time (such as columns with names including 'date', 'time', 'day', 'month', or 'year'), you MUST sort the dataframe in ascending order by that column before creating any visualization, but only if the column's data type is numerical or datetime (not object or string)
        -If there’s a column that represents date-related strings like months of the year or days of the week, make sure to sort them in their natural chronological order (e.g., January to December ) before plotting. This helps the visualization make more sense and improves readability.
        - YOU MUST use df = df.copy() inside the functions to avoid modifying the original dataframe.
        DIVERSE VISUALIZATION REQUIREMENTS:
        Use ALL of these visualization types where appropriate:
        
        1. STANDARD CHARTS:
           - BAR CHARTS (vertical/horizontal): For categorical comparisons, counts, aggregations
           - LINE CHARTS: For time series, trends over continuous variables
           - SCATTER PLOTS: For relationships between numerical variables
           - PIE/DONUT CHARTS: For part-to-whole relationships (limit to 5-7 categories)
           - HISTOGRAMS: For distribution of numerical data
           - BOX PLOTS: For distribution characteristics and outliers
           - HEATMAPS: For correlation matrices, density, or two-category comparisons
           - TREEMAPS: For hierarchical data
           - SUNBURST CHARTS: For multi-level hierarchical data
           
        
        The dataset is already loaded as 'df'. Return clean, executable Plotly code only.
        When you create the visualization functions, always access columns using df["column name"] syntax, never df.column_name
        return only code without commands, markdown and so on 
        """,
        agent=agent,
        dependencies=[dependency_task],
        expected_output="Python code with visualization functions that answer the analysis questions" 
    )