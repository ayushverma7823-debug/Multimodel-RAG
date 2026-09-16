def create_index_if_not_exists(client, index_name):
    if client.indices.exists(index=index_name):
        print(f"Index '{index_name}' already exists.")
        client.indices.delete(index=index_name)

    body = {
        "settings": {"index": {"knn": True}},
        "mappings": {
            "properties": {
                "content": {"type": "text"},
                "content_type": {"type": "keyword"},
                "filename": {"type": "keyword"},
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 768,
                    "method": {
                        "name": "hnsw",
                        "space_type": "cosinesimil",
                        "engine": "nmslib",
                    },
                },
            }
        },
    }

    try:
        client.indices.create(index=index_name, body=body)
        print(f"Index '{index_name}' created successfully.")
    except Exception as e:
        print(f"Error creating index '{index_name}': {e}")
        raise

def prepare_chunks_for_ingestion(chunks):
   from helper import get_embedding
   prepared_chunks=[]

   for idx, chunk in enumerate(chunks) :
        if not chunk.get("content"):
            print(f"Skipping chunk {idx} due to missing content.")
            continue


        # Generate embedding for the content
        chunk ["embedding"] = get_embedding(chunk["content"])

        # Prepare the chunk data
        chunk_data = {
            "content": chunk.get("content", ""),
            "content_type": chunk.get("content_type", "text"),
            "filename": chunk.get("filename", None),
            "embedding": chunk.get("embedding", None),
        }

        prepared_chunks. append (chunk_data)
        print(f"Prepared chunk {idx} for ingestion: {chunk_data}")

        return prepared_chunks

def ingest_chunks_into_opensearch(client, index_name, chunks):
    """
    Ingest prepared chunks into the specified OpenSearch index.
    """
    from opensearchpy import helpers

    actions = []
    for chunk in chunks:
        action = {
        "_index": index_name,
        "_source": chunk,
        }
    actions.append(action)

    try:
        helpers.bulk(client, actions)
        print(f"Ingested {len(actions)} chosks into index '{index_name}'.")
    except Exception as e:
        print(f"Error ingesting chunks into index '{index_name}': {e}")
        raise

def ingest_all_content_into_opensearch(processed_images,processed_tables,semantic_chunks,index_name):
    """
    Ingest all content into OpenSearch.
    """
    from helper import get_opensearch_client

    # Initialize OpenSearch client
    client = get_opensearch_client("localhost", 9200)

    # Create index if it does not exist
    create_index_if_not_exists(client, index_name)

    # Prepare and ingest images
    image_chunks = prepare_chunks_for_ingestion(processed_images)
    ingest_chunks_into_opensearch(client, index_name, image_chunks)

    # Prepare and ingest tables
    table_chunks = prepare_chunks_for_ingestion(processed_tables)
    ingest_chunks_into_opensearch(client, index_name, table_chunks)

    # Prepare and ingest semantic chunks
    semantic_chunks_data = prepare_chunks_for_ingestion(semantic_chunks)
    ingest_chunks_into_opensearch(client, index_name, semantic_chunks_data)

if __name__=="__main__":
    from unstructured.partition.pdf import partition_pdf
    from chunking import process_image_with_caption,process_table_with_caption,create_semantic_chunks

        # Example usage
    pdf_file_path = "files/2312.10997v5.pdf"
    raw_chunks = partition_pdf(
        filename=pdf_file_path,
        strategy="hi_res",
        infer_table_structure=True,
        extract_image_block_types=["Image", "Figure", "Table"],
        extract_image_block_to_payload=True,
        chunking_strategy=None,
    )

    processed_images = process_image_with_caption(raw_chunks, gemini=True)

    process_tables = process_table_with_caption(raw_chunks, gemini=True)


    text_chunks = partition_pdf(
        filename=pdf_file_path,
        strategy="hi_res",
        chunking_strategy="by_title",
        max_characters=2000,
        combine_text_under_n_chars=500,
        new_after_n_chars=1500
    )

    semantic_chunks=create_semantic_chunks(text_chunks)
    index_name="pdf_content_index"
    ingest_all_content_into_opensearch(processed_images,process_tables,semantic_chunks,index_name)

