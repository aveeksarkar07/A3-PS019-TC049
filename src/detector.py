
import re
from datetime import datetime


def is_valid_date(value):
    """Check whether a date is valid."""

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%Y-%m-%d"
    ]

    for date_format in formats:
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            continue

    return False


def passes_luhn(number):
    """Validate a card-number candidate using the Luhn algorithm."""

    digits = [int(digit) for digit in number]

    checksum = 0
    parity = len(digits) % 2

    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2

            if digit > 9:
                digit -= 9

        checksum += digit

    return checksum % 10 == 0


def detect_pii(text):
    """
    Detect common personal information using patterns.
    These matches are potential indicators, not identity verification.
    """

    findings = []

    # Existing detection categories
    patterns = {
        "Email Address": (
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        ),
        "Phone Number": (
            r"\b(?:\+91[- ]?)?[6-9]\d{9}\b"
        ),
        "Indian PIN Code": (
            r"\b[1-9]\d{5}\b"
        ),
        "Aadhaar-like Number": (
            r"(?<!\d)(?:\d{4}[ -]?){2}\d{4}(?!\d)"
        ),
        "PAN-like Number": (
            r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
        )
    }

    # Detect existing and new pattern-based categories
    for pii_type, pattern in patterns.items():

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for match in matches:
            findings.append({
                "type": pii_type,
                "value": match,
                "risk": get_risk_level(pii_type)
            })

    # Detect dates only when a DOB-related label appears nearby
    date_pattern = (
        r"\b(?:\d{2}[/-]\d{2}[/-]\d{4}"
        r"|\d{2}\.\d{2}\.\d{4}"
        r"|\d{4}-\d{2}-\d{2})\b"
    )

    for match in re.finditer(date_pattern, text):

        nearby_text = text[max(0, match.start() - 35):match.start()]

        if re.search(
            r"(?:DOB|date\s+of\s+birth|birth\s+date)\s*[:=-]?\s*$",
            nearby_text,
            re.IGNORECASE
        ):

            if is_valid_date(match.group()):
                findings.append({
                    "type": "Date of Birth",
                    "value": match.group(),
                    "risk": get_risk_level("Date of Birth")
                })

    # Detect card-number candidates and validate with Luhn
    card_pattern = r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)"

    for match in re.finditer(card_pattern, text):

        original_value = match.group()
        digits_only = re.sub(r"[ -]", "", original_value)

        if 13 <= len(digits_only) <= 19:
            if passes_luhn(digits_only):
                findings.append({
                    "type": "Credit/Debit Card-like Number",
                    "value": original_value,
                    "risk": get_risk_level(
                        "Credit/Debit Card-like Number"
                    )
                })

    return findings


def mask_pii(value, pii_type):

    if pii_type == "Email Address":
        parts = value.split("@")
        return parts[0][:2] + "****@" + parts[1]

    elif pii_type == "Phone Number":
        return value[:2] + "XXXXXX" + value[-2:]

    elif pii_type == "Indian PIN Code":
        return "XX" + value[-4:]

    elif pii_type == "Aadhaar-like Number":
        digits = re.sub(r"\D", "", value)
        return "XXXX XXXX " + digits[-4:]

    elif pii_type == "PAN-like Number":
        return value[:2] + "******" + value[-2:]

    elif pii_type == "Date of Birth":
        return "XX/XX/XXXX"

    elif pii_type == "Credit/Debit Card-like Number":
        digits = re.sub(r"\D", "", value)
        return "XXXX XXXX XXXX " + digits[-4:]

    return "********"


def get_risk_level(pii_type):

    risk_levels = {
        "Email Address": "High",
        "Phone Number": "High",
        "Indian PIN Code": "Low",
        "Aadhaar-like Number": "High",
        "PAN-like Number": "High",
        "Date of Birth": "Medium",
        "Credit/Debit Card-like Number": "High"
    }

    return risk_levels.get(pii_type, "Medium")
