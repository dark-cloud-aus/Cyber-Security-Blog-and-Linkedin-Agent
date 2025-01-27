from crewai import Agent, Task
from langchain_openai import ChatOpenAI
import os

def create_senior_agent():
    llm = ChatOpenAI(
        model_name="gpt-4-0125-preview",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    return Agent(
        role='Senior Research Reviewer',
        goal='Review and enhance cybersecurity research findings',
        backstory="""You are a senior cybersecurity expert with 20+ years of experience.
        Your role is to verify research findings, ensure technical accuracy, and identify
        any gaps in the analysis.""",
        verbose=True,
        allow_delegation=False,
        tools=[],
        llm=llm
    )

def create_senior_review_task(agent, research_data):
    return Task(
        description=f"""
        Review and enhance the following research content. Ensure:
        1. Technical accuracy of all claims
        2. Completeness of analysis
        3. Proper technical depth
        4. Verification of sources
        5. Addition of any missing critical information

        Research content to review:
        {research_data}
        """,
        expected_output="Enhanced and verified research content with additional technical details and fact-checking",
        agent=agent,
        context=[research_data]
    )

async def review(self, content):
    review_template = """
    Review and enhance the following research content. Ensure:
    1. Technical accuracy of all claims
    2. Completeness of analysis
    3. Proper technical depth
    4. Verification of sources
    5. Addition of any missing critical information

    Content to review:
    {content}
    """
    return await self.agent.run(review_template.format(content=content)) 
