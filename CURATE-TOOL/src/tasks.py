"""
Task definitions for CrewAI Content Curator - Real Content Curation
"""
from typing import List
from crewai import Task

from .agents import (
    topic_analyzer,
    web_researcher,
    content_analyst,
    quality_controller,
    content_curator
)


def create_tasks_for_topic(topic: str) -> List[Task]:
    """
    Create all necessary tasks for content curation
    
    Args:
        topic: The educational topic to curate content for
        
    Returns:
        List of Task objects
    """
    
    # Task 1: Topic Analysis for Content Curation
    task_analyze = Task(
        description=f"""
        Analyze the topic '{topic}' to define what types of content to search for:
        1. Identify key subtopics and areas to cover
        2. Define search keywords in English and Spanish
        3. Determine what types of resources are most valuable (articles, tutorials, documentation, guides)
        4. Specify target audiences (beginner, intermediate, advanced)
        5. Create search strategy for both languages
        
        Focus on FINDING existing content, not creating new content.
        """,
        expected_output="Search strategy with keywords in English and Spanish, and content types to look for",
        agent=topic_analyzer
    )
    
    # Task 2: Web Research for Articles and Resources
    task_research = Task(
        description=f"""
        You MUST use the web_search tool to find REAL articles about '{topic}'.
        
        MANDATORY STEPS - Use web_search tool with these exact queries:
        1. web_search("{topic} tutorial")
        2. web_search("{topic} guide") 
        3. web_search("{topic} article")
        4. web_search("{topic} beginner")
        5. web_search("{topic} español")
        6. web_search("{topic} blog post")
        7. web_search("learn {topic}")
        
        For EACH search result returned by the web_search tool:
        - Copy the EXACT "link" field as the URL - DO NOT MODIFY IT
        - Copy the EXACT "title" field as the title
        - Extract the "snippet" for description
        
        NEVER create fake URLs like "http://example.com" or similar.
        Only use URLs that come directly from the web_search tool results.
        
        PRIORITIZE THESE TYPES OF CONTENT:
        1. **Blog articles and tutorials** (Medium, Dev.to, personal blogs)
        2. **Technical articles** from companies and experts  
        3. **Practical guides** with step-by-step instructions
        4. **How-to articles** with code examples
        
        AVOID:
        - University courses or academic papers
        - Paid courses or course platforms
        
        Find at least 15-20 REAL ARTICLES with working URLs.
        """,
        expected_output="List of REAL URLs with exact titles from web_search tool results",
        agent=web_researcher
    )
    
    # Task 3: Deep Content Analysis and Evaluation
    task_analyze_content = Task(
        description=f"""
        Analyze and evaluate each resource found for '{topic}':
        
        For EACH URL from the research, determine:
        1. **Content Quality** (1-10 score):
           - Accuracy and up-to-date information
           - Clarity of explanations
           - Practical examples included
           - Professional presentation
        
        2. **Educational Value** (1-10 score):
           - Completeness of coverage
           - Difficulty level appropriateness
           - Step-by-step guidance
           - Learning outcomes clarity
        
        3. **Credibility** (1-10 score):
           - Author expertise
           - Source reputation
           - References and citations
           - Community validation (comments, shares)
        
        4. **Target Audience**:
           - Beginner, Intermediate, or Advanced
           - Prerequisites mentioned
        
        5. **Content Type Classification**:
           - Quick Start Guide
           - Comprehensive Tutorial
           - Reference Documentation  
           - Practical Examples
           - Theoretical Explanation
        
        Provide detailed reasoning for each score.
        """,
        expected_output="Detailed evaluation of each resource with scores and classifications",
        agent=content_analyst,
        context=[task_research]
    )
    
    # Task 4: Quality Control and Filtering
    task_quality = Task(
        description="""
        Quality control and filtering of curated resources:
        
        1. **Remove duplicates** and very similar content
        2. **Filter out low-quality resources** (total score below 21/30)
        3. **Verify URLs are accessible** and content is still available
        4. **Check for outdated information** and flag if necessary
        5. **Identify any missing key areas** that need more resources
        6. **Flag exceptional resources** (total score above 27/30)
        
        Create quality categories:
        - **Essential** (27-30 points): Must-read resources
        - **Recommended** (24-26 points): High-quality, valuable content
        - **Good** (21-23 points): Solid resources for specific needs
        - **Archive** (below 21): Remove from final list
        
        Ensure balanced representation of:
        - Both languages (English and Spanish)
        - Different difficulty levels
        - Various content types
        """,
        expected_output="Quality-filtered list with categories and accessibility verification",
        agent=quality_controller,
        context=[task_research, task_analyze_content]
    )
    
    # Task 5: Final Content Curation and Organization
    task_curate = Task(
        description="""
        Create the final curated list with exactly 10 high-quality resources:
        
        ## Format the output as:
        
        # RECURSOS CURADOS - [TOPIC NAME]
        
        ## TOP 10 RECURSOS SELECCIONADOS
        
        ### 1. 
        **Título Original:** [Title in original language]
        **URL:** http://complete-url-here
        **Idioma:** [Inglés/Español]
        **Autor/Fuente:** [Author/Source]
        **Nivel:** [Principiante/Intermedio/Avanzado]
        **Relevancia:** [Explicación en español de por qué este recurso es valioso, qué aprenderás y por qué lo recomendamos]
        
        ### 2.
        **Título Original:** [Title in original language]
        **URL:** http://complete-url-here
        **Idioma:** [Inglés/Español]
        **Autor/Fuente:** [Author/Source]
        **Nivel:** [Principiante/Intermedio/Avanzado]
        **Relevancia:** [Explicación en español de por qué este recurso es valioso]
        
        [Continue with items 3-10 in the same format]
        
        ## RESUMEN
        - Total de recursos curados: 10
        - Recursos en inglés: [número]
        - Recursos en español: [número]
        - Distribución por nivel: Principiante ([número]), Intermedio ([número]), Avanzado ([número])
        
        Make it ready to copy-paste and use immediately.
        """,
        expected_output="Final organized list of curated resources with URLs, ready to use",
        agent=content_curator,
        context=[task_analyze, task_quality]
    )
    
    return [
        task_analyze,
        task_research,
        task_analyze_content,
        task_quality,
        task_curate
    ]