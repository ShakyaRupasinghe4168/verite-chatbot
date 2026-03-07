# agent.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from tools import search_documents
from memory_store import load_memory, save_memory
from prompts import SYSTEM_PROMPT


load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-flash-latest")


memory = load_memory()

GREETINGS = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]

def agent_chat(user_message):
    """
    Main chat function for the Verité Research Assistant.
    Returns the assistant's answer and a list of sources.
    """
    global memory

    user_lower = user_message.lower().strip()


    if any(greet in user_lower for greet in GREETINGS):
        answer = "Hello! How can I help you understand Verité Research publications today?"
        memory.append({"role": "user", "content": user_message})
        memory.append({"role": "assistant", "content": answer})
        save_memory(memory)
        return answer, []  

    docs = search_documents(user_message)

    if not docs:
        answer = "Sorry, I can only answer questions related to Verité Research publications."
        memory.append({"role": "user", "content": user_message})
        memory.append({"role": "assistant", "content": answer})
        save_memory(memory)
        return answer, []

    context = ""
    sources = []

    for d in docs:
        context += f"""
Source: {d['source']}
Page: {d['page']}

{d['text']}
"""
        sources.append(f"{d['source']} - page {d['page']}") 

    prompt = f"""
{SYSTEM_PROMPT}

Conversation history:
{memory}

Context:
{context}

User:
{user_message}
"""

    try:
        response = model.generate_content(prompt)
        answer = response.text
    except Exception as e:
        answer = "Sorry, I am having trouble generating a response right now."
        print("Gemini API error:", e)

    memory.append({"role": "user", "content": user_message})
    memory.append({"role": "assistant", "content": answer})
    save_memory(memory)

    return answer, sources