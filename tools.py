import os
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

model = SentenceTransformer("all-MiniLM-L6-v2")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index(os.getenv("PINECONE_INDEX"))


def search_documents(query, top_k=6, score_threshold=0.75):

    vector = model.encode(query).tolist()

    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )

    docs = []

    for match in results["matches"]:

        score = match["score"]
        meta = match["metadata"]
        text = meta.get("text", "").strip()

        if score < score_threshold:
            continue

        if len(text) < 100:
            continue

        docs.append({
            "source": meta.get("source"),
            "page": meta.get("page"),
            "text": text
        })

    return docs