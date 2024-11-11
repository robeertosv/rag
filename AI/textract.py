import pymupdf
import os
import re
import json
from bertopic import BERTopic

path = "D:/Proyectos/rag/AI/docs" # As needed

# lists all files in ./docs
def getAllFiles(path=path):    
    folder = path
    files = os.listdir(folder)
    return files

# Extracts text from PDF and stores it on ./results
def textract():
    files = getAllFiles()
       
    for file in files:
        doc = pymupdf.open(path + '/' + file) # open a document
        text = ''
        for page in doc: # iterate the document pages
            text += page.get_text()
        
        text = re.sub(r'\s+', ' ', text).strip()
        #generate_chunks(file, text)
        thematic_chunking(file, text)

def generate_chunks(file, text):
    sentences = re.split(r'(?<=[.!?]) +', text)  # split on spaces following sentence-ending punctuation
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        # Check if the current sentence plus the current chunk exceeds the limit
        if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
            current_chunk += (sentence + " ").strip()
        else:
            # When the chunk exceeds 1000 characters, store it and start a new one
            chunks.append(current_chunk)
            current_chunk = sentence + " "
            
    if current_chunk:  # Don't forget the last chunk!
        chunks.append(current_chunk)
    
    save_file(file, chunks)


def thematic_chunking(file, text):
    topic_model = BERTopic(language="spanish")
    topics, _ = topic_model.fit_transform(text.split(". "))
    chunks = []
    current_chunk = ""
    current_topic = topics[0]

    for i, topic in enumerate(topics):
        # Dividir si cambia el tema
        if topic != current_topic:
            chunks.append(current_chunk.strip())
            current_chunk = ""
            current_topic = topic
        current_chunk += " " + text.split(". ")[i]
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    save_file(file, chunks)
    
def save_file(file, chunks):
    name = 'results/vault.json'
    data = []
    for chunk in chunks:
        data.append({
            "chunk": chunk,
            "file": file
        })
    
    with open(name, 'a', encoding='utf-8') as vault_file:
        json.dump(data, vault_file, ensure_ascii=False)
        vault_file.close()

textract()