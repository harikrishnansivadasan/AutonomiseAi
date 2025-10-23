import streamlit as st
import tempfile
import os
from data_extraction.extract import extract_multiple_forms
from summariser import generate_text_summary, generate_holistic_summary
from qa import llm_reply


# Streamlit App Config

st.set_page_config(page_title="Intelligent Form Agent", layout="wide")
st.title("🧾 Intelligent Form Agent")
st.write(
    "Upload one or more PDF, DOCX, or image forms to extract, summarize, and ask questions."
)


# Initialize session_state

if "uploaded_filenames" not in st.session_state:
    st.session_state.uploaded_filenames = []  # stores names of uploaded files
if "results" not in st.session_state:
    st.session_state.results = {}  # stores extracted text
if "summaries" not in st.session_state:
    st.session_state.summaries = {}  # stores per-file summaries
if "holistic_summary" not in st.session_state:
    st.session_state.holistic_summary = ""  # stores combined summary


# File Upload Section

uploaded_files = st.file_uploader(
    "Upload your form files",
    type=[
        "pdf",
        "docx",
        "jpg",
        "jpeg",
        "png",
        "csv",
        "xlsx",
        "xls",
        "json",
        "txt",
        "md",
    ],
    accept_multiple_files=True,
)

if uploaded_files:
    st.info(f"Processing {len(uploaded_files)} file(s)... Please wait.")

    uploaded_filenames = [file.name for file in uploaded_files]

    # Remove deleted files from session state

    removed_files = set(st.session_state.uploaded_filenames) - set(uploaded_filenames)
    for file_name in removed_files:
        st.session_state.results.pop(file_name, None)
        st.session_state.summaries.pop(file_name, None)

    # Update session state with current filenames
    st.session_state.uploaded_filenames = uploaded_filenames

    # Save newly uploaded files temporarily

    new_files = [
        file for file in uploaded_files if file.name not in st.session_state.results
    ]
    temp_files = []
    for file in new_files:
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, file.name)
        with open(temp_path, "wb") as f:
            f.write(file.read())
        temp_files.append(temp_path)

    # Extract text for new files only
    if temp_files:
        with st.spinner("Extracting text for new files..."):
            new_results = extract_multiple_forms(temp_files)
            st.session_state.results.update(new_results)
        st.success("✅ Text extraction completed for new files.")

    # Generate per-file summaries

    for file_path, text in st.session_state.results.items():

        if not text.strip():
            st.error(f"❌ No text extracted from {file_path}")
            continue

        st.subheader(f"📄 {file_path}")

        if file_path not in st.session_state.summaries:
            with st.spinner("Generating summary..."):
                st.session_state.summaries[file_path] = generate_text_summary(text)

        with st.expander("View Summary"):
            st.markdown(st.session_state.summaries[file_path])

    # Generate holistic summary if multiple files

    if len(st.session_state.results) > 1:
        combined_texts = [
            text for text in st.session_state.results.values() if text.strip()
        ]
        if combined_texts:
            with st.spinner("Generating holistic summary..."):
                st.session_state.holistic_summary = generate_holistic_summary(
                    combined_texts
                )

    if st.session_state.holistic_summary:
        st.markdown("---")
        st.subheader("Summary Across All Forms")
        with st.expander("View Holistic Summary"):
            st.markdown(st.session_state.holistic_summary)

    # Sidebar Q&A

    st.sidebar.header("💬 Ask a Question")
    question = st.sidebar.text_input("Enter your question:")

    if question:
        st.sidebar.subheader("Answer")
        valid_texts = [
            text for text in st.session_state.results.values() if text.strip()
        ]

        if not valid_texts:
            st.sidebar.warning("No content available to answer the question.")
        else:
            # Use combined context if multiple files
            combined_text = (
                "\n\n".join(valid_texts) if len(valid_texts) > 1 else valid_texts[0]
            )
            answer = llm_reply(combined_text, question)
            st.sidebar.markdown(f"**Answer:** {answer}")

else:
    st.info("👆 Upload one or more files to begin.")
