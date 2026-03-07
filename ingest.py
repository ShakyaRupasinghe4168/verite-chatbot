import os
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

documents = []

for file in os.listdir("data"):

    if file.endswith(".pdf"):

        loader = PyPDFLoader(f"data/{file}")
        pages = loader.load()

        chunks = splitter.split_documents(pages)

        for chunk in chunks:

            documents.append({
                "text":chunk.page_content,
                "source":file,
                "page":chunk.metadata["page"]
            })

texts = [d["text"] for d in documents]

embeddings = model.encode(texts)

vectors = []

for i, emb in enumerate(embeddings):

    vectors.append({
        "id":str(i),
        "values":emb.tolist(),
        "metadata":documents[i]
    })

index.upsert(vectors)

print("Documents indexed successfully")