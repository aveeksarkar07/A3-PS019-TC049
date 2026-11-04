import csv
from pathlib import Path


def read_file(file_path):
    """
    Read TXT or CSV files and return their text content.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")

    elif path.suffix.lower() == ".csv":
        rows = []

        with path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)

            for row in reader:
                rows.append(" ".join(row))

        return "\n".join(rows)

    else:
        raise ValueError("Only TXT and CSV files are supported.")