# 🧾 Intelligent Form Agent

The **Intelligent Form Agent** is a Streamlit-based application that allows users to:

- Upload one or multiple documents (PDF, DOCX, images, etc.)
- Extract text from the uploaded documents
- Generate per-document summaries
- Generate a holistic summary across multiple documents
- Ask questions about the uploaded documents using a sidebar Q&A interface powered by the Groq API

This tool is useful for quickly analyzing resumes, reports, or forms and retrieving insights without manual reading.

---

## Features

1. **Text Extraction** – Extract text from multiple document formats.
2. **Per-Document Summaries** – Automatically generates concise summaries.
3. **Holistic Summary** – Combines all uploaded documents into a single summary.
4. **Q&A Interface** – Ask questions in the sidebar and get answers from the uploaded documents.
5. **Session Persistence** – Added/removed files are tracked, and summaries are cached for faster interaction.

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/harikrishnansivadasan/AutonomiseAi.git
cd intelligent-form-agent
```
### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install required Packages
```bash
pip install -r requirements.txt
```
### 4. Configure environment variables
```bash
create a .env file in the project directory
add your Groq api key ( get it from - https://console.groq.com/keys )
For a step-by-step video guide, see this [YouTube tutorial](https://youtu.be/TTG7Uo8lS1M?si=CM4AcN4M7r9POmZT).

GROQ_API_KEY=your_api_key_here
```

### 5. Running the Application
```bash
streamlit run src/app.py
```
## Using the Agent

1.  **Upload Documents:** PDF, DOCX, JPG, PNG, etc.
    
2.  **View Per-Document Summary:** Click the expander under each document.
    
3.  **View Holistic Summary:** If multiple files are uploaded, a combined summary will appear.
    
4.  **Ask Questions:** Enter queries in the sidebar Q&A interface.
    
    -   If multiple files are uploaded, the system will combine all documents for context.
        
    -   Example queries:
        
        -   _“Who has done the most projects?”_
            
        -   _“List key skills of each individual.”_
            
        -   _“Summarize education and experience.”_

![Example](https://github.com/harikrishnansivadasan/AutonomiseAi/blob/main/tests/multiform/Intelligent-Form-Agent.png)