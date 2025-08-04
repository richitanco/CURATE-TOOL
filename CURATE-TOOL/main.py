#!/usr/bin/env python3
"""
CrewAI Content Curator - Main entry point
"""
import click
from datetime import datetime
from typing import Optional

from config.settings import validate_config
from src.crew import ContentCurationCrew
from src.utils import save_content, create_project_structure, test_apis, generate_run_id


@click.command()
@click.argument('topic', required=False)
@click.option('--output-format', '-f', default='markdown', help='Output format (markdown/html)')
@click.option('--create-structure', '-s', is_flag=True, help='Create folder structure')
@click.option('--test', '-t', is_flag=True, help='Test API connections')
def main(topic: str, output_format: str, create_structure: bool, test: bool):
    """
    CrewAI Content Curator - Create educational content using AI
    
    TOPIC: The educational topic to create content for
    """
    print(f"\n🎓 CrewAI Content Curator")
    print("=" * 50)
    
    # Test mode
    if test:
        print("\n🔍 Testing API connections...")
        results = test_apis()
        for api, status in results.items():
            emoji = "✅" if status else "❌"
            print(f"{emoji} {api.upper()}: {'Connected' if status else 'Failed'}")
        return
    
    # Check if topic is provided when not in test mode
    if not topic:
        print("\n❌ Error: Please provide a topic")
        print("Usage: python main.py 'Your Topic Here'")
        print("   or: python main.py --test")
        return
    
    # Validate configuration
    try:
        validate_config()
    except ValueError as e:
        print(f"\n❌ Configuration error: {e}")
        print("Please check your .env file")
        return
    
    # Generate run ID for this execution
    run_id = generate_run_id(topic)
    
    # Start content curation
    print(f"\n📚 Topic: {topic}")
    print(f"🔖 Run ID: {run_id}")
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🚀 Starting content curation...\n")
    
    # Create and run crew
    crew = ContentCurationCrew()
    result = crew.run(topic)
    
    if result['success']:
        # Create folder structure if requested
        base_dir = None
        if create_structure:
            base_dir = create_project_structure(topic, run_id)
            print(f"\n📁 Project structure created at: {base_dir}")
        
        # Save content
        filepath = save_content(
            content=result['content'], 
            topic=topic, 
            run_id=run_id,
            output_format=output_format,
            base_dir=base_dir
        )
        print(f"\n✅ Content saved to: {filepath}")
        
        print(f"\n🎉 Content curation completed successfully!")
        
    else:
        print(f"\n❌ Error: {result['error']}")
        print("Please check the logs for more details")
    
    print(f"\n⏰ Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    main()