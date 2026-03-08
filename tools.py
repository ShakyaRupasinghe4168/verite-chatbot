import os
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

model = SentenceTransformer("all-MiniLM-L6-v2")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

# Load all documents locally for keyword search
# This assumes your `documents` list is the same as in the indexing step
# If not, you can load from Pinecone metadata or a local JSON/Pickle
try:
    import json
    with open("documents.json", "r", encoding="utf-8") as f:
        documents = json.load(f)
except:
    documents = []  # fallback if not saved locally


def search_documents(query, top_k=6, score_threshold=0.5, keyword_weight=0.3):
    """
    Hybrid search: vector + keyword.
    - top_k: number of vector search results to return
    - score_threshold: minimum vector similarity
    - keyword_weight: additional score for keyword match (0-1)
    """

    # --------------------------
    # VECTOR SEARCH
    # --------------------------
    vector = model.encode(query).tolist()
    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )

    vector_docs = []
    for match in results["matches"]:
        score = match["score"]
        meta = match["metadata"]
        text = meta.get("text", "").strip()
        if score < score_threshold or len(text) < 50:
            continue
        vector_docs.append({
            "source": meta.get("source"),
            "page": meta.get("page"),
            "text": text,
            "score": score
        })

    # --------------------------
    # KEYWORD SEARCH
    # --------------------------
    query_words = set(query.lower().split())
    keyword_docs = []
    for d in documents:
        text_words = set(d["text"].lower().split())
        common_words = query_words.intersection(text_words)
        if common_words:
            # simple score proportional to fraction of words matched
            score = len(common_words) / len(query_words) * keyword_weight
            keyword_docs.append({
                "source": d["source"],
                "page": d["page"],
                "text": d["text"],
                "score": score
            })

    # --------------------------
    # COMBINE AND SORT
    # --------------------------
    combined = { (d['source'], d['page']): d for d in vector_docs }  # vector docs first
    for kd in keyword_docs:
        key = (kd['source'], kd['page'])
        if key in combined:
            combined[key]['score'] += kd['score']  # boost vector doc if keyword also present
        else:
            combined[key] = kd

    # Sort by score descending and take top_k
    final_docs = sorted(combined.values(), key=lambda x: x['score'], reverse=True)[:top_k]

    # Remove score before returning
    for d in final_docs:
        d.pop("score", None)

    return final_docs