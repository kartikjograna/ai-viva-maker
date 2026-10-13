import streamlit as st
from services.document_service import DocumentService
from database.db import add_document

def show():
    st.title("📁 Upload Study Material")
    st.markdown("Upload your PDFs, DOCX, or TXT files to build your question bank.")

    with st.form("upload_form"):
        subject = st.text_input("Subject Name (e.g., Operating Systems)")
        topic = st.text_input("Topic (e.g., CPU Scheduling)")
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
        submit = st.form_submit_button("Process Document")

    if submit:
        if not subject or not topic or not uploaded_file:
            st.error("Please provide subject, topic, and a file.")
            return

        with st.spinner("Extracting text from document..."):
            try:
                # Extract text
                text = DocumentService.extract_text(uploaded_file)
                cleaned_text = DocumentService.clean_text(text)

                if not cleaned_text:
                    st.error("The uploaded document seems to be empty.")
                    return

                # Show extracted text preview
                st.subheader("📄 Extracted Text Preview")
                st.text_area("Content", cleaned_text[:2000] + "...", height=300)

                # Save to DB
                doc_id = add_document(subject, topic, cleaned_text, uploaded_file.name)
                st.success(f"Successfully uploaded {uploaded_file.name}! Document ID: {doc_id}")

            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
