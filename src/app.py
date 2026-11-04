
import streamlit as st
import pandas as pd

from detector import detect_pii, mask_pii

st.set_page_config(
    page_title="Team Equinox | Privacy Scanner",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Personal Data Discovery")
st.subheader("Privacy Evidence Inventory")
st.caption("Team Equinox | AIORI-3 Hackathon")

st.write(
    "Upload multiple files to discover, classify "
    "and review personal information."
)

# Multiple file upload
uploaded_files = st.file_uploader(
    "Upload TXT or CSV files",
    type=["txt", "csv"],
    accept_multiple_files=True
)

if uploaded_files:

    results = []

    for uploaded_file in uploaded_files:

        try:
            text = uploaded_file.getvalue().decode("utf-8-sig")
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

        except UnicodeDecodeError:
            st.warning(
                f"Could not read {uploaded_file.name}. "
                "Please use a UTF-8 TXT or CSV file."
            )

    report = pd.DataFrame(results)

    st.success(
        f"Scanned {len(uploaded_files)} uploaded file(s)."
    )

    # Summary
    total = len(results)

    high = sum(
        1 for item in results
        if item["Risk Level"] == "High"
    )

    medium = sum(
        1 for item in results
        if item["Risk Level"] == "Medium"
    )

    low = sum(
        1 for item in results
        if item["Risk Level"] == "Low"
    )

    st.header("📊 Scan Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Findings", total)
    col2.metric("High Risk", high)
    col3.metric("Medium Risk", medium)
    col4.metric("Low Risk", low)

    if not report.empty:

        st.divider()

        # Chart
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

        # Evidence inventory
        st.divider()

        st.header("📋 Privacy Evidence Inventory")

        st.dataframe(
            report,
            use_container_width=True,
            hide_index=True
        )

        # CSV download
        csv_report = report.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Combined Privacy Report",
            data=csv_report,
            file_name="team_equinox_privacy_report.csv",
            mime="text/csv"
        )

    else:
        st.info(
            "No supported personal information was detected "
            "in the uploaded files."
        )
