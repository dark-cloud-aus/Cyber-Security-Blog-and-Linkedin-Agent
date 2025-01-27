from crewai import Agent, Task
from langchain_openai import ChatOpenAI
import os

def create_writer_agent():
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    return Agent(
        role='Professional Content Writer',
        goal='Create engaging, format-specific cybersecurity content',
        backstory="""You are an experienced technical writer specializing in 
        cybersecurity content. You excel at adapting complex technical information 
        for different formats and audiences while maintaining accuracy.""",
        verbose=True,
        allow_delegation=False,
        tools=[],
        llm=llm
    )

def create_writing_task(agent, content, format_type):
    templates = {
        'blog_post': _blog_template(content),
        'linkedin_post': _linkedin_template(content),
        'threat_alert': _threat_alert_template(content),
        'confluence_page': _confluence_template(content)
    }
    
    return Task(
        description=templates[format_type],
        expected_output=f"Professionally written {format_type} with appropriate formatting and style",
        agent=agent,
        context=[content]
    )

def _blog_template(content):
    return f"""
    Create a technical blog post that includes:
    - Engaging title
    - Technical background
    - Detailed analysis
    - IOCs
    - MITRE ATT&CK details
    - References

    Content to format:
    {content}
    """

def _linkedin_template(content):
    return f"""
    Create a LinkedIn post that:
    - Has an attention-grabbing title
    - Uses appropriate emojis
    - Maintains technical accuracy
    - Includes a call to action
    - Is optimized for social media

    Content to format:
    {content}
    """

def _threat_alert_template(content):
    return f"""
    Create a formal threat alert bulletin that includes:
    - Alert Level and Summary
    - Technical Details
    - Threat Actor Profile
    - IOCs
    - MITRE ATT&CK Framework mapping
    - Recommended Actions
    - Timeline of Events
    - References

    Content to format:
    {content}
    """

def _confluence_template(content):
    return f"""
    Create a Confluence page that includes:
    - Brief Overview
    - Ransomware/Threat Actor History
    - Technical Details
    - TTPs (Tactics, Techniques, and Procedures)
    - List of IOCs
    - References
    
    Format with appropriate Confluence markdown.
    
    Content to format:
    {content}
    """

    # Add other template methods as needed 
