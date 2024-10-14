import chromadb
from chromadb.utils import embedding_functions
import uuid
import json


def main():
    print('Iniciando...')
    path = 'D:/Proyectos/rag/AI/results/vault.json'
    print('Iniciando 1...')
    chroma_client = chromadb.PersistentClient(path='db/')
    print('Iniciando 2...')
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
    print('Iniciando 3...')
    chroma_collection = chroma_client.get_or_create_collection(name="pdf_docs", embedding_function=sentence_transformer_ef)
    print('Iniciado!')
    data = []
    
    documents = []
    metadatas = []
    ids = []
    
    print("Cargando el json...")
    
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)       
        file.close() 
    
    print('JSON cargado correctamente')
    
    for doc in data:
        documents.append(doc['chunk'])
        metadatas.append({"file": doc['file']})
        ids.append(str(uuid.uuid1()))
    
    print("Cargando en chormadb")
    
    chroma_collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
        
    print("Cargado!")
    
main()