import fitz  # PyMuPDF
from docx import Document
import os

class DocumentService:
    @staticmethod
    def extract_text(file):
        """
        Extracts text from uploaded file based on extension.
        'file' is a Streamlit UploadedFile object or a file path.
        """
        # Handle Streamlit UploadedFile (which has a .name attribute)
        file_name = getattr(file, 'name', os.path.basename(str(file)))
        extension = os.path.splitext(file_name)[1].lower()

        if extension == '.pdf':
            return DocumentService._extract_pdf(file)
        elif extension == '.docx':
            return DocumentService._extract_docx(file)
        elif extension == '.txt':
            return DocumentService._extract_txt(file)
        else:
            raise ValueError(f"Unsupported file extension: {extension}")

    @staticmethod
    def _extract_pdf(file):
        text = ""
        # PyMuPDF can take a stream or a file path
        # For Streamlit files, we can read bytes
        try:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            raise RuntimeError(f"Error reading PDF: {e}")
        return text

    @staticmethod
    def _extract_docx(file):
        text = ""
        try:
            # python-docx needs a file-like object
            doc = Document(file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            raise RuntimeError(f"Error reading DOCX: {e}")
        return text

    @staticmethod
    def _extract_txt(file):
        text = ""
        try:
            # Read bytes and decode
            bytes_content = file.read()
            text = bytes_content.decode("utf-8")
        except UnicodeDecodeError:
            # Try other common encodings if utf-8 fails
            try:
                text = bytes_content.decode("latin-1")
            except Exception as e:
                raise RuntimeError(f"Error reading TXT: {e}")
        except Exception as e:
            raise RuntimeError(f"Error reading TXT: {e}")
        return text

    @staticmethod
    def clean_text(text):
        """Basic text cleaning to remove excessive whitespace."""
        if not text:
            return ""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    @staticmethod
    def chunk_text(text, chunk_size=4000):
        """
        Splits text into manageable chunks for LLM context windows.
        In a real project, this would be more sophisticated (e.g., overlapping chunks).
        """
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
