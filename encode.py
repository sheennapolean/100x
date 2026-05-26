import chromadb
from sentence_transformers import SentenceTransformer
import os

# -----------------------------
# CHROMADB SETUP
# -----------------------------
CHROMA_PATH = "chroma_db"

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="profile_data"
)

# -----------------------------
# EMBEDDING MODEL
# -----------------------------
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------
# LOAD ALL FILES
# -----------------------------
DATA_FOLDER = "data"

documents = []
metadatas = []
ids = []

counter = 0

for filename in os.listdir(DATA_FOLDER):

    filepath = os.path.join(DATA_FOLDER, filename)

    with open(filepath, "r", encoding="utf-8") as file:

        text = file.read()

        # Split into chunks
        chunks = text.split("\n\n")

        for chunk in chunks:

            if len(chunk.strip()) == 0:
                continue

            documents.append(chunk)

            metadatas.append({
                "source": filename
            })

            ids.append(f"id_{counter}")

            counter += 1

# -----------------------------
# GENERATE EMBEDDINGS
# -----------------------------
embeddings = model.encode(documents).tolist()

# -----------------------------
# STORE IN CHROMADB
# -----------------------------
collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

print(f"Added {len(documents)} chunks to ChromaDB")