import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path='db/')
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
collection = client.get_or_create_collection(name="pdf_docs", embedding_function=sentence_transformer_ef)

prompt = "Cuál es el minimo de creditos a matricular?"

results = collection.query(
        # Chroma will embed this for you
        query_texts=[prompt],
        n_results=1  # how many results to return
    )

print(results)