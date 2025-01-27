from crewai import Agent, Task
from langchain_openai import ChatOpenAI
import os

def create_seo_agent():
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.4,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    return Agent(
        role='SEO Specialist',
        goal='Optimize cybersecurity content for search engines while maintaining technical accuracy',
        backstory="""You are an SEO expert specializing in technical and cybersecurity content. 
        You know how to optimize content for search engines while preserving technical accuracy 
        and professional tone.""",
        verbose=True,
        allow_delegation=False,
        tools=[],
        llm=llm
    )

def create_seo_task(agent, content, format_type):
    templates = {
        'blog_post': _blog_seo_template(content),
        'linkedin_post': _social_seo_template(content),
        'threat_alert': _threat_alert_seo_template(content),
        'confluence_page': _confluence_seo_template(content)
    }
    
    return Task(
        description=templates[format_type],
        expected_output=f"SEO-optimized {format_type} content",
        agent=agent,
        context=[content]
    )

def _blog_seo_template(content):
    return f"""
    Optimize this blog post for search engines:
    1. Create an SEO-optimized title
    2. Add meta description
    3. Optimize headings (H1, H2, H3)
    4. Include relevant keywords naturally
    5. Optimize image alt texts if any
    6. Add internal/external linking suggestions
    
    Original content:
    {content}
    """

def _social_seo_template(content):
    return f"""
    Optimize this LinkedIn post for maximum visibility:
    1. Use trending hashtags relevant to cybersecurity
    2. Optimize post structure for LinkedIn algorithm
    3. Include relevant keywords
    4. Suggest optimal posting time
    
    Original content:
    {content}
    """

def _threat_alert_seo_template(content):
    return f"""
    Optimize this threat alert for searchability:
    1. Create clear, searchable title
    2. Add relevant tags and categories
    3. Include standardized threat identifiers
    4. Optimize technical term usage
    
    Original content:
    {content}
    """

def _confluence_seo_template(content):
    return f"""
    Optimize this Confluence page for internal searchability:
    1. Add appropriate labels
    2. Optimize page title
    3. Include relevant internal links
    4. Add table of contents
    
    Original content:
    {content}
    """ 
