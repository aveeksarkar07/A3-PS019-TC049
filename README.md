[Proposed-structure-hackathon.pdf](https://github.com/user-attachments/files/33433432/Proposed-structure-hackathon.pdf)
[Proposed-structure-hackathon.pptx](https://github.com/user-attachments/files/33433431/Proposed-structure-hackathon.pptx)
# AIORI-3-HACKATHON-PROJECTS
This repository will contain the code and resources for the AIORI-3 hackathon that will be developed during the AIORI-3.

## TEAM INTRODUCTION VIDEO
YOUTUBE : https://youtu.be/90jJaUa5YGM?si=TtDoho6tvs5y72EQ

# 🔐 EQUINOX
### Personal Data Discovery & Privacy Evidence Inventory

**AIORI-3 Hackathon | Team Equinox**

## 📌 About the Project

EQUINOX is a privacy-focused tool designed to discover, classify and organize potential Personally Identifiable Information (PII) from digital documents.

It scans supported files, identifies potential sensitive information, assigns risk levels, masks detected values and generates structured privacy evidence reports.

## ✨ Key Features

- **Multi-format scanning:** Supports TXT, CSV, PDF and DOCX files.
- **PII Detection:** Detects email addresses, phone numbers, Indian PIN codes, Aadhaar-like numbers, PAN-like numbers, dates of birth and card-like numbers.
- **Risk Classification:** Categorizes findings into High, Medium and Low risk.
- **Data Masking:** Displays sensitive information in masked form.
- **Duplicate Detection:** Groups repeated findings within the same file.
- **Occurrence Counting:** Shows how many times each unique finding appears.
- **File-wise Risk Summary:** Provides a separate summary for each uploaded document.
- **Interactive Dashboard:** Displays risk and PII category visualizations.
- **Searchable Evidence Inventory:** Allows users to search detected findings.
- **Report Generation:** Exports findings in Excel, CSV and PDF formats.

## 🛠️ Technology Stack

- Python
- Streamlit
- Pandas
- Regular Expressions
- PyPDF
- Python-docx
- ReportLab
- Openpyxl

## 📂 Project Structure

```text
A3-PS019-TC049/
│
├── src/
│   ├── app.py
│   ├── detector.py
│   ├── file_reader.py
│   ├── test_detector.py
│   ├── sample.txt
│   ├── sample2.txt
│   └── utils/
│
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/aveeksarkar07/A3-PS019-TC049.git
```

### 2. Navigate into the project

```bash
cd A3-PS019-TC049
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
cd src
python3 -m streamlit run app.py
```

The application will open in your browser.

## 🧪 Running Tests

Navigate to the `src` directory and execute:

```bash
python3 -m unittest test_detector -v
```

The current detector test suite contains 13 automated tests.

## 🔒 Privacy Considerations

- Detected values are masked before being displayed in the evidence inventory.
- Raw matching values are used temporarily in memory for duplicate grouping.
- Temporary uploaded files are removed after processing.
- Reports contain masked findings rather than original detected values.
- Fictional data should be used for testing and demonstrations.

## ⚠️ Limitations

- Detection is based on pattern matching and contextual rules.
- Aadhaar, PAN and card-like matches are not official identity verification.
- Card checksum validation does not establish whether a card exists or belongs to anyone.
- Scanned image PDFs are not currently supported by the text extraction pipeline.
- DOCX table contents are not currently included in extraction.

## 👥 Team

**Team Equinox**

AIORI-3 Hackathon

---

*EQUINOX — Discover. Classify. Protect.*
