import logging
from src.core.llm import llm_client
from src.agents.analyzer import analyzer_agent

logger = logging.getLogger(__name__)

class Coach:
    """
    Agent responsible for Interview Preparation and Question Prediction.
    """

    def generate_interview_prep(self, resume_text: str, jd_text: str) -> dict:
        """
        Predicts questions and suggests answers based on the resume.
        """
        logger.info("🎤 Coach is preparing interview questions...")
        
        prompts = analyzer_agent._load_prompts()
        base_instruction = prompts['interview_coach']['instruction']
        
        prompt = base_instruction.replace("{jd_text}", jd_text)\
                                 .replace("{resume_text}", resume_text)
        
        response = llm_client.generate(prompt)
        
        return analyzer_agent._clean_and_parse_json(response)

# Singleton Instance
coach_agent = Coach()