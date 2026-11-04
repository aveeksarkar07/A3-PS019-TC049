import csv
from pathlib import Path
from pypdf import PdfReader
from docx import Document


def read_file(file_path):
    """
    Read TXT, CSV, PDF and DOCX files.
    Supports paragraphs and tables in DOCX files.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read TXT files
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")

    # Read CSV files
    elif path.suffix.lower() == ".csv":
        rows = []

        with path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.reader(file)

            for row in reader:
                rows.append(" ".join(row))

        return "\n".join(rows)

    # Read PDF files
    elif path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    # Read DOCX files, including tables
    elif path.suffix.lower() == ".docx":
        document = Document(str(path))

        extracted_text = []

        # Read normal paragraphs
        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                extracted_text.append(paragraph.text)

        # Read tables
        for table in document.tables:
            for row in table.rows:
                row_data = []

                for cell in row.cells:
                    row_data.append(cell.text.strip())

                extracted_text.append(" | ".join(row_data))

        return "\n".join(extracted_text)

    else:
        raise ValueError(
            "Only TXT, CSV, PDF and DOCX files are supported."
        )