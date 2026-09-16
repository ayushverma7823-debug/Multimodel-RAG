# Text Image Table
import os

from torch import chunk
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Tesseract-OCR"

def process_image_with_caption(raw_chunks,gemini=True):
    import base64
    import os
    import google.generativeai as genai
    from dotenv import load_dotenv
    from unstructured.documents.elements import Image, FigureCaption


    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)

    processed_images = []

    for idx, chunk in enumerate(raw_chunks):
        if isinstance(chunk, Image):
            # check idx+1 is figure caption
            if idx + 1 < len(raw_chunks) and isinstance(raw_chunks[idx + 1], FigureCaption):
                caption = raw_chunks[idx + 1].text
            else:
                caption = None

            image_data={
                "caption": caption if caption else "No caption found",
                "image_text":chunk.text,
                "image_base64": chunk.metadata.image_base64,
                "content": chunk.text,
                "content_type": "image",
                "filename": chunk.metadata.filename
            }
            if gemini:
                model=genai.GenerativeModel("gemini-3.1-flash-lite")
                image_binary = base64.b64decode(image_data["image_base64"])
                prompt =(
                f"Describe the image in detail. The caption is: {image_data['caption']}."
                f"The image text is: {image_data['image_text']}."
                f"Direct analyse the image and provide a detailed description without any additional commentary."
                )


                response = model.generate_content([
                    prompt,
                    {"mime_type": "image/png", "data": image_binary}
                ])
                image_data["content"]= response.text

            processed_images.append(image_data)

    return processed_images




def process_table_with_caption(raw_chunks,gemini=True,ollama=False):
    import os
    import requests
    import google.generativeai as genai
    from dotenv import load_dotenv
    from unstructured.documents.elements import Table, FigureCaption

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)

    processed_tables = []

    for idx, element in enumerate(raw_chunks):
        if isinstance(element, Table):
            # check idx+1 is figure caption
            if idx + 1 < len(raw_chunks) and isinstance(raw_chunks[idx + 1], FigureCaption):
                caption = raw_chunks[idx + 1].text
            else:
                caption = None

            table_data={
                "table_as_html": element.metadata.text_as_html,
                "table_text": element.text,
                "content": element.text,
                "content_type": "table",
                "filename": element.metadata.filename
            }
            if gemini:
                model=genai.GenerativeModel("gemini-3.1-flash-lite")
                prompt =(
                f"Analyse the following table and provied the detailed summary"
                f"including the key insights, trends, and any notable patterns."
                f"here is the table in HTML format: {table_data['table_as_html']}."
                f"Direct analyse the table and provide a detailed description without any additional commentary."
                )


                response = model.generate_content([
                    prompt,
                ])
                table_data["content"]= response.text
            elif ollama:
                    url = "http://localhost:11434/api/generate"
                    data = {
                        "model": "deepseek-r1:1.5b",
                        "prompt": (
                            "Analyze the following table and provide a detailed summary of its contents, "
                            "including the structure, key data points, and any notable trends or insights."
                            f"Here is the table in HTML format: {table_data['table_as_html']}"
                            "Directly analyze the table and provide a detailed summary without any additional text."
                        ),
                        "max_tokens": 1000,
                        "stream": False,
                        "temperature": 0.7,
                    }

                    response = requests.post(url, json=data)
                    response.raise_for_status()
                    table_data["content"]= response.json().get("response", "No response from model")
            processed_tables.append(table_data)

    return processed_tables

def create_semantic_chunks(text_chunks):
    from unstructured.documents.elements import  CompositeElement 
    prdocessed_chunks = []
    for idx,chunk in enumerate(text_chunks):
        if isinstance(chunk, CompositeElement):
            chunk_data={
                "content":chunk.text,
                "content_type":"text",
                "filename":chunk.metadata.filename if chunk.metadata else None
                }  
            prdocessed_chunks.append(chunk_data)

    return prdocessed_chunks

if __name__ == "__main__":
    from unstructured.partition.pdf import partition_pdf


    #example usage
    pdf_path = "files/2312.10997v5.pdf"
    raw_chunks = partition_pdf(
        filename=pdf_path,
        strategy="hi_res",
        infer_table_structure=True,
        extract_image_block_types=["Image","Table","Figure"],
        extract_image_block_to_payload=True,
        chunking_strategy=None,
)
    # processed_images = process_image_with_caption(raw_chunks,gemini=True)

    # for image in processed_images:
    #     print(image)

    processed_tables = process_table_with_caption(raw_chunks,gemini=True)
    for table in processed_tables:
        print(table)

    text_chunks= partition_pdf(
        filename=pdf_path,
        strategy="hi_res",
        chunking_strategy="by_title",
        max_characters=1000,
        combine_text_under_n_chars=500,
        new_after_n_chars=1500
    )

    semantic_chunks = create_semantic_chunks(text_chunks)
    for chunk in semantic_chunks:
        print(chunk)