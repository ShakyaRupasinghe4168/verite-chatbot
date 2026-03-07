import os
from dotenv import load_dotenv
load_dotenv()
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

def search_documents(query):

    embedding = model.encode(query).tolist()

    results = index.query(
        vector=embedding,
        top_k=5,
        include_metadata=True
    )

    docs = []

    for match in results["matches"]:
        docs.append(match["metadata"])

    return docs