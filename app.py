import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import pdfplumber

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def extract_text_from_pdf(uploaded_file):
    full_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

st.set_page_config(page_title="Document Q&A", page_icon="📄")
st.title("📄 Document Q&A Assistant")
st.write("Upload a document (like an insurance policy) and ask questions about it.")

# Keep the document text and chat history alive between interactions
if "document_text" not in st.session_state:
    st.session_state.document_text = None
if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None and st.session_state.document_text is None:
    with st.spinner("Reading document..."):
        st.session_state.document_text = extract_text_from_pdf(uploaded_file)
    st.success("Document loaded! Ask your questions below.")

# Show past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if st.session_state.document_text:
    user_question = st.chat_input("Ask a question about the document...")

    if user_question:
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.write(user_question)

        system_prompt = f"""You are a helpful assistant that answers questions ONLY using the document text provided below.
If the answer is not in the document, say "I couldn't find that in the document." Do not make anything up.

DOCUMENT:
{st.session_state.document_text}
"""

        api_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="openrouter/free",
                    max_tokens=300,
                    messages=api_messages,
                )
                reply = response.choices[0].message.content
                st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
else:
    st.info("Upload a PDF above to get started.")