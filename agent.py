import os
import re
from dotenv import load_dotenv
from google.genai import Client

from tools import search_documents
from memory_store import load_memory, save_memory
from prompts import SYSTEM_PROMPT

load_dotenv()

client = Client(api_key=os.getenv("GEMINI_API_KEY"))

memory = load_memory()


def extract_used_sources(answer, docs):
    """
    Return only sources that appear in the citation text.
    """
    used = []
    for d in docs:
        citation = f"{d['source']}:{d['page']}"
        if citation in answer:
            used.append(d)

    return used


def agent_chat(user_message):

    global memory

    # -------------------------
    # MEMORY CHECK
    # -------------------------

    if memory:

        recent = memory[-6:]
        history = "\n".join(
            [f"{m['role']}: {m['content']}" for m in recent]
        )

        memory_prompt = f"""
{SYSTEM_PROMPT}

Conversation history:
{history}

User question:
{user_message}

Instructions:
If the answer exists in the conversation history, answer normally.

If it cannot be answered from the conversation history reply ONLY with:
VECTOR_SEARCH
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=memory_prompt
        )

        answer = response.text.strip()

        if "VECTOR_SEARCH" not in answer:

            memory.append({"role": "user", "content": user_message})
            memory.append({"role": "assistant", "content": answer})

            save_memory(memory)

            return answer, []

    # -------------------------
    # VECTOR SEARCH
    # -------------------------

    docs = search_documents(user_message)

    if not docs:

        refusal = (
            "I'm Verity, an assistant for Verité Research publications. "
            "I can only answer questions based on those publications."
        )

        memory.append({"role": "user", "content": user_message})
        memory.append({"role": "assistant", "content": refusal})

        save_memory(memory)

        return refusal, []

    # Build context

    context = ""
    for d in docs:

        context += f"""
SOURCE: {d['source']}:{d['page']}

{d['text']}
"""

    rag_prompt = f"""
{SYSTEM_PROMPT}

Answer the question using ONLY the context below.

Context:
{context}

User question:
{user_message}

Instructions:
• Cite sources like (source:page)
• Do not invent sources
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=rag_prompt
    )

    answer = response.text.strip()

    used_sources = extract_used_sources(answer, docs)

    memory.append({"role": "user", "content": user_message})
    memory.append({"role": "assistant", "content": answer})

    save_memory(memory)

    return answer, used_sources