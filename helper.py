def get_embedding(prompt,model="nomic-embed-text"):

    import requests
    url="http://localhost:11434/api/embeddings"
    data = {
        "model": model,
        "prompt": prompt
    }

    response = requests.post(url, json=data)
    response.raise_for_status()

    return response.json().get("embedding", None)

def get_opensearch_client(host,port):
    from opensearchpy import OpenSearch

    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_compress=True,
        timeout=30,
        max_retries=3,
        retry_on_timeout=True
    )

    return client

if __name__ == "__main__":
    # # Example usage
    # prompt = "Hello, world!"
    # embedding = get_embedding(prompt)
    # print("Embedding:", embedding)

    host = "localhost"
    port = 9200
    client = get_opensearch_client(host, port)
    print("OpenSearch client created:", client)
