import chromadb    
from chromadb.config import Settings
client = chromadb.Client(settings=Settings(allow_reset=True))

def reset_chromadb():
    client.reset()

def insert_chunks_into_chromadb(doc_chunks, collection_name="my_documents"):
    collection = client.get_or_create_collection(name=collection_name)

    # It is necessary to insert in smaller batches to avoid Batch size exceeding ChromaDB's Max
    batch_size = 25
    for i in range(0, len(doc_chunks), batch_size):
        batch_chunks = doc_chunks[i:i + batch_size]
        # Assuming each chunk is a string and you want to store them with a simple ID
        # You might want to add more sophisticated metadata depending on your use case
        ids = [f"doc_chunk_{i + j}" for j in range(len(batch_chunks))]

        collection.add(
            documents=batch_chunks,
            ids=ids
        )
        # print(f"Inserted batch {i // batch_size + 1} into ChromaDB.")

    return collection