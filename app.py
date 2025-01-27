import streamlit as st
from crewai import Agent, Task, Crew, Process
from agents.research_agent import create_research_agent, create_research_task
from agents.senior_agent import create_senior_agent, create_senior_review_task
from agents.analyst_agent import create_analyst_agent, create_analysis_task
from agents.writer_agent import create_writer_agent, create_writing_task
from agents.seo_agent import create_seo_agent, create_seo_task
from agents.copy_manager_agent import create_copy_manager_agent, create_review_task
import asyncio
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Verify API key is loaded
if not os.getenv("OPENAI_API_KEY"):
    st.error("OpenAI API key not found. Please add it to your .env file.")
    st.stop()

# Add this right after load_dotenv()
print("API Key:", os.getenv("OPENAI_API_KEY")[:10] + "...")  # Only prints first 10 chars for security

# Configure Streamlit page
st.set_page_config(
    page_title="Cyber Intelligence Content Generator",
    page_icon="🛡️",
    layout="wide"
)

class ContentGenerator:
    def __init__(self):
        # Create all agents
        self.research_agent = create_research_agent()
        self.senior_agent = create_senior_agent()
        self.analyst_agent = create_analyst_agent()
        self.writer_agent = create_writer_agent()
        self.seo_agent = create_seo_agent()
        self.copy_manager = create_copy_manager_agent()

    def create_crew(self, prompt, format_type):
        """Create and configure the CrewAI instance for a specific format"""
        # Create a single task that includes all the steps
        task = Task(
            description=f"""
            Create a {format_type} about {prompt}.
            
            Follow these steps in order:
            1. Research Phase:
               - Start with these authoritative sources:
                 
                 Threat Intelligence:
                 * MITRE ATT&CK (https://attack.mitre.org/)
                 * The DFIR Report (https://thedfirreport.com/)
                 * Unit42 Research (https://unit42.paloaltonetworks.com/)
                 * Unit42 Threat Briefs (https://unit42.paloaltonetworks.com/?pg=1#threat-brief)
                 * IBM Security (https://www.ibm.com/security/data-breach/threat-intelligence)
                 * FireEye Research (https://www.fireeye.com/blog/threat-research.html)
                 * Recorded Future (https://www.recordedfuture.com/category/research/)
                 
                 News and Analysis:
                 * The Hacker News (https://thehackernews.com/)
                 * Dark Reading (https://www.darkreading.com/)
                 * Krebs on Security (https://krebsonsecurity.com/)
                 * Bleeping Computer (https://www.bleepingcomputer.com/)
                 * Threatpost (https://threatpost.com/)
                 * CyberScoop (https://www.cyberscoop.com/)
                 
                 Technical Research:
                 * Google Project Zero (https://googleprojectzero.blogspot.com/)
                 * SANS ISC (https://isc.sans.edu/)
                 * This Week in 4n6 (https://thisweekin4n6.com/)
                 * Troy Hunt's Blog (https://www.troyhunt.com/)
                 * Schneier on Security (https://www.schneier.com/)
                 
                 Industry Reports:
                 * Verizon DBIR (https://enterprise.verizon.com/resources/reports/dbir/)
                 * FireEye Intelligence (https://www.fireeye.com/current-threats/threat-intelligence-reports.html)
                 * Red Canary (https://redcanary.com/threat-detection-report/)
                 
               - Cross-reference information across multiple sources
               - Prioritize recent information and developments
               - Include citations for all sources used
            
            2. Analysis Phase:
               - Verify technical accuracy
               - Validate all claims and sources
               - Enhance technical details
            
            3. Writing Phase:
               Format specifically as a {format_type} following these guidelines:
               {self._get_format_guidelines(format_type)}
            
            4. Final Review:
               - Ensure technical accuracy
               - Verify proper formatting
               - Check completeness
            
            The final output should be a complete, polished {format_type}.
            """,
            expected_output=f"Complete {format_type} about {prompt}",
            agent=self.writer_agent
        )
        
        crew = Crew(
            agents=[
                self.research_agent,
                self.senior_agent,
                self.analyst_agent,
                self.writer_agent,
                self.seo_agent,
                self.copy_manager
            ],
            tasks=[task],
            verbose=True
        )
        
        return crew

    def _get_format_guidelines(self, format_type):
        """Return specific guidelines for each format type"""
        guidelines = {
            'blog_post': """
                Create a comprehensive technical blog post with the following structure:
                
                1. Title and Introduction (200-300 words)
                   - Create an engaging, technical title
                   - Include key technical details in the introduction
                   - State the specific threat/vulnerability being discussed
                   - Include exact CVSS scores or threat levels
                   - Provide immediate context for technical readers
                
                2. Technical Analysis (400-600 words)
                   - Provide in-depth technical breakdown
                   - Include specific vulnerability mechanics
                   - Show actual code examples or exploit methods
                   - Document exact affected versions
                   - Include specific technical diagrams or flowcharts
                   - Use actual command examples
                   - Show real configuration snippets
                
                3. Threat Intelligence (200-300 words)
                   - Document specific threat actors involved
                   - Include actual campaign timelines
                   - Show real-world exploitation examples
                   - Provide specific industry targets
                   - Include exact dates and events
                
                4. IOCs and Technical Indicators (200-300 words)
                   - List all discovered IOCs with context
                   - Include actual file hashes
                   - Show real malicious IP addresses
                   - Document exact C2 domains
                   - Include specific registry keys
                   - Show actual file paths
                   - Provide exact configuration indicators
                
                5. MITRE ATT&CK Mapping (150-200 words)
                   - Map exact techniques with IDs
                   - Provide specific examples of each TTP
                   - Show actual command examples used
                   - Include detailed sub-technique information
                
                6. Detection Methods (200-300 words)
                   - Include actual YARA rules
                   - Show specific Sigma rules
                   - Provide exact log queries
                   - Include real IDS/IPS signatures
                   - Document specific detection logic
                
                7. Mitigation Strategies (200-300 words)
                   - Provide exact patch information
                   - Show specific configuration changes
                   - Include actual command examples
                   - Document exact mitigation steps
                   - Provide timeline recommendations
                
                8. Conclusion (100-200 words)
                   - Summarize key technical points
                   - Provide specific recommendations
                   - Include next steps for readers
                
                Format Requirements:
                - Minimum Length: 1500 words
                - Target Length: 2000-2500 words
                - Use proper markdown formatting
                - Include code blocks for all technical examples
                - Use tables for organizing IOCs
                - Include proper section headers
                
                Technical Requirements:
                - Must include actual technical details, not placeholders
                - Must provide real IOCs with context
                - Must include specific commands and configurations
                - Must show exact version numbers
                - Must include proper citations
                - Must provide detailed technical examples
                
                Writing Style:
                - Technical and detailed
                - Show deep technical expertise
                - Include specific examples
                - Maintain professional tone
                - Focus on actionable information
                """,
                
            'linkedin_post': """
                Create a LinkedIn post with this structure:
                
                1. Opening (2-3 paragraphs)
                   - Start with the specific CVE ID and CVSS score if applicable
                   - Write a compelling technical introduction
                   - Explain the vulnerability/issue in clear, technical terms
                   - Make it engaging but maintain professional tone
                
                2. Technical Details (2-3 paragraphs)
                   - Explain the technical aspects in a conversational flow
                   - Include specific vulnerability type and mechanics
                   - Detail exact affected versions
                   - Describe attack vector and exploitation method
                   - Explain required privileges and conditions
                   - Discuss impact using CIA triad framework
                
                3. Real-World Context (1-2 paragraphs)
                   - Describe known exploitations in the wild
                   - Explain scope of affected systems/organizations
                   - Name specific threat actors if known
                   - Detail which industries are most at risk
                   - Provide context about why this matters
                
                4. Mitigation Discussion (1-2 paragraphs)
                   - Discuss available patches and updates
                   - Explain specific mitigation strategies
                   - Share detection methods
                   - Provide clear timeline recommendations
                   - Link to full advisories or detailed reports
                
                5. Conclusion
                   - Brief wrap-up of key points
                   - Clear next steps
                   - Professional call to engagement
                
                6. Hashtags (on final line)
                   - Include the CVE ID as a hashtag
                   - Use relevant product hashtags
                   - Include #InfoSec #CyberSecurity #ThreatIntel
                
                Format: 
                - Write in clear paragraphs, not bullet points
                - Use line breaks between sections
                - Make it read like a technical story
                - Avoid bullet points except for specific lists of IOCs or version numbers
                
                Length: 300-500 words
                
                Requirements:
                - Must flow naturally like a professional conversation
                - Must include specific technical details woven into the narrative
                - Must cite sources within the flow of the text
                - Must include actual version numbers
                - Must include real threat actor names if known
                - Must include specific mitigation steps
                
                Tone: 
                - Professional but conversational
                - Technically precise without being dry
                - Engaging but not informal
                - Write as if explaining to a fellow security professional
                """,
                
            'threat_alert': """
                Create a formal threat intelligence bulletin with:
                
                1. Alert Header
                   - Severity Level
                   - Date/Time
                   - Threat Type
                   - Affected Systems/Sectors
                
                2. Executive Summary
                   - 2-3 sentences overview
                   - Immediate actions required
                
                3. Technical Details
                   - Detailed attack analysis
                   - All observed IOCs
                   - Attack flow diagram
                
                4. Impact Assessment
                   - Potential business impact
                   - Affected systems/data
                   - Scope of compromise
                
                5. Mitigation Steps
                   - Immediate actions
                   - Long-term recommendations
                   - Required patches/updates
                
                6. Detection Methods
                   - SIEM rules
                   - IDS/IPS signatures
                   - Log queries
                
                Format: Formal report structure
                Length: As needed for complete details
                Tone: Formal and precise
                """,
                
            'confluence_page': """
                Create a Confluence page with:
                
                1. Page Header
                   - Title
                   - Table of Contents
                   - Last Updated Date
                
                2. Overview
                   - Brief description
                   - Scope
                   - Relevance to organization
                
                3. Technical Documentation
                   - Step-by-step procedures
                   - Configuration details
                   - Command references
                
                4. Related Information
                   - Links to related pages
                   - External references
                   - Tool documentation
                
                5. Attachments
                   - Relevant files
                   - Scripts
                   - Templates
                
                Format: Use Confluence markdown
                Include: {color:red}Important notes{color}
                Structure: Use proper heading hierarchy
                """
        }
        return guidelines.get(format_type, "")

    async def generate_content(self, prompt, selected_formats):
        """Generate content based on selected formats"""
        results = {}
        
        try:
            # Create status containers for each phase
            status_container = st.empty()
            progress_bar = st.progress(0)
            agent_status = st.empty()
            
            # Process each format sequentially
            for format_type in selected_formats:
                start_time = time.time()
                status_container.write(f"Starting generation of {format_type.replace('_', ' ')}...")
                
                # Show research phase
                agent_status.write("🔍 Research Agent: Gathering information from primary sources...")
                progress_bar.progress(10)
                time.sleep(2)  # Small delay for UI update
                
                agent_status.write("📊 Research Agent: Cross-referencing information...")
                progress_bar.progress(20)
                time.sleep(2)
                
                # Show analysis phase
                agent_status.write("🔎 Senior Agent: Reviewing technical accuracy...")
                progress_bar.progress(30)
                time.sleep(2)
                
                agent_status.write("🧪 Analyst Agent: Enhancing technical details...")
                progress_bar.progress(40)
                time.sleep(2)
                
                # Show writing phase
                agent_status.write("✍️ Writer Agent: Crafting content...")
                progress_bar.progress(60)
                time.sleep(2)
                
                # Create and execute crew for this format
                crew = self.create_crew(prompt, format_type)
                
                # Show SEO phase
                agent_status.write("🎯 SEO Agent: Optimizing content...")
                progress_bar.progress(80)
                
                result = crew.kickoff()
                
                # Show final review phase
                agent_status.write("📝 Copy Manager: Performing final review...")
                progress_bar.progress(90)
                
                # Ensure minimum processing time (30 seconds)
                elapsed_time = time.time() - start_time
                if elapsed_time < 30:
                    agent_status.write("⚡ All Agents: Gathering additional technical details...")
                    time.sleep(30 - elapsed_time)
                
                # Store the result
                if isinstance(result, str):
                    results[format_type] = result
                else:
                    results[format_type] = str(result)
                
                # Show completion
                progress_bar.progress(100)
                agent_status.write("✅ Generation complete!")
                status_container.write(f"Completed {format_type.replace('_', ' ')}!")
                
                # Reset progress for next format
                if format_type != selected_formats[-1]:
                    time.sleep(2)
                    progress_bar.progress(0)
                
        except Exception as e:
            st.error(f"Error during content generation: {str(e)}")
            for format_type in selected_formats:
                results[format_type] = f"Error generating content: {str(e)}"
        
        return results

async def main():
    st.title("🛡️ Cyber Intelligence Content Generator")
    st.write("Generate professional cybersecurity content using AI agents")

    # User input section
    prompt = st.text_area(
        "Enter your research topic (e.g., ransomware group, vulnerability):",
        height=100,
        placeholder="Example: Research the Conti ransomware group's tactics and recent activities"
    )

    # Output format selection
    st.subheader("Select Output Formats:")
    col1, col2 = st.columns(2)
    
    with col1:
        blog_post = st.checkbox("Technical Blog Post", help="Detailed technical analysis with IoCs")
        linkedin_post = st.checkbox("LinkedIn Article", help="Social media optimized content")
    
    with col2:
        threat_alert = st.checkbox("Threat Alert Bulletin", help="Formal threat intelligence bulletin")
        confluence_page = st.checkbox("Confluence Page", help="Internal documentation format")

    # Collect selected formats
    selected_formats = []
    if blog_post: selected_formats.append("blog_post")
    if linkedin_post: selected_formats.append("linkedin_post")
    if threat_alert: selected_formats.append("threat_alert")
    if confluence_page: selected_formats.append("confluence_page")

    if st.button("Generate Content", type="primary"):
        if not prompt:
            st.error("Please enter a research topic")
            return
        
        if not selected_formats:
            st.error("Please select at least one output format")
            return

        with st.spinner("AI agents are analyzing and generating content..."):
            try:
                generator = ContentGenerator()
                results = await generator.generate_content(prompt, selected_formats)

                # Display results in tabs
                st.success("Content generation complete!")
                tabs = st.tabs([format_type.replace('_', ' ').title() for format_type in selected_formats])
                
                for tab, format_type in zip(tabs, selected_formats):
                    with tab:
                        st.markdown(results[format_type])
                        st.download_button(
                            f"Download {format_type.replace('_', ' ').title()}",
                            results[format_type],
                            file_name=f"{format_type}.txt",
                            mime="text/plain"
                        )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
