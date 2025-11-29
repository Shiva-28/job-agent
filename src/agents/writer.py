import logging
from src.core.llm import llm_client
from src.agents.analyzer import analyzer_agent

logger = logging.getLogger(__name__)

class Writer:
    """
    Agent responsible for drafting text content (Cover Letters, Emails).
    """

    def write_cover_letter(self, resume_text: str, jd_text: str, format_type: str = "standard") -> str:
        """
        Generates a personalized cover letter.
        """
        logger.info(f"✍️ Writing Cover Letter ({format_type})...")
        
        prompts = analyzer_agent._load_prompts()
        base_instruction = prompts['cover_letter_writer']['instruction']
        
        prompt = base_instruction.replace("{jd_text}", jd_text)\
                                 .replace("{resume_text}", resume_text)\
                                 .replace("{format_type}", format_type)
        
        return llm_client.generate(prompt)

    def write_email(self, email_type: str, job_details: dict) -> str:
        """
        Generates a networking or application email.
        """
        logger.info(f"📧 Writing Email ({email_type})...")
        
        prompts = analyzer_agent._load_prompts()
        base_instruction = prompts['email_generator']['instruction']
        
        # Safe extraction of details with defaults
        role = job_details.get('role_title', 'the open role')
        company = job_details.get('company_name', 'your company')
        
        # Handle skills: take top 3 or default
        skills_list = job_details.get('technical_skills', [])
        skills = ", ".join(skills_list[:3]) if skills_list else "relevant technical skills"
        
        prompt = base_instruction.replace("{email_type}", email_type)\
                                 .replace("{role_name}", role)\
                                 .replace("{company_name}", company)\
                                 .replace("{key_skills}", skills)
        
        return llm_client.generate(prompt)

# Singleton Instance
writer_agent = Writer()