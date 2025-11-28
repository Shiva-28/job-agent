import google.generativeai as genai
from src.core.config import Config
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    """
    Wrapper for Google Gemini API to handle text generation and embeddings.
    Updated for Gemini 2.5 Flash.
    """

    def __init__(self):
        # Initialize the API using the key from Config
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        # Models Configuration
        # using gemini-2.5-flash as requested
        self.generation_model_name = 'gemini-2.5-flash' 
        self.embedding_model_name = 'models/text-embedding-004'

        self.generation_model = genai.GenerativeModel(self.generation_model_name)

    def generate(self, prompt: str) -> str:
        """
        Sends a prompt to Gemini and returns the text response.
        """
        try:
            logger.info(f"🤖 Sending request to {self.generation_model_name}...")
            response = self.generation_model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"❌ Gemini Generation Error: {e}")
            return f"Error: Could not generate content. Details: {e}"

    def get_embedding(self, text: str) -> list[float]:
        """
        Converts text into a vector embedding for comparison/matching.
        """
        try:
            # Clean text for better embedding results
            clean_text = text.replace("\n", " ")
            result = genai.embed_content(
                model=self.embedding_model_name,
                content=clean_text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"❌ Embedding Error: {e}")
            return []

# Singleton instance
llm_client = LLMClient()