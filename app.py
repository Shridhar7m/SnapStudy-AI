import streamlit as st
import fitz

st.set_page_config(
    page_title="SnapStudy AI",
    page_icon="📚"
)

st.title("📚 SnapStudy AI")
st.write("Your AI Learning Assistant")

uploaded_file = st.file_uploader(
    "Upload your study PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    pdf = fitz.open(
        stream=uploaded_file.getvalue(),
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    if text.strip():
        st.success("PDF uploaded successfully!")

        st.subheader("Extracted Text")

        st.text_area(
            "PDF Content",
            text,
            height=400
        )

    else:
        st.warning(
            "No readable text found in this PDF."
        )