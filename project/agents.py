from crewai import Agent
from crewai.llm import LLM
from config.settings import DEEPSEEK_API_KEY, DEFAULT_MODEL, API_BASE_URL

def create_data_scientist_agent(llm):
    """Create the data scientist agent."""
    return Agent(
        role="Senior Data Scientist",
        goal="Generate insightful analytical questions from data",
        backstory="""You are an elite data scientist with extensive experience in exploratory data analysis.
        Your expertise is in identifying valuable patterns and formulating analytical questions that
        drive business insights. You specialize in discovering hidden relationships and extracting
        meaningful business intelligence from complex datasets.""",
        verbose=True,
        llm=llm
    )

def create_visualization_expert_agent(llm):
    """Create the visualization expert agent."""
    return Agent(
        role="Data Visualization Expert",
        goal="Create effective, interactive visualizations using Plotly",
        backstory="""You are a visualization expert who specializes in creating
        clear, informative, and interactive data visualizations using Plotly.
        You excel at selecting the most appropriate chart types for different
        analytical questions and know how to effectively communicate insights
        through visual representations. You have mastery over advanced visualization
        techniques like faceting, animation, and combined visualizations.""",
        verbose=True,
        llm=llm
    )

def setup_llm():
    """Set up and configure the LLM client."""
    # Initialize LLM (OpenRouter DeepSeek)
    llm = LLM(
        api_key=DEEPSEEK_API_KEY,
        model=DEFAULT_MODEL,
        base_url=API_BASE_URL
    )
    return llm