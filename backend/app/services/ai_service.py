import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Find the project root:
# ai-business-assistant/
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Load the exact .env file
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_FILE)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        f"GEMINI_API_KEY is not configured. Checked: {ENV_FILE}"
    )


client = genai.Client(api_key=API_KEY)


def generate_answer(question: str, context: str) -> str:

    prompt = f"""
You are an AI Business Assistant.

Answer the user's question using ONLY the business information
provided below.

Do not invent or assume any numbers.

Business information:

{context}

User question:

{question}

Rules:

1. If the user asks about customers, use the Customers metric.
2. If the user asks about products, use the Products metric and
   the Products list.
3. If the user asks about sales, use the Sales metric.
4. If the user asks about revenue, use Total Revenue.
5. Answer directly and concisely.
6. Do not make up information.
7. If the requested information is unavailable, say so.

Return only the answer to the user's question.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        if response is None:
            return "I couldn't generate an answer."

        answer = getattr(response, "text", None)

        if not answer:
            return "I couldn't generate an answer."

        return answer.strip()

    except Exception as e:

        print("=" * 60)
        print("GEMINI ERROR")
        print(type(e).__name__)
        print(str(e))
        print("=" * 60)

        raise
