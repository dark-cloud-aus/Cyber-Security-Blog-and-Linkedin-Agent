# Ai agent for cyber sec technical blog posts and linkedin posts using CrewAI and Streamlit for web UI

from crewai import Agent, Task
from langchain_openai import ChatOpenAI
import os

def create_analyst_agent():
    llm = ChatOpenAI(
        model_name="gpt-4-0125-preview",
        temperature=0.4,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    return Agent(
        role='Technical Security Analyst',
        goal='Verify and enhance technical details in cybersecurity content',
        backstory="""You are a technical security analyst specializing in malware 
        analysis, threat hunting, and technical threat intelligence. Your role is to 
        ensure all technical details are accurate and comprehensive.""",
        verbose=True,
        allow_delegation=False,
        tools=[],
        llm=llm
    )

def create_analysis_task(agent, content):
    return Task(
        description=f"""
        Analyze and enhance the technical aspects of this content:
        1. Verify all technical claims
        2. Add missing technical details
        3. Validate IOCs
        4. Enhance MITRE ATT&CK mappings
        5. Add relevant technical context

        Content to analyze:
        {content}
        """,
        expected_output="Technically enhanced content with verified claims and additional technical details",
        agent=agent,
        context=[content]
    )

async def analyze(self, content):
    analysis_template = """
    Analyze and enhance the technical aspects of this content:
    1. Verify all technical claims
    2. Add missing technical details
    3. Validate IOCs
    4. Enhance MITRE ATT&CK mappings
    5. Add relevant technical context

    Content to analyze:
    {content}
    """
    return await self.agent.run(analysis_template.format(content=content)) 
