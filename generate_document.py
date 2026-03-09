import os
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


pdf_folder = "data" 

output_file = "documents.json"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

documents = []

for file_name in os.listdir(pdf_folder):
    if file_name.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(pdf_folder, file_name))
        pages = loader.load()
        chunks = splitter.split_documents(pages)

        for chunk in chunks:
            documents.append({
                "text": chunk.page_content,
                "source": file_name,
                "page": chunk.metadata["page"]
            })

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=2, ensure_ascii=False)

print(f"Generated {len(documents)} document chunks in {output_file}")