# Verity — Verité Research Assistant

## Overview

Verity is an AI chatbot designed to provide information from Verité Research publications.
It uses vector search and conversation memory to answer questions with citations.

---

## Features

- Chat UI with user and assistant messages.
- Inline source citations `(document_name:page)` and expandable source display.
- Hybrid search (vector + keyword) for document retrieval.
- Session memory stored persistently (last 20 messages).
- Small talk handling (greetings, thanks, etc.).
- Clear Chat (UI only) and Clear Permanently (deletes memory).
- Out-of-scope question handling (polite refusal).

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repo_url>
cd verite-chatbot
```

### 2. Create virtual environment

```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory with your API keys:

```env
GEMINI_API_KEY=<your_google_gemini_api_key>
PINECONE_API_KEY=<your_pinecone_api_key>
PINECONE_INDEX=<your_pinecone_index_name>
```

### 5. Prepare data

- Place up to 5 Verité PDFs in the `data/` folder.
- Run the indexing script to embed documents into the vector database.

### 6. Run the app

```bash
streamlit run app.py
```

- Input your question in the chat box.
- Hover over buttons to see tooltips:
  - **Clear Chat:** Clears chat UI only.
  - **Clear Permanently:** Clears UI and deletes memory file.

## 7. Notes About Free Tier Usage

- **Hugging Face Spaces Free Tier**
  - The app is deployed on the Hugging Face free tier.
  - Free Spaces **sleep after ~1 hour of inactivity**.
  - While the Space is active, `memory/chat_memory.json` persists and remembers your chat.
  - If the Space sleeps, is rebuilt, or restarted, all local memory will reset.
  - For quick demo or short-term testing, memory persists within the active session.

- **Gemini API Free Tier**
  - The project uses the free tier of Google Gemini API.
  - Free tier has a limited number of chat requests per day.
  - Users should be aware that excessive questions may hit the usage limit, after which responses will fail until the quota resets.
