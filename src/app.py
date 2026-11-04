import streamlit as st
import pandas as pd
import tempfile
import os
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from detector import detect_pii, mask_pii
from file_reader import read_file
def generate_pdf_report(report, total, high, medium, low):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph(
            "TEAM EQUINOX",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Personal Data Discovery & Privacy Evidence Inventory",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 8 * mm))

    elements.append(
        Paragraph("SCAN SUMMARY", styles["Heading2"])
    )

    summary_data = [
        ["Total Findings", "High Risk", "Medium Risk", "Low Risk"],
        [str(total), str(high), str(medium), str(low)]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[60 * mm] * 4
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172554")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#E8EEF8")),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 10)
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 10 * mm))

    elements.append(
        Paragraph("PRIVACY EVIDENCE INVENTORY", styles["Heading2"])
    )

    table_data = [[
        "File Name",
        "PII Category",
        "Masked Value",
        "Risk Level"
    ]]

    for _, row in report.iterrows():
        table_data.append([
            str(row["File Name"]),
            str(row["PII Category"]),
            str(row["Masked Value"]),
            str(row["Risk Level"])
        ])

    evidence_table = Table(
        table_data,
        repeatRows=1,
        colWidths=[65 * mm, 65 * mm, 65 * mm, 35 * mm]
    )

    evidence_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172554")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#E8EEF8")])
    ]))

    elements.append(evidence_table)
    elements.append(Spacer(1, 8 * mm))

    elements.append(
        Paragraph(
            "Note: Findings are potential pattern matches, "
            "not official identity verification.",
            styles["Italic"]
        )
    )

    document.build(elements)

    buffer.seek(0)
    return buffer.getvalue()

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Equinox | Privacy Scanner",
    page_icon="🔐",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #0b1020;
    color: #f1f5f9;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 30px;
    border-radius: 18px;
    background: linear-gradient(120deg, #172554, #312e81);
    border: 1px solid #3730a3;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 36px;
    margin-bottom: 8px;
}

.hero p {
    color: #c7d2fe;
    font-size: 16px;
}

div[data-testid="stMetric"] {
    background: #151d32;
    border: 1px solid #26334f;
    padding: 18px;
    border-radius: 12px;
}

div[data-testid="stMetricLabel"] {
    color: #cbd5e1;
}

div[data-testid="stMetricValue"] {
    color: white;
}

h2, h3 {
    color: #e2e8f0;
}

.stButton button {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>🔐 EQUINOX</h1>
    <p>Personal Data Discovery & Privacy Evidence Inventory</p>
    <p>AIORI-3 Hackathon | Team Equinox</p>
</div>
""", unsafe_allow_html=True)

st.write(
    "Discover, classify and review potential personal "
    "information across multiple digital files."
)

st.info(
    "Privacy note: Files are processed for this scan. "
    "Findings are displayed in masked form. Detection results "
    "are pattern matches, not official identity verification."
)


# ---------------- FILE UPLOAD ----------------

st.header("📂 Upload Documents")

uploaded_files = st.file_uploader(
    "Choose TXT, CSV, PDF or DOCX files",
    type=["txt", "csv", "pdf", "docx"],
    accept_multiple_files=True
)


# ---------------- SCANNING ----------------

if uploaded_files:

    results = []
    errors = []

    with st.spinner("Scanning your documents..."):

        for uploaded_file in uploaded_files:

            temp_path = None

            try:
                suffix = "." + uploaded_file.name.split(".")[-1].lower()

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix
                ) as temp_file:

                    temp_file.write(uploaded_file.getvalue())
                    temp_path = temp_file.name

                text = read_file(temp_path)
                findings = detect_pii(text)

                for item in findings:
                    results.append({
                        "File Name": uploaded_file.name,
                        "PII Category": item["type"],
                        "Masked Value": mask_pii(
                            item["value"],
                            item["type"]
                        ),
                        "Risk Level": item["risk"]
                    })

            except Exception as e:
                errors.append(
                    f"{uploaded_file.name}: {e}"
                )

            finally:
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)

    for error in errors:
        st.warning(f"Could not read {error}")

    report = pd.DataFrame(
        results,
        columns=[
            "File Name",
            "PII Category",
            "Masked Value",
            "Risk Level"
        ]
    )

    st.success(
        f"Scan completed: {len(uploaded_files)} file(s) processed."
    )

    # ---------------- OVERVIEW ----------------

    st.divider()
    st.header("📊 Scan Overview")

    total = len(results)

    high = sum(
        item["Risk Level"] == "High"
        for item in results
    )

    medium = sum(
        item["Risk Level"] == "Medium"
        for item in results
    )

    low = sum(
        item["Risk Level"] == "Low"
        for item in results
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Findings", total)
    col2.metric("🔴 High Risk", high)
    col3.metric("🟠 Medium Risk", medium)
    col4.metric("🟢 Low Risk", low)

    # ---------------- RESULTS ----------------

    if not report.empty:

        st.divider()
        st.header("📈 PII Distribution")

        category_counts = (
            report["PII Category"]
            .value_counts()
            .rename_axis("Category")
            .reset_index(name="Count")
        )

        st.bar_chart(
            category_counts,
            x="Category",
            y="Count"
        )

        st.divider()
        st.header("📋 Privacy Evidence Inventory")

        st.dataframe(
            report,
            use_container_width=True,
            hide_index=True
        )

        # ---------------- DOWNLOAD ----------------

        st.divider()
        st.header("📥 Export Report")

        csv_report = report.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Privacy Report (CSV)",
            data=csv_report,
            file_name="team_equinox_privacy_report.csv",
            mime="text/csv"
        )
        pdf_report = generate_pdf_report(
            report,
            total,
            high,
            medium,
            low
        )

        st.download_button(
            label="Download Privacy Report (PDF)",
            data=pdf_report,
            file_name="team_equinox_privacy_report.pdf",
            mime="application/pdf"
        )

    else:
        st.info(
            "No supported personal information patterns were detected."
        )

else:
    st.markdown("""
    ### 🚀 Ready to scan

    Upload one or more supported documents to begin.

    **Supported formats:** TXT · CSV · PDF · DOCX

    Your privacy evidence inventory will appear here after scanning.
    """)