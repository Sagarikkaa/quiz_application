from io import BytesIO

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None


def extract_text(uploaded_file):
    content = uploaded_file.read()
    uploaded_file.seek(0)

    if uploaded_file.name.lower().endswith(".pdf"):
        if PdfReader is None:
            raise ImportError("PyPDF2 is required to parse PDF files. Install with pip install PyPDF2")
        reader = PdfReader(BytesIO(content))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        return text

    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("latin-1", errors="ignore")
