import PyPDF2
import io

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from uploaded PDF file with error handling
    """
    try:
        text = ""
        
        # Read the uploaded file
        pdf_bytes = uploaded_file.read()
        pdf_file = io.BytesIO(pdf_bytes)
        
        # Create PDF reader
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception as e:
                print(f"Warning: Could not extract text from page {page_num + 1}")
                continue
        
        # Clean up text
        text = text.strip()
        
        if not text:
            raise ValueError("No text could be extracted from the PDF")
        
        return text
    
    except PyPDF2.PdfReadError as e:
        raise ValueError(f"Error reading PDF file: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing PDF file: {str(e)}")


def clean_text(text):
    """
    Clean extracted text by removing extra whitespace and special characters
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text.strip()
