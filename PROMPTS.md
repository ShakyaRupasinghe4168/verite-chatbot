# Verity — System Prompt Design and Decisions

## 1. System Prompt Design

The system prompt defines the persona and behavior of Verity, the AI assistant:

- **Persona:**
  - Professional, knowledgeable AI representing Verité Research.
  - Provides clear, concise, and accurate responses based solely on Verité publications.

- **Scope Rules:**
  - Only answer questions related to Verité Research content.
  - Politely refuse out-of-scope questions (e.g., general knowledge or unrelated topics).

- **Answering Style:**
  - Include inline citations `(document_name:page)` when referencing retrieved content.
  - If the answer comes from conversation memory, citations are inline only.
  - Never invent answers or sources.

- **Memory Handling:**
  - The agent remembers the last 20 messages across sessions (persistent memory file).
  - Only uses vector search if the answer cannot be found in memory.

---

## 2. Handling Borderline Questions

Some questions are general terms but relevant to Verité's work.

**Example:** "What is forced labour?"

- **Challenge:** There is no single "correct" answer; the term is general but relevant to the publications.
- **Design Choice:**
  1. The agent first checks conversation memory for prior mentions.
  2. If memory does not provide an answer, the agent performs hybrid search (vector + keyword) across the ingested documents.
  3. Only responds if retrieved content provides direct, verifiable information.
  4. If no clear answer exists, the agent politely explains the limitation.

**Example Interaction:**

> **User:** What is forced labour?
>
> **Agent:** I apologize, but the retrieved documents discuss the Forced Labour Convention, 1930 (No. 29) and its Protocol of 2014, noting that the "illegal exaction of forced or compulsory labour should be punishable as a penal offence" `(fair_recruitment_migrant_workers.pdf:28)`. However, a specific definition of forced labour is not provided in the given context.

- **Rationale:**
  - Ensures answers are accurate and verifiable.
  - Prevents providing misleading or out-of-scope information.
  - Hybrid search improves retrieval relevance for such borderline or partially matching queries.

---

## 3. Small Talk and Greetings

- The agent responds naturally to greetings like "Hi", "Hello", "How are you?", "Thanks", "Bye".
- No vector search is triggered for small talk.
- Responses are friendly and concise, keeping the focus on Verité Research content.

---

## 4. Memory vs. Hybrid Search

- **Memory-first logic:** Check recent conversation history before searching documents.
- **Hybrid search (vector + keyword):** Triggered if memory does not contain the answer.
  - Retrieves top-k document chunks with source citations.
  - Balances semantic relevance (vector) with precise keyword matching.

---

## 5. Source Citation

- All retrieved information includes inline citations `(document_name:page)`.
- Sources are displayed in the UI under expandable sections.
- If the answer comes from memory, inline citations are included directly in the text.

---

## 6. Out-of-Scope Questions

- Politely decline unrelated questions.

**Example Interaction:**

> **User:** Who is Virat Kohli?
>
> **Agent:** I'm only here to provide information from Verité Research publications. I cannot answer this question.

---

## 7. Memory Management

- **Clear Chat button:** Clears messages from the UI only. Memory remains on disk.
- **Clear Permanently button:** Clears UI and deletes the persistent memory file, starting a fresh session.

---

## 8. Design Summary

- Accurate and verifiable answers only.
- Proper handling of borderline questions with hybrid search.
- Friendly, professional interaction.
- Transparent source citation.
- Safe handling of out-of-scope questions.
