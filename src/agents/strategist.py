import json
import logging
from src.core.llm import llm_client
from src.core.utils import cosine_similarity
from src.agents.analyzer import analyzer_agent

logger = logging.getLogger(__name__)

class Strategist:
    """
    Agent responsible for strategy, fitment analysis, and scoring.
    """

    def calculate_fitment(self, resume_text: str, jd_text: str) -> dict:
        """
        Performs a dual-layer analysis:
        1. Semantic Score (Embeddings)
        2. Strategic Analysis (LLM)
        """
        logger.info("🧠 Strategist is calculating fitment...")

        # 1. The Science: Calculate Vector Score
        resume_vec = llm_client.get_embedding(resume_text)
        jd_vec = llm_client.get_embedding(jd_text)
        
        # Convert 0-1 score to 0-100%
        raw_score = cosine_similarity(resume_vec, jd_vec)
        match_percentage = round(raw_score * 100, 2)

        # 2. The Art: Get Qualitative Analysis
        qualitative_analysis = self._get_qualitative_analysis(resume_text, jd_text)

        return {
            "match_percentage": match_percentage,
            "analysis": qualitative_analysis
        }

    def _get_qualitative_analysis(self, resume_text: str, jd_text: str) -> dict:
        """Uses Gemini to explain the fitment."""
        prompts = analyzer_agent._load_prompts() # Reuse the loader
        base_instruction = prompts['fitment_analyzer']['instruction']
        
        # Inject the actual text into the prompt
        formatted_prompt = base_instruction.replace("{jd_text}", jd_text).replace("{resume_text}", resume_text)
        
        response = llm_client.generate(formatted_prompt)
        return analyzer_agent._clean_and_parse_json(response)

# Singleton Instance
strategist_agent = Strategist()