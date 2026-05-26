
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

# load_dotenv()



class ChatRequest(BaseModel):
    message: str


# -----------------------------
# GROQ CLIENT
# -----------------------------
client = OpenAI(
    # api_key=os.environ.get("API_KEY"),
    api_key=st.secrets["API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

# -----------------------------
# CHROMADB
# -----------------------------
CHROMA_PATH = "chroma_db"

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = chroma_client.get_or_create_collection(
    name="profile_data"
)

# -----------------------------
# BASE SYSTEM PROMPT
# -----------------------------
BASE_SYSTEM_PROMPT = """
You are Sheen Napolean, a Machine Learning Engineer with 4+ years of experience.

You are answering interview questions naturally like a real candidate.

COMMUNICATION STYLE:
- Speak professionally and confidently.
- Keep responses concise and conversational.
- Use first-person responses like:
  "I worked on..."
  "I implemented..."
  "I designed..."
- Never say you are an AI assistant.

ANSWERING RULES:
- Use the retrieved resume context while answering.
- Explain concepts clearly with practical examples.
- Focus on impact, scalability, optimization, and business value.
- Do not invent fake experience.
- If you don't know something, explain your approach honestly.

TECHNICAL AREAS:
- Machine Learning
- Deep Learning
- NLP & LLMs
- RAG Applications
- TensorFlow
- PyTorch
- FastAPI
- AWS SageMaker
- Docker & Kubernetes
- Apache Spark
- SQL & ETL pipelines
"""

# -----------------------------
# CHAT FUNCTION
# -----------------------------
def chat(user_message):

    # Retrieve relevant resume/project context
    results = collection.query(
        query_texts=[user_message],
        n_results=4
    )
    print(results)
    documents = results["documents"][0]

    # Format context nicely
    context = "\n\n".join([
        f"Context {i+1}:\n{doc}"
        for i, doc in enumerate(documents)
    ])

    # Dynamic system prompt
    SYSTEM_PROMPT = f"""
{BASE_SYSTEM_PROMPT}

========================================
RELEVANT CONTEXT
========================================

{context}

========================================
INSTRUCTIONS
========================================

Use the context above to answer naturally.

- Combine multiple context pieces if needed.
- Do not copy the context directly.
- Sound like a real interview candidate.
"""

    # LLM Call
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        temperature=0.7,
        max_tokens=500,
    )

    reply = completion.choices[0].message.content

    return {
        "reply": reply
    }

