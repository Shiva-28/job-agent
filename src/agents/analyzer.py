import json
import yaml
import logging
from pathlib import Path
from src.core.config import Config
from src.core.llm import llm_client

logger = logging.getLogger(__name__)

class Analyzer:
    """
    Agent responsible for analyzing text using LLM and returning structured JSON.
    """
    
    def __init__(self):
        self.prompts = self._load_prompts()

    def _load_prompts(self):
        """Loads the YAML prompts file."""
        prompt_path = Config.TEMPLATES_DIR / "system_prompts.yaml"
        if not prompt_path.exists():
            raise FileNotFoundError(f"❌ Prompts file missing at {prompt_path}")
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def analyze_jd(self, jd_text: str) -> dict:
        """
        Extracts structured data from a Job Description.
        """
        logger.info("🔍 Analyzing Job Description...")
        
        system_instruction = self.prompts['job_analyzer']['instruction']
        prompt = f"{system_instruction}\n\nJOB DESCRIPTION:\n{jd_text}"
        
        response_text = llm_client.generate(prompt)
        return self._clean_and_parse_json(response_text)

    def analyze_resume(self, resume_text: str) -> dict:
        """
        Extracts structured data from a Resume.
        """
        logger.info("🔍 Analyzing Resume...")
        
        system_instruction = self.prompts['resume_analyzer']['instruction']
        prompt = f"{system_instruction}\n\nRESUME CONTENT:\n{resume_text}"
        
        response_text = llm_client.generate(prompt)
        return self._clean_and_parse_json(response_text)

    def _clean_and_parse_json(self, text: str) -> dict:
        """
        Helper to robustly parse JSON from LLM output.
        Removes markdown code blocks if Gemini adds them.
        """
        try:
            # Remove ```json and ``` if present
            cleaned = text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            return json.loads(cleaned)
        except json.JSONDecodeError:
            logger.error(f"❌ Failed to parse JSON. Raw Output: {text}")
            return {"error": "Failed to parse API response", "raw": text}

# Singleton Instance
analyzer_agent = Analyzer()