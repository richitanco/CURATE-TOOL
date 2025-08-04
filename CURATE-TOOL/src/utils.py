"""
Utility functions for the project
"""
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from config.settings import OUTPUT_DIR, OUTPUT_FORMAT, GEMINI_MODEL


def generate_run_id(topic: str) -> str:
    """
    Generate a unique run ID for the content curation
    
    Args:
        topic: Topic name
        
    Returns:
        Unique run ID
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = topic.replace(" ", "_").replace("/", "_")[:30]  # Limit length
    return f"course_{safe_topic}_{timestamp}"


def save_content(content: str, topic: str, run_id: str = None, 
                output_format: str = None, base_dir: Optional[Path] = None) -> str:
    """
    Save curated content to file
    
    Args:
        content: Content to save
        topic: Topic name
        run_id: Unique identifier for the run (generated if not provided)
        output_format: Output format (default from settings)
        base_dir: Optional base directory to save into
        
    Returns:
        Path to saved file
    """
    output_format = output_format or OUTPUT_FORMAT
    run_id = run_id or generate_run_id(topic)
    
    if base_dir:
        # Save inside the provided project structure
        filename = f"full_content.{output_format}"
        filepath = base_dir / filename
    else:
        # Save as a standalone file in the main output directory
        filename = f"{run_id}.{output_format}"
        filepath = OUTPUT_DIR / filename
    
    # Ensure output directory exists
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        if output_format == 'markdown':
            f.write(f"# Recursos Curados: {topic}\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
        
        f.write(str(content))
    
    return str(filepath)


def create_project_structure(topic: str, run_id: str = None) -> Path:
    """
    Create organized folder structure for a course
    
    Args:
        topic: Topic name
        run_id: Unique identifier for the run (generated if not provided)
        
    Returns:
        Base directory path
    """
    run_id = run_id or generate_run_id(topic)
    base_dir = OUTPUT_DIR / run_id
    
    # Create subdirectories
    subdirs = [
        "01_modules",
        "02_presentations",
        "03_exercises",
        "04_assessments",
        "05_resources",
        "06_guides"
    ]
    
    for subdir in subdirs:
        (base_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    # Create README
    readme_content = f"""# {topic}

## Course Structure

- **01_modules/**: Course modules and lessons
- **02_presentations/**: Slide presentations
- **03_exercises/**: Practical exercises
- **04_assessments/**: Tests and evaluations
- **05_resources/**: Additional resources
- **06_guides/**: Instructor and student guides

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open(base_dir / "README.md", 'w') as f:
        f.write(readme_content)
    
    return base_dir


def test_apis() -> Dict[str, bool]:
    """
    Test all API connections
    
    Returns:
        Dictionary with API status
    """
    results = {}
    
    # Test OpenAI
    try:
        from openai import OpenAI
        from config.settings import OPENAI_API_KEY
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        results['openai'] = True
    except Exception as e:
        results['openai'] = False
        print(f"OpenAI error: {str(e)[:50]}")
    
    # Test Serper
    try:
        import requests
        from config.settings import SERPER_API_KEY
        
        response = requests.post(
            "https://google.serper.dev/search",
            headers={'X-API-KEY': SERPER_API_KEY},
            json={"q": "test"},
            timeout=5
        )
        results['serper'] = response.status_code == 200
    except Exception as e:
        results['serper'] = False
        print(f"Serper error: {str(e)[:50]}")
    
    # Test Gemini
    try:
        import google.generativeai as genai
        from config.settings import GOOGLE_API_KEY
        
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content("test")
        results['gemini'] = True
    except Exception as e:
        results['gemini'] = False
        print(f"Gemini error: {str(e)[:50]}")
    
    return results