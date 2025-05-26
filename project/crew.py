import re
from crewai import Crew, Process
from core.agents import setup_llm, create_data_scientist_agent, create_visualization_expert_agent
from core.tasks import create_question_generation_task, create_visualization_task

def setup_crew(df_summary):
    """
    Set up the CrewAI with agents and tasks.
    
    Args:
        df_summary: A dictionary containing dataset summary information
        
    Returns:
        crew: The configured CrewAI instance
    """
    try:
        # Initialize LLM
        llm = setup_llm()
        
        # Create agents
        data_scientist = create_data_scientist_agent(llm)
        visualization_expert = create_visualization_expert_agent(llm)
        
        # Create tasks
        generate_questions_task = create_question_generation_task(data_scientist, df_summary)
        create_visualizations_task = create_visualization_task(
            visualization_expert, 
            df_summary, 
            generate_questions_task
        )
        
        # Create the crew
        crew = Crew(
            agents=[data_scientist, visualization_expert],
            tasks=[generate_questions_task, create_visualizations_task],
            process=Process.sequential,
            verbose=1
        )
            
        return crew
    except Exception as e:
        print(f"Error setting up CrewAI: {str(e)}")
        raise

def extract_questions(questions_text):
    """
    Extract questions from the AI output.
    
    Args:
        questions_text: Raw text containing the questions
        
    Returns:
        List of extracted questions
    """
    pattern = r'(?:\d+\.|\-)\s*(.*?)(?=(?:\d+\.|\-)|$)'
    matches = re.findall(pattern, questions_text, re.DOTALL)

    if not matches:
        raise ValueError("No questions found in the AI output.")

    # Format and extract the questions
    questions = [match.strip() for match in matches if match.strip()]
    return questions[:10]  # Ensure we have at most 10 questions

def extract_visualization_code(raw_output):
    """
    Extract code between triple backticks from the AI output.
    
    Args:
        raw_output: Raw text output from visualization agent
        
    Returns:
        Extracted code as a string
    """
    # Extract code between triple backticks
    match = re.search(r"```(?:python)?\n(.*?)```", raw_output, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return raw_output.strip()  # fallback to full output

def run_crew_analysis(df_summary):
    """
    Run the CrewAI analysis on the dataset.
    
    Args:
        df_summary: A dictionary containing dataset summary information
        
    Returns:
        tuple: (questions, visualization_code)
    """
    try:
        # Set up the crew
        crew = setup_crew(df_summary)
        
        # Kick off the crew's work
        crew.kickoff()
        
        # Extract questions
        questions_text = str(crew.tasks[0].output).strip() if crew.tasks[0].output is not None else ""
        questions = extract_questions(questions_text)
        
        # Extract visualization code
        viz_code = ""
        if hasattr(crew.tasks[1], 'output') and crew.tasks[1].output is not None:
            raw_output = str(crew.tasks[1].output)
            viz_code = extract_visualization_code(raw_output)
            
        return questions, viz_code
        
    except Exception as e:
        print(f"Error in crew analysis: {str(e)}")
        return [], ""