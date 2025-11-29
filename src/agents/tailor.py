import logging
from src.core.llm import llm_client
from src.agents.analyzer import analyzer_agent

logger = logging.getLogger(__name__)

class Tailor:
    """
    Agent responsible for tailoring resume content to specific JDs.
    """

    def tailor_resume(self, resume_text: str, jd_text: str) -> dict:
        """
        Rewrites summary and bullets to match JD keywords.
        Returns a dictionary with the optimized text.
        """
        logger.info("✂️ Tailoring Resume content...")
        
        prompts = analyzer_agent._load_prompts()
        base_instruction = prompts['resume_tailor']['instruction']
        
        prompt = base_instruction.replace("{jd_text}", jd_text)\
                                 .replace("{resume_text}", resume_text)
        
        response = llm_client.generate(prompt)
        
        # Reuse the robust JSON parser from the analyzer
        return analyzer_agent._clean_and_parse_json(response)

# Singleton Instance
tailor_agent = Tailor()