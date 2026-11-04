
import csv
from pathlib import Path
from pypdf import PdfReader
from docx import Document


def read_file(file_path):
    """
    Read TXT, CSV, PDF and DOCX files.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")

    elif path.suffix.lower() == ".csv":
        rows = []

        with path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.reader(file)

            for row in reader:
                rows.append(" ".join(row))

        return "\n".join(rows)

    elif path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    elif path.suffix.lower() == ".docx":
        document = Document(str(path))
        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    else:
        raise ValueError(
            "Only TXT, CSV, PDF and DOCX files are supported."
        )
