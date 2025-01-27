from crewai import Agent, Task
from langchain_openai import ChatOpenAI
import os

def create_research_agent():
    """Create and return a research agent"""
    llm = ChatOpenAI(
        model_name="gpt-4-0125-preview",
        temperature=0.5,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    return Agent(
        role='Senior Cybersecurity Researcher',
        goal='Conduct comprehensive research on cybersecurity topics and gather detailed technical information',
        backstory="""You are an experienced cybersecurity researcher with over 15 years 
        of experience in threat intelligence, malware analysis, computer vulnerability research and ransomware gangs. You specialize in 
        tracking threat actors, analyzing malware, and understanding attack patterns.""",
        verbose=True,
        allow_delegation=False,
        tools=[],  # Add empty tools list
        llm=llm
    )

def create_research_task(agent, topic):
    """Create a research task for the agent"""
    return Task(
        description=f"""
        Conduct exhaustive research on {topic}. Your goal is to gather comprehensive technical details 
        that will support a detailed technical blog post of at least 1000 words.

        If researching a CVE:
        - Find and document the exact vulnerability details from NVD
        - Locate and analyze any available exploit code or POCs
        - Document all known affected versions with exact version numbers
        - Find specific examples of real-world exploitation
        - Gather actual IOCs including:
          * Specific malicious IP addresses
          * Actual file hashes
          * Real command and control domains
          * Exact registry keys and values
          * Specific file paths
        - Document exact CVSS scores and vectors
        - Find and document specific patch information
        
        If researching a threat actor or malware:
        - Document specific campaigns with dates and targets
        - Gather actual IOCs from real attacks
        - Find specific malware samples and their hashes
        - Document exact C2 infrastructure details
        - Gather specific TTPs with examples
        - Find actual code snippets or configuration files
        
        Required Research Depth:
        1. Technical Details
           - Find and document exact technical specifications
           - Gather detailed vulnerability mechanics
           - Document specific exploit methods
           - Find actual code examples where available
        
        2. Impact Analysis
           - Find specific organizations affected
           - Document actual financial impacts
           - Gather specific incident timelines
           - Find real victim statements or reports
        
        3. Detection & Mitigation
           - Find exact YARA rules
           - Gather specific Sigma rules
           - Document actual Snort/Suricata signatures
           - Find specific log queries for detection
           - Gather exact configuration changes needed
        
        4. Threat Intelligence
           - Document specific threat actor attributions
           - Find exact campaign timelines
           - Gather specific tool and infrastructure details
           - Document actual malware variants
        
        Primary Sources to Check:
        - MITRE ATT&CK Database: https://attack.mitre.org/
        - US-CERT Advisories: https://www.cisa.gov/news-events/cybersecurity-advisories
        - The DFIR Report: https://thedfirreport.com/
        - Unit42 Threat Research: https://unit42.paloaltonetworks.com/
        - Unit42 Threat Assessments: https://unit42.paloaltonetworks.com/tag/threat-assessment/
        - Unit42 Reports: https://unit42.paloaltonetworks.com/?pg=1#reports
        - Unit42 Threat Briefs: https://unit42.paloaltonetworks.com/?pg=1#threat-brief
        - IBM Security Intelligence: https://www.ibm.com/security/data-breach/threat-intelligence
        - Red Canary Threat Reports: https://redcanary.com/threat-detection-report/
        - Recorded Future Research: https://www.recordedfuture.com/category/research/
        - Recorded Future Blog: https://www.recordedfuture.com/blog/
        - FireEye Threat Research: https://www.fireeye.com/blog/threat-research.html
        - FireEye APT Groups: https://www.fireeye.com/current-threats/apt-groups.html
        - FireEye Intelligence Reports: https://www.fireeye.com/current-threats/threat-intelligence-reports.html
        
        Security News and Analysis:
        - The Hacker News: https://thehackernews.com/
        - Bleeping Computer: https://www.bleepingcomputer.com/
        - Dark Reading: https://www.darkreading.com/
        - Dark Reading Attacks & Breaches: https://www.darkreading.com/attacks-breaches.asp
        - Dark Reading Threat Intelligence: https://www.darkreading.com/threat-intelligence.asp
        - Dark Reading Vulnerabilities & Threats: https://www.darkreading.com/vulnerabilities-threats.asp
        - Dark Reading Security Analytics: https://www.darkreading.com/security-analytics.asp
        - Krebs on Security: https://krebsonsecurity.com/
        - The Record: https://therecord.media/
        - Security Week: https://www.securityweek.com/
        - Portswigger Daily Swig: https://portswigger.net/daily-swig
        - Threatpost: https://threatpost.com/
        - CyberScoop: https://www.cyberscoop.com/
        
        Technical Research and Analysis:
        - Google Project Zero: https://googleprojectzero.blogspot.com/
        - Schneier on Security: https://www.schneier.com/
        - SANS ISC: https://isc.sans.edu/
        - SANS Reading Room: https://www.sans.org/reading-room/popular/week
        - This Week in 4n6: https://thisweekin4n6.com/
        - Troy Hunt's Blog: https://www.troyhunt.com/
        - Didier Stevens's Blog: https://blog.didierstevens.com/
        
        Industry Reports and Resources:
        - Verizon DBIR: https://enterprise.verizon.com/resources/reports/dbir/
        - The DFIR Report: https://thedfirreport.com/
        - ISC SANS: https://isc.sans.edu/
        
        Additional CVE-specific Sources:
        - National Vulnerability Database: https://nvd.nist.gov/vuln
        - Rapid7 Database: https://www.rapid7.com/db/
        - Exploit Database: https://www.exploit-db.com/
        - VulnDB: https://vuldb.com/
        - Red Hat Security Database: https://access.redhat.com/security/security-updates/
        - GitHub Security Lab: https://securitylab.github.com/
        
        Research Requirements:
        - Must find and document actual technical details, not generalizations
        - Must gather real IOCs, not placeholder examples
        - Must find specific examples and instances
        - Must document exact commands, configurations, and code where available
        - Must gather enough detail to support a 1000+ word technical blog post
        - Must include proper citations for all information
        
        Final Output:
        Provide a comprehensive research document with all findings organized by category,
        including all specific technical details, IOCs, and examples found. Include proper
        citations for each piece of information.
        """,
        expected_output="Detailed technical analysis with specific vulnerability details, affected versions, exploitation status, and mitigation steps.",
        agent=agent
    )

async def research(agent, topic):
    """Conduct initial research on the given topic"""
    research_template = """
    Conduct thorough research on {topic}. Include:
    
    1. Historical Background
    - Origin and evolution
    - Key events and timeline
    
    2. Technical Analysis
    - Infrastructure details
    - Malware analysis (if applicable)
    - Technical specifications
    
    3. TTPs (Tactics, Techniques, and Procedures)
    - MITRE ATT&CK mapping
    - Common attack patterns
    - Delivery methods
    
    4. Indicators of Compromise (IoCs)
    - File hashes
    - C2 domains
    - Network indicators
    
    5. Notable Campaigns
    - Major attacks
    - Target sectors
    - Impact analysis
    
    6. Current Threat Landscape
    - Recent activities
    - Threat level assessment
    - Potential future developments
    
    Ensure all information is technically accurate and properly sourced.
    """
    
    return await agent.run(research_template.format(topic=topic)) 
