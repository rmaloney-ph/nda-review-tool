import streamlit as st
from PyPDF2 import PdfReader  # This should now work after you add PyPDF2 to the requirements.txt

# Define some basic rules for NDA approval
def check_terms(nda_text):
    """ Check if the terms of the NDA are acceptable """
    term_valid = "trade secrets" in nda_text.lower() or "confidentiality" in nda_text.lower()
    return term_valid

def check_jurisdiction(nda_text):
    """ Check if the jurisdiction is either Minnesota or Delaware """
    return "Minnesota" in nda_text or "Delaware" in nda_text

def check_definition_of_confidential_info(nda_text):
    """ Ensure the definition of confidential information isn't too broad """
    return "confidential" in nda_text and "proprietary" in nda_text

# Add logic for document review
def review_nda(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    
    is_valid_term = check_terms(text)
    is_valid_jurisdiction = check_jurisdiction(text)
    is_valid_confidential_info = check_definition_of_confidential_info(text)

    # Create an approval status based on the checks
    if not is_valid_term:
        return "Requires internal review: Terms are too broad."
    elif not is_valid_jurisdiction:
        return "Requires internal review: Jurisdiction issue."
    elif not is_valid_confidential_info:
        return "Requires internal review: Confidential information is defined too broadly."
    else:
        return "Approved: NDA meets the company's requirements."

# Streamlit UI
st.title("NDA Review Tool")
st.write("Upload your NDA PDF file for review.")

# File upload input
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    status = review_nda(uploaded_file)
    st.write(f"**Status**: {status}")