"""
Crew configuration and execution
"""
from typing import Dict
from crewai import Crew, Process

from .agents import (
    topic_analyzer,
    web_researcher,
    content_analyst,
    quality_controller,
    content_curator
)
from .tasks import create_tasks_for_topic


class ContentCurationCrew:
    """Main crew for content curation"""
    
    def __init__(self):
        """Initialize the crew with agents"""
        self.agents = [
            topic_analyzer,
            web_researcher,
            content_analyst,
            quality_controller,
            content_curator
        ]
    
    def create_crew(self, topic: str) -> Crew:
        """
        Create a crew for the given topic
        
        Args:
            topic: Educational topic to curate
            
        Returns:
            Configured Crew instance
        """
        tasks = create_tasks_for_topic(topic)
        
        return Crew(
            agents=self.agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
    
    def run(self, topic: str) -> Dict:
        """
        Execute the content curation process
        
        Args:
            topic: Educational topic to curate
            
        Returns:
            Dictionary with results
        """
        try:
            crew = self.create_crew(topic)
            result = crew.kickoff()
            
            return {
                'success': True,
                'topic': topic,
                'content': result,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'topic': topic,
                'content': None,
                'error': str(e)
            }