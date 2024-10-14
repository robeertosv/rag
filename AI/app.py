import chromadb
from chromadb.utils import embedding_functions
import pika
import sys
import os
import json

client = chromadb.PersistentClient(path='db/')
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
collection = client.get_or_create_collection(name="pdf_docs", embedding_function=sentence_transformer_ef)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='prompt')

def query(prompt):
    print("Recieved: " + prompt)
    results = collection.query(
        # Chroma will embed this for you
        query_texts=[prompt],
        n_results=1  # how many results to return
    )

    sendStatus({
        "text": results['documents'][0][0],
        "file": results['metadatas'][0][0]['file']
    })


def main():
    def callback(ch, method, properties, body):
        # Hacer print del mensaje
        prompt = body.decode('utf-8')
        query(prompt)

    channel.basic_consume(queue='message', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def sendStatus(response):
    channel.queue_declare(queue='result')
    response = json.dumps(response)
    channel.basic_publish(exchange='', routing_key='result', body=response, properties=pika.BasicProperties(
        content_type='application/json',  # Definir el tipo de contenido
        delivery_mode=2  # Hacer que el mensaje sea persistente
    ))
    print(" [x] Complete'")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
