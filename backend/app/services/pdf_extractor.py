import fitz
from app.utils.exceptions import PDFExtractionError

# Takes PDF file bytes, reads using PyMuPDF(fitz), and returns cleaned raw text
def extract_text_from_pdf(file_bytes: bytes) -> str:
    if not file_bytes:
        raise PDFExtractionError("Empty file received.")    
    
    text = ""
    
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()

        clean_text = " ".join(text.split())
        print("----------------------------------------------------------------------------")
        print(clean_text)

        if not clean_text.strip():
            raise PDFExtractionError("PDF appears to be empty or image-only (no extractable text).")

        return clean_text
    except PDFExtractionError:
        raise
    except Exception as e:
        raise PDFExtractionError(f"Failed to process PDF: {str(e)}")