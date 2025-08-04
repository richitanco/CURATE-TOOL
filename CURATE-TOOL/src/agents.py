"""
Agent definitions for CrewAI Content Curator
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import OPENAI_MODEL, GEMINI_MODEL, TEMPERATURE, GOOGLE_API_KEY, OPENAI_API_KEY
from .tools import search_tool, gemini_tool, scrape_tool, quality_tool


# Configure LLMs
openai_llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=TEMPERATURE,
    openai_api_key=OPENAI_API_KEY
)

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=TEMPERATURE
)


# Define agents
topic_analyzer = Agent(
    role='Topic Analysis Expert',
    goal='Analyze educational topics and define clear learning objectives',
    backstory="""You are an expert instructional designer with 20 years of experience. 
    You excel at breaking down complex topics into manageable components and 
    defining SMART learning objectives.""",
    verbose=True,
    allow_delegation=False,
    llm=openai_llm
)

web_researcher = Agent(
    role='Web Research Specialist',
    goal='Find comprehensive and reliable information about topics',
    backstory="""You are a digital research expert skilled in finding the best 
    online sources. You know how to evaluate source credibility and extract 
    relevant information.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, scrape_tool],
    llm=openai_llm
)

content_analyst = Agent(
    role='Deep Content Analyst',
    goal='Perform deep analysis and generate educational insights',
    backstory="""You are an expert analyst who uses advanced AI capabilities 
    to understand complex topics, identify connections, and create high-quality 
    educational content.""",
    verbose=True,
    allow_delegation=False,
    tools=[gemini_tool],
    llm=openai_llm
)

quality_controller = Agent(
    role='Quality Assurance Expert',
    goal='Ensure content quality and pedagogical effectiveness',
    backstory="""You are a quality control expert with skills in detecting 
    inaccurate or outdated information. Your mission is to ensure educational 
    excellence.""",
    verbose=True,
    allow_delegation=False,
    tools=[quality_tool],
    llm=openai_llm
)

content_curator = Agent(
    role='Educational Content Curator',
    goal='Organize and structure content for optimal learning',
    backstory="""You are an expert curator who creates effective learning 
    structures. You know how to organize information for progressive and 
    meaningful learning.""",
    verbose=True,
    allow_delegation=False,
    llm=openai_llm
)