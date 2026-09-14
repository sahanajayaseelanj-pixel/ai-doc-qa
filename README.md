# AI Document Q&A

A simple Streamlit app that lets you upload a PDF and ask questions about its contents. Answers are generated through OpenRouter and are limited to the text extracted from the uploaded document.

## Requirements

- Python 3.10 or newer
- An OpenRouter API key

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```text
OPENROUTER_API_KEY=your_api_key_here
```

## Run

Start the app with:

```powershell
streamlit run app.py
```

Open the local URL shown by Streamlit, upload a PDF, and ask questions about it.

## Project Files

- `app.py`: Streamlit application
- `extract.py`: PDF text extraction utility
- `chat.py` and `doc_qa.py`: Supporting modules
- `sample.pdf`: Example document