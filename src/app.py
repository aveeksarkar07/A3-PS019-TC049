
import streamlit as st
import pandas as pd
import tempfile
import os
from io import BytesIO

from detector import detect_pii, mask_pii
from file_reader import read_file

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# ---------------- PDF REPORT GENERATOR ----------------

def generate_pdf_report(report, file_summary, total, occurrences,
                        high, medium, low):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("TEAM EQUINOX", styles["Title"])
    )

    elements.append(
        Paragraph(
            "Personal Data Discovery & Privacy Evidence Inventory",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 8 * mm))

    # Overall summary

    elements.append(
        Paragraph("OVERALL SCAN SUMMARY", styles["Heading2"])
    )

    summary_data = [
        [
            "Unique Findings",
            "Total Occurrences",
            "High Risk",
            "Medium Risk",
            "Low Risk"
        ],
        [
            str(total),
            str(occurrences),
            str(high),
            str(medium),
            str(low)
        ]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[50 * mm] * 5
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172554")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#E8EEF8")),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 7)
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 8 * mm))

    # File-wise summary

    elements.append(
        Paragraph("FILE-WISE RISK SUMMARY", styles["Heading2"])
    )

    file_data = [[
        "File Name",
        "Unique Findings",
        "Occurrences",
        "High",
        "Medium",
        "Low"
    ]]

    for _, row in file_summary.iterrows():
        file_data.append([
            str(row["File Name"]),
            str(row["Unique Findings"]),
            str(row["Occurrences"]),
            str(row["High Risk"]),
            str(row["Medium Risk"]),
            str(row["Low Risk"])
        ])

    file_table = Table(
        file_data,
        repeatRows=1,
        colWidths=[85 * mm, 35 * mm, 35 * mm, 25 * mm, 25 * mm, 25 * mm]
    )

    file_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172554")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#E8EEF8")])
    ]))

    elements.append(file_table)
    elements.append(Spacer(1, 8 * mm))

    # Evidence inventory

    elements.append(
        Paragraph("PRIVACY EVIDENCE INVENTORY", styles["Heading2"])
    )

    evidence_data = [[
        "File Name",
        "PII Category",
        "Masked Value",
        "Risk Level",
        "Occurrences"
    ]]

    for _, row in report.iterrows():
        evidence_data.append([
            str(row["File Name"]),
            str(row["PII Category"]),
            str(row["Masked Value"]),
            str(row["Risk Level"]),
            str(row["Occurrences"])
        ])

    evidence_table = Table(
        evidence_data,
        repeatRows=1,
        colWidths=[55 * mm, 50 * mm, 80 * mm, 30 * mm, 25 * mm]
    )

    evidence_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172554")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (4, 0), (4, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 6),
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
    "Privacy note: Findings are displayed in masked form. "
    "Detection results are pattern matches, not official identity "
    "verification. Use fictional data for testing."
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
                        "Risk Level": item["risk"],
                        "Match Key": item["value"]
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

    # ---------------- GROUP DUPLICATES ----------------

    report = pd.DataFrame(results)

    if not report.empty:

        report = (
            report.groupby(
                [
                    "File Name",
                    "PII Category",
                    "Masked Value",
                    "Risk Level",
                    "Match Key"
                ],
                as_index=False
            )
            .size()
            .rename(columns={"size": "Occurrences"})
        )

        report = report.drop(columns=["Match Key"])

    else:

        report = pd.DataFrame(
            columns=[
                "File Name",
                "PII Category",
                "Masked Value",
                "Risk Level",
                "Occurrences"
            ]
        )

    st.success(
        f"Scan completed: {len(uploaded_files)} file(s) processed."
    )

    # ---------------- OVERALL SUMMARY ----------------

    st.divider()
    st.header("📊 Overall Scan Overview")

    total = len(report)

    occurrences = (
        int(report["Occurrences"].sum())
        if not report.empty else 0
    )

    high = int((report["Risk Level"] == "High").sum())
    medium = int((report["Risk Level"] == "Medium").sum())
    low = int((report["Risk Level"] == "Low").sum())

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Unique Findings", total)
    col2.metric("Total Occurrences", occurrences)
    col3.metric("🔴 High Risk", high)
    col4.metric("🟠 Medium Risk", medium)
    col5.metric("🟢 Low Risk", low)

    # ---------------- FILE-WISE SUMMARY ----------------

    st.divider()
    st.header("📁 File-wise Risk Summary")

    if not report.empty:

        file_summary = (
            report.groupby("File Name")
            .agg(
                **{
                    "Unique Findings": ("PII Category", "count"),
                    "Occurrences": ("Occurrences", "sum"),
                    "High Risk": (
                        "Risk Level",
                        lambda x: (x == "High").sum()
                    ),
                    "Medium Risk": (
                        "Risk Level",
                        lambda x: (x == "Medium").sum()
                    ),
                    "Low Risk": (
                        "Risk Level",
                        lambda x: (x == "Low").sum()
                    )
                }
            )
            .reset_index()
        )

        st.dataframe(
            file_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        file_summary = pd.DataFrame(
            columns=[
                "File Name",
                "Unique Findings",
                "Occurrences",
                "High Risk",
                "Medium Risk",
                "Low Risk"
            ]
        )

        st.info("No findings available for the file-wise summary.")

    # ---------------- RISK DISTRIBUTION ----------------

    if not report.empty:

        st.divider()
        st.header("📈 Risk Distribution")

        risk_counts = (
            report["Risk Level"]
            .value_counts()
            .reindex(["High", "Medium", "Low"], fill_value=0)
            .rename_axis("Risk Level")
            .reset_index(name="Unique Findings")
        )

        st.bar_chart(
            risk_counts,
            x="Risk Level",
            y="Unique Findings"
        )

        st.header("📊 PII Category Distribution")

        category_counts = (
            report["PII Category"]
            .value_counts()
            .rename_axis("Category")
            .reset_index(name="Unique Findings")
        )

        st.bar_chart(
            category_counts,
            x="Category",
            y="Unique Findings"
        )

    # ---------------- SEARCHABLE INVENTORY ----------------

    st.divider()
    st.header("📋 Privacy Evidence Inventory")

    if not report.empty:

        st.caption(
            "Duplicate findings within the same file are grouped. "
            "Raw matching values are not included in this inventory."
        )

        search_text = st.text_input(
            "🔎 Search evidence",
            placeholder="Search file name, category or risk level..."
        )

        filtered_report = report.copy()

        if search_text:
            search_columns = [
                "File Name",
                "PII Category",
                "Risk Level"
            ]

            mask = filtered_report[search_columns].apply(
                lambda column: column.astype(str).str.contains(
                    search_text,
                    case=False,
                    na=False
                )
            ).any(axis=1)

            filtered_report = filtered_report[mask]

        st.dataframe(
            filtered_report,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Showing {len(filtered_report)} of {len(report)} unique findings."
        )

    # ---------------- EXPORT REPORTS ----------------

    st.divider()
    st.header("📥 Export Reports")

    if not report.empty:

        csv_buffer = BytesIO()

        with pd.ExcelWriter(csv_buffer, engine="openpyxl") as writer:
            report.to_excel(
                writer,
                sheet_name="Evidence Inventory",
                index=False
            )

            file_summary.to_excel(
                writer,
                sheet_name="File-wise Summary",
                index=False
            )

        st.download_button(
            label="Download Excel Report",
            data=csv_buffer.getvalue(),
            file_name="team_equinox_privacy_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        csv_report = report.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download CSV Report",
            data=csv_report,
            file_name="team_equinox_privacy_report.csv",
            mime="text/csv"
        )

        pdf_report = generate_pdf_report(
            report,
            file_summary,
            total,
            occurrences,
            high,
            medium,
            low
        )

        st.download_button(
            label="Download PDF Report",
            data=pdf_report,
            file_name="team_equinox_privacy_report.pdf",
            mime="application/pdf"
        )

    else:

        st.info("No findings available to export.")

else:

    st.markdown("""
    ### 🚀 Ready to scan

    Upload one or more supported documents to begin.

    **Supported formats:** TXT · CSV · PDF · DOCX

    Your privacy evidence inventory will appear here after scanning.
    """)
