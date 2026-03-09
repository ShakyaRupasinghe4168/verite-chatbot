# Verity — Verité Research Assistant

## Overview

Verity is an AI chatbot designed to provide information from Verité Research publications.
It uses vector search and conversation memory to answer questions with citations.

- Live URL : https://huggingface.co/spaces/shakyarupasinghe/verite-chatbot 
- Used Documents details & Sample questions and answers: https://drive.google.com/file/d/1QX_9hjimD8Beb0tzq1lMRgOH847YnaJT/view?usp=sharing
---

## Features

- Chat UI with user and assistant messages.
- Inline source citations `(document_name:page)` and expandable source display.
- Hybrid search (vector + keyword) for document retrieval.
- Persistent conversation memory across sessions.
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

### Notes About Free Tier Usage

#### Hugging Face Spaces (Free Tier)

* The application is deployed on the free tier of Hugging Face Spaces.  
* Free Spaces may automatically sleep after approximately **1 hour of inactivity**.  
* While the Space is active, `memory/chat_memory.json` persists, allowing conversation memory across multiple sessions during that period.
* If the Space sleeps, rebuilds, or restarts, the local memory file may reset.   

#### Gemini API (Free Tier)

* The chatbot uses the **Google Gemini API** free tier for generating responses.  
* The free tier provides a **limited number of requests per day**.  
* If the quota is exceeded, the application may temporarily stop responding until the daily quota resets.  
* 
* The system currently stores the **last 20 messages** for conversation memory. This limit is configurable and set to 20 for this demo deployment.  As number of messages sent will increase token usage. 

**Note:**  
These limitations (sleep behavior, request limits, and memory size) are related to free-tier hosting and API usage. They are configured this way for demonstration purposes, and the system architecture can support higher limits in a production deployment.
