import os
from dotenv import load_dotenv
from openai import OpenAI
import pdfplumber

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def extract_text_from_pdf(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

# Load the document once at the start
document_text = extract_text_from_pdf("sample.pdf")

# This system prompt is what forces the model to stay grounded
system_prompt = f"""You are a helpful assistant that answers questions ONLY using the document text provided below.
If the answer is not in the document, say "I couldn't find that in the document." Do not make anything up.

DOCUMENT:
{document_text}
"""

messages = [{"role": "system", "content": system_prompt}]

print("Document loaded. Ask questions about it. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="openrouter/free",
        max_tokens=300,
        messages=messages,
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    print(f"AI: {reply}\n")