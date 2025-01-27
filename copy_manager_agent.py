from crewai import Agent, Task
from langchain_openai import ChatOpenAI
import os

def create_copy_manager_agent():
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    return Agent(
        role='Copy Manager',
        goal='Ensure content quality, accuracy, and professional standards',
        backstory="""You are a senior copy manager with expertise in cybersecurity 
        content. You ensure all content meets the highest standards of technical 
        accuracy, professionalism, and readability.""",
        verbose=True,
        allow_delegation=False,
        tools=[],
        llm=llm
    )

def create_review_task(agent, content, format_type):
    return Task(
        description=f"""
        Perform final review of this {format_type} content. Ensure:
        1. Technical accuracy and completeness
        2. Professional tone and language
        3. Format-specific requirements are met
        4. All technical terms are used correctly
        5. Citations and references are properly formatted
        6. Content flow and readability
        7. No sensitive/confidential information disclosure
        8. Compliance with cybersecurity best practices

        Content to review:
        {content}
        """,
        expected_output=f"Final reviewed and polished {format_type} content",
        agent=agent,
        context=[content]
    ) 
