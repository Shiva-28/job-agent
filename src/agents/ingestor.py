import logging
from pathlib import Path
from pypdf import PdfReader

logger = logging.getLogger(__name__)

class Ingestor:
    """
    Agent responsible for reading files (PDF, TXT, MD) and extracting raw text.
    """

    def file_to_text(self, file_path: Path) -> str:
        """
        Determines file type and extracts text accordingly.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"❌ File not found: {file_path}")

        suffix = file_path.suffix.lower()

        try:
            if suffix == ".pdf":
                return self._read_pdf(file_path)
            elif suffix in [".txt", ".md"]:
                return self._read_text(file_path)
            else:
                raise ValueError(f"❌ Unsupported file format: {suffix}")
        except Exception as e:
            logger.error(f"Failed to ingest {file_path}: {e}")
            return ""

    def _read_pdf(self, path: Path) -> str:
        """Extracts text from a PDF file."""
        logger.info(f"📄 Reading PDF: {path.name}")
        reader = PdfReader(path)
        text = []
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text.append(content)
        return "\n".join(text)

    def _read_text(self, path: Path) -> str:
        """Reads simple text or markdown files."""
        logger.info(f"📄 Reading Text File: {path.name}")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

# Singleton instance
ingestor_agent = Ingestor()