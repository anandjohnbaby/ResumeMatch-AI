class PDFExtractionError(Exception):
    """Raised when PDF text extraction fails."""
    pass

class SkillExtractionError(Exception):
    """Raised when LLM skill extraction fails."""
    pass