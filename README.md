# Cyber-Security-Blog-and-Linkedin-Agent (plus much more)
An Ai agent that takes a simple prompt, then uses a series of agents to conduct research and then, depending on the users selection, output:

1. A technical blog post of at least 1000 words
2. A linkedIn post
3. A confluence page
4. Threat Alert bulletin

All based on the initial research!


This Ai agent uses CrewAI framework to create a team of agents to conduct cyber security resarch on a specific subject (a ransmware gang or specific CVE).  Once
prompted the research agent uses GPT4o to conduct a deep level research in to the subject. Once the initial research has been conducted the agent passes the information to a cyber security analyst agent who adds more technical detail. Then this is passed to the the Senior research agent who checks what has been written, makes ammendments and then passes this to the writer agent who writes the blog post, confluence page, linked post etc and the passes that content to the SEO agent who corrects the content to make sure its good for SEO and then finally the copy manager who checks over everything and published in to the UI for the user to simply copy and paste 


<img width="1420" alt="Screen Shot 2025-01-27 at 13 10 53" src="https://github.com/user-attachments/assets/784ceb20-a17b-44b9-a113-60a780293511" />
