import streamlit as st
from PyPDF2 import PdfReader
import docx

# Function to check NDA text against company rules
def check_nda(nda_text):
    # Initialize results
    results = {"status": "Requires Internal Review", "suggestions": []}
    
    # Rule 1: Definition of Confidential Information should not be too broad
    if "confidential information" in nda_text.lower():
        if "publicly available" not in nda_text.lower() and "independently developed" not in nda_text.lower():
            results["suggestions"].append("Define confidential information more narrowly to exclude publicly available or independently developed data.")
    
    # Rule 2: Confidentiality term should not exceed 3 years (except for trade secrets)
    if "confidentiality period" in nda_text.lower():
        if "3 years" not in nda_text.lower() and "trade secret" not in nda_text.lower():
            results["suggestions"].append("Confidentiality period should not exceed 3 years, except for trade secrets.")
    
    # Rule 3: Jurisdiction should be Minnesota or Delaware
    if "jurisdiction" in nda_text.lower():
        if "Minnesota" not in nda_text.lower() and "Delaware" not in nda_text.lower():
            results["suggestions"].append("Jurisdiction should be Minnesota or Delaware.")
    
    # Rule 4: Include a clause for return or destruction of confidential information
    if "return of confidential information" not in nda_text.lower():
        results["suggestions"].append("Include a clause requiring the return or destruction of confidential information upon termination.")
    
    # Rule 5: Exclusions from confidentiality (publicly available, lawful third-party, etc.)
    if "confidential information" in nda_text.lower():
        if "public" not in nda_text.lower() or "lawfully obtained" not in nda_text.lower():
            results["suggestions"].append("Ensure exclusions from confidentiality for publicly available and lawfully obtained information.")
    
    # Rule 6: Non-solicitation clauses should not be overly restrictive
    if "non-solicitation" in nda_text.lower():
        if "reasonable" not in nda_text.lower() or "scope" not in nda_text.lower():
            results["suggestions"].append("Non-solicitation clauses should be reasonable in scope, duration, and geographical area.")
    
    # Rule 7: Governing law should be Minnesota or Delaware
    if "governing law" in nda_text.lower():
        if "Minnesota" not in nda_text.lower() and "Delaware" not in nda_text.lower():
            results["suggestions"].append("Governing law should be Minnesota or Delaware.")
    
    # Rule 8: Include a waiver of rights clause
    if "waiver" not in nda_text.lower():
        results["suggestions"].append("Include a clause stating that a waiver of rights does not waive future rights.")
    
    # Additional Rules
    # Rule 9: Indemnification clause
    if "indemnification" not in nda_text.lower():
        results["suggestions"].append("Include an indemnification clause protecting the company from losses due to breaches.")
    
    # Rule 10: No license grant
    if "license" not in nda_text.lower():
        results["suggestions"].append("Include a clause stating that no license is granted by the NDA.")
    
    # Rule 11: Automatic termination on breach
    if "termination" not in nda_text.lower():
        results["suggestions"].append("Include an automatic termination clause upon breach of confidentiality.")
    
    # Rule 12: No reverse engineering
    if "reverse engineering" not in nda_text.lower():
        results["suggestions"].append("Include a clause prohibiting reverse engineering or creation of derivative works from confidential information.")
    
    # Rule 13: Ownership of confidential information
    if "ownership" not in nda_text.lower():
        results["suggestions"].append("Clarify that confidential information remains the property of the disclosing party.")
    
    # Rule 14: Access to confidential information
    if "access to confidential information" not in nda_text.lower():
        results["suggestions"].append("Include a clause specifying that only employees with a need to know can access the confidential information.")
    
    # Final Decision
    if len(results["suggestions"]) == 0:
        results["status"] = "Approved"
    elif len(results["suggestions"]) > 0:
        results["status"] = "Approved with Suggestions"
    
    return results

# Streamlit Interface
def display_nda_review_tool():
    st.title("NDA Review Tool")
    
    # File Upload Section
    uploaded_file = st.file_uploader("Upload your NDA document", type=["pdf", "docx"])
    if uploaded_file is not None:
        # Extract text from PDF
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            nda_text = ""
            for page in reader.pages:
                nda_text += page.extract_text()
        
        # Extract text from Word Document
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            nda_text = ""
            for para in doc.paragraphs:
                nda_text += para.text
        
        # Display extracted text for user reference
        st.subheader("Extracted NDA Text:")
        st.text_area("NDA Text", nda_text, height=300)

        # Check NDA rules and provide feedback
        results = check_nda(nda_text)
        st.subheader("Review Results:")
        st.write(f"**Status**: {results['status']}")
        
        if len(results["suggestions"]) > 0:
            st.write("**Suggestions for Improvement**:")
            for suggestion in results["suggestions"]:
                st.write(f"- {suggestion}")
        else:
            st.write("No suggestions needed. NDA is approved.")

# Run the app
if __name__ == "__main__":
    display_nda_review_tool()