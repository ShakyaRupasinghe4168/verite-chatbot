# agent.py
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
from tools import search_documents
from memory_store import load_memory, save_memory
from prompts import SYSTEM_PROMPT

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemma-3-12b-it")

memory = load_memory()

GREETINGS = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
SMALL_TALK = ["how are you", "what’s up", "how’s it going"]

def extract_sources_from_text(text):
    """
    Extract sources from memory-based answers.
    Expects format like: (data\filename.pdf, page 11)
    """
    matches = re.findall(r"\(data\\(.*?\.pdf), page (\d+)\)", text)
    return [{"source": m[0], "page": m[1], "text": ""} for m in matches]

def agent_chat(user_message):
    """
    Main chat function for Verité Research Assistant (Verity).
    Returns the assistant's answer and a list of sources with chunk text.
    """
    global memory
    user_lower = user_message.lower().strip()

    # 1️⃣ Handle greetings and small talk
    if any(phrase in user_lower for phrase in GREETINGS + SMALL_TALK):
        answer = "Hello! I'm Verity, your assistant for Verité Research publications. How can I help you today?"
        memory.append({"role": "user", "content": user_message})
        memory.append({"role": "assistant", "content": answer})
        save_memory(memory)
        return answer, []

    # 2️⃣ Attempt to answer from memory first
    prompt_memory_only = f"""
{SYSTEM_PROMPT}

Conversation history:
{memory}

User:
{user_message}

Instructions: Answer only based on the conversation history above. 
If you cannot answer from memory alone, respond exactly with: 'I need to check documents.'
"""
    try:
        response = model.generate_content(prompt_memory_only)
        answer = response.text.strip()
    except Exception as e:
        answer = "Sorry, I am having trouble generating a response right now."
        print("Gemini API error:", e)
        memory.append({"role": "user", "content": user_message})
        memory.append({"role": "assistant", "content": answer})
        save_memory(memory)
        return answer, []

    sources = []

    # 3️⃣ Memory-only answer: extract sources only if content-related
    if "I need to check documents" not in answer:
        # Only extract sources if it is not an out-of-scope refusal
        if ("only here to help" not in answer.lower()) and ("do not contain any information" not in answer.lower()):
            sources = extract_sources_from_text(answer)
        else:
            sources = []  # polite refusal → no sources

    # 4️⃣ Vector search only if memory cannot answer
    if "I need to check documents" in answer:
        docs = search_documents(user_message)
        if not docs:
            # Out-of-scope → polite refusal, no sources
            answer = "I'm Verity, and I’m only here to help with Verité Research publications. I’m sorry I can’t answer that question."
            sources = []
        else:
            # Build context from retrieved documents
            context = ""
            for d in docs:
                context += f"""
Source: {d['source']}
Page: {d['page']}

{d['text']}
"""
                sources.append({
                    "source": d['source'],
                    "page": d['page'],
                    "text": d['text']
                })

            # Generate final answer using retrieved context
            prompt_with_docs = f"""
{SYSTEM_PROMPT}

Conversation history:
{memory}

Context:
{context}

User:
{user_message}

Instructions: When answering, always cite the source PDF and page number in your response.
"""
            try:
                response = model.generate_content(prompt_with_docs)
                answer = response.text
            except Exception as e:
                answer = "Sorry, I am having trouble generating a response right now. Your free quota is ended, try after 24 hours" \
                "."
                print("Gemini API error:", e)

    # 5️⃣ Save conversation to memory
    memory.append({"role": "user", "content": user_message})
    memory.append({"role": "assistant", "content": answer})
    save_memory(memory)

    return answer, sources