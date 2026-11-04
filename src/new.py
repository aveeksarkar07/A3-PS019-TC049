
import re

def detect_pii(text):
    """
    Detect common personally identifiable information.
    """

    patterns = {
        "Email Address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "Phone Number": r"\b(?:\+91[- ]?)?[6-9]\d{9}\b",
        "Indian PIN Code": r"\b[1-9]\d{5}\b"
    }

    findings = []

    for pii_type, pattern in patterns.items():
        matches = re.findall(pattern, text)

        for match in matches:
            findings.append({
                "type": pii_type,
                "value": match,
                "risk": "Medium"
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

    return "********"