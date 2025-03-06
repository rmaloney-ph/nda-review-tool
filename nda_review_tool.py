import streamlit as st
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(pdf_file):
    """Extract text from a given PDF file"""
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    """Extract text from a given DOCX file"""
    doc = Document(docx_file)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text

def analyze_nda(text):
    """Analyze the NDA text for key clauses and flag issues."""
    issues = []

    # 1. Check for confidentiality duration (should be defined)
    if "confidential" in text.lower():
        if "years" not in text.lower() and "duration" not in text.lower():
            issues.append("Missing clear duration for confidentiality clause.")

    # 2. Look for governing law section (common in NDAs)
    if "governing law" not in text.lower():
        issues.append("No governing law clause found. This is typically required.")

    # 3. Analyze term and termination conditions
    if "termination" not in text.lower() and "term" not in text.lower():
        issues.append("No termination clause found. It is important to define how the NDA can be terminated.")

    # 4. Review for the inclusion of non-compete terms (if applicable)
    if "non-compete" in text.lower():
        issues.append("Non-compete clause found. Ensure it aligns with local laws.")

    # 5. Inconsistencies in the wording of the confidentiality clause
    if "confidential" in text.lower() and "public" in text.lower():
        issues.append("The document contains potential conflicts between confidentiality and public domain clauses.")

    # 6. Look for mutual NDA (check for both parties being protected)
    if "mutual" not in text.lower():
        issues.append("No mutual confidentiality clause found. This could be one-sided.")

    # 7. General review for commonly overlooked clauses
    if "dispute resolution" not in text.lower():
        issues.append("No dispute resolution process defined. It is important to specify how disputes will be handled.")

    return issues

# Streamlit App UI
st.title("NDA Review Tool")

st.write(
    "Upload an NDA document (PDF or Word format) and the tool will review the document for common issues, missing clauses, and potential inconsistencies."
)

# File upload
uploaded_file = st.file_uploader("Upload NDA (PDF or Word)", type=["pdf", "docx"])

if uploaded_file is not None:
    # Check file type and extract text accordingly
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(uploaded_file)

    # Display the first 1000 characters of the document for preview
    st.write("### NDA Content Preview:")
    st.write(text[:1000])

    # Perform analysis
    issues = analyze_nda(text)

    # Display issues or feedback
    if issues:
        st.write("### Issues Found:")
        for issue in issues:
            st.warning(issue)
    else:
        st.write("### No major issues found. The NDA appears to be in good shape.")