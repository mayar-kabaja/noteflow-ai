"""
Book text extraction service for various file formats
"""
import os
from pypdf import PdfReader
import ebooklib
from ebooklib import epub
from docx import Document
from bs4 import BeautifulSoup


def extract_text_from_pdf(filepath):
    """Extract text from PDF file"""
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_epub(filepath):
    """Extract text from EPUB file"""
    try:
        book = epub.read_epub(filepath)
        text = ""

        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Parse HTML content
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text += soup.get_text() + "\n"

        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from EPUB: {str(e)}")


def extract_text_from_docx(filepath):
    """Extract text from DOCX file"""
    try:
        doc = Document(filepath)
        text = ""

        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")


def extract_text_from_txt(filepath):
    """Extract text from TXT file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from TXT: {str(e)}")


def extract_text_from_book(filepath, file_type):
    """
    Extract text from book file based on type

    Args:
        filepath: Path to the book file
        file_type: Type of file (pdf, epub, docx, txt)

    Returns:
        Extracted text content
    """
    file_type = file_type.lower()

    extractors = {
        'pdf': extract_text_from_pdf,
        'epub': extract_text_from_epub,
        'docx': extract_text_from_docx,
        'doc': extract_text_from_docx,  # Try DOCX extractor for DOC files
        'txt': extract_text_from_txt
    }

    if file_type not in extractors:
        raise Exception(f"Unsupported file type: {file_type}")

    extractor = extractors[file_type]
    text = extractor(filepath)

    if not text or len(text.strip()) < 50:
        raise Exception("No text content found in the file")

    return text


def get_book_title_from_text(text, filename):
    """
    Try to extract book title from text or use filename

    Args:
        text: Full book text
        filename: Original filename

    Returns:
        Book title
    """
    # Try to get title from first few lines
    lines = text.split('\n')
    for line in lines[:10]:
        line = line.strip()
        if line and len(line) < 100:  # Likely a title
            return line

    # Fallback to filename
    return os.path.splitext(filename)[0]
