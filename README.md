# LocalRAG Q&A System

> A production-style Retrieval-Augmented Generation (RAG) application
> for asking questions over indexed research documents and generating
> grounded answers with either Google Gemini or a local Ollama model.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/UI-Gradio-orange?logo=gradio&logoColor=white)](https://www.gradio.app/)
[![RAG](https://img.shields.io/badge/Architecture-RAG-purple)](#-system-architecture)
[![LLM](https://img.shields.io/badge/LLM-Gemini%20%7C%20Ollama-green)](#-supported-ai-models)

## 📸 Screenshots

### LocalRAG Q&A System

<p align="center">
  <img src="./Screenshot%20%28496%29.png" alt="LocalRAG Q&A System" width="900">
</p>

### Application Interface

<p align="center">
  <img src="./Screenshot%20%28497%29.png" alt="LocalRAG Application Interface" width="900">
</p>
## 📌 Overview

**LocalRAG Q&A System** is an end-to-end Retrieval-Augmented Generation
application designed to answer questions from a document collection
instead of relying only on an LLM's pre-trained knowledge

The system combines:

-   Document parsing and preprocessing
-   Intelligent chunking
-   Search/index ingestion
-   Keyword retrieval
-   Semantic retrieval using embeddings
-   Hybrid retrieval
-   LLM-based answer generation
-   Optional streaming responses
-   A simple Gradio web interface
-   Support for both cloud-based Gemini and locally hosted Ollama models

The main goal is to provide answers that are **grounded in retrieved
document context**, while giving the user control over the retrieval
strategy and generation model.

------------------------------------------------------------------------

## ✨ Key Features

### 🔎 Multiple Retrieval Strategies

  -----------------------------------------------------------------------
  Method                              Description
  ----------------------------------- -----------------------------------
  **Keyword**                         Traditional lexical/text-based
                                      retrieval using matching terms

  **Semantic**                        Finds conceptually similar content
                                      using embeddings

  **Hybrid**                          Combines keyword and semantic
                                      retrieval for broader coverage
  -----------------------------------------------------------------------

### 🤖 Multiple AI Models

The interface supports two generation paths:

-   **Google Gemini** --- cloud-based LLM requiring an API key
-   **Ollama** --- locally running LLMs for a more private/local
    workflow

### ⚡ Streaming Generation

The application can stream generated text so users can see the answer as
it is being produced rather than waiting for the complete response.

### 📄 RAG Document Pipeline

The project separates the RAG workflow into logical stages:

``` text
Documents
   ↓
Parsing
   ↓
Cleaning / Preprocessing
   ↓
Chunking
   ↓
Embedding / Indexing
   ↓
Retrieval
   ↓
Context Construction
   ↓
LLM Generation
   ↓
Final Answer
```

### 🖥️ Interactive UI

The Gradio interface provides:

-   Question input
-   Answer display
-   Retrieval-method selection
-   AI-model selection
-   Streaming-response toggle
-   Example questions
-   Usage instructions

------------------------------------------------------------------------

# 🚀 Quick Start

This section takes you from a fresh clone of the project to a running **LocalRAG Q&A System**.

The setup follows the complete pipeline:

```text
Environment Setup
       ↓
Ollama + Local Models
       ↓
OpenSearch
       ↓
Environment Variables
       ↓
Chunk Ingestion
       ↓
Gradio Application
       ↓
LocalRAG Q&A
```

## 1. Clone the Repository

Clone the project and move into the project directory.

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd PDF-Parsing
```

---

## 2. Create a Virtual Environment

Create an isolated Python environment for the project.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

> **Why use a virtual environment?**  
> It keeps the project's Python packages isolated from other Python projects on your machine.

---

## 3. Install Dependencies

Install all required Python packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

After installation, the environment contains the libraries required for parsing, retrieval, embeddings, generation and the Gradio interface.

---

## 4. Install and Start Ollama as a Docker Container

This project can use Ollama as the local LLM runtime.

Start Ollama in a Docker container:

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

This command:

- Creates an Ollama container
- Exposes Ollama on port `11434`
- Persists downloaded models using the `ollama` Docker volume
- Makes the local Ollama API available to the application

You can verify the container with:

```bash
docker ps
```

---

## 5. Pull the Required Models

Download the models used by the local RAG pipeline.

### Local LLM

```bash
docker exec -it ollama ollama run deepseek-r1:1.5b          
```

### Embedding Model

```bash
docker exec -it ollama ollama run nomic-embed-text # For embeddings
```

The two models serve different purposes:

| Model | Purpose |
|---|---|
| `deepseek-r1:1.5b` | Local answer generation |
| `nomic-embed-text` | Text embeddings for semantic retrieval |

> **Note:** The first model download can take some time depending on your internet connection.

---

## 6. Start OpenSearch

Start the OpenSearch service configured by the project:

```bash
docker compose -f docker-compose.yml
```

The RAG retrieval layer uses OpenSearch for indexing and searching document chunks.

Make sure the OpenSearch instance is available at:

```text
localhost:9200
```

If your OpenSearch service uses a different host or port, update the corresponding connection settings in the project configuration.

You can also check the Docker containers with:

```bash
docker ps
```

---

## 7. Create the `.env` File

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=
```

For example:

```env
GEMINI_API_KEY=your_api_key_here
```

The Gemini key is used when the **Gemini** option is selected in the application.

### 🔐 Security

Do not commit your `.env` file to GitHub.

Add it to `.gitignore`:

```gitignore
.env
```

---

## 8. Ingest the Chunks

Once the document chunks have been generated and your search backend is running, execute the ingestion script:

```bash
python ingestion.py
```

This stage loads the processed chunks into the configured search/indexing system.

Conceptually:

```text
Processed Chunks
      ↓
   ingestion.py
      ↓
   OpenSearch
      ↓
Searchable Knowledge Base
```

Before starting the application, make sure ingestion completes successfully.

---

## 9. Run the Application

Start the Gradio application:

```bash
python app.py
```

The terminal will display the local application address.

Open the displayed URL in your browser, typically:

```text
http://127.0.0.1:7860
```

You can then:

1. Enter a question.
2. Select **Keyword**, **Semantic**, or **Hybrid** retrieval.
3. Select **Gemini** or **Ollama**.
4. Enable or disable **Stream Response**.
5. Click **Generate Answer**.

---

## ⚡ Quick Command Reference

For convenience, the core setup commands are:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama run deepseek-r1:1.5b          
docker exec -it ollama ollama run nomic-embed-text # For embeddings
docker compose -f docker-compose.yml
python ingestion.py
python app.py
```

> On Windows, use `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

---

## 🔍 Quick Verification Checklist

Before using the application, verify:

- [ ] Virtual environment is activated
- [ ] `requirements.txt` dependencies are installed
- [ ] Docker Desktop is running
- [ ] Ollama container is running
- [ ] `deepseek-r1:1.5b` is available
- [ ] `nomic-embed-text` is available
- [ ] OpenSearch is running on `localhost:9200`
- [ ] `.env` contains the required Gemini API key
- [ ] `python ingestion.py` completed successfully
- [ ] `python app.py` starts without errors


# 🏗️ System Architecture

``` text
                    ┌──────────────────────┐
                    │     Source PDFs      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Document Parsing    │
                    │  Text / Tables /     │
                    │  Images / Captions   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Chunking & Cleanup │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Embedding / Indexing │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
          ┌──────────┐   ┌───────────┐   ┌──────────┐
          │ Keyword  │   │ Semantic  │   │  Hybrid  │
          │ Retrieval│   │ Retrieval │   │ Retrieval│
          └────┬─────┘   └─────┬─────┘   └────┬─────┘
               │               │              │
               └───────────────┼──────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Retrieved Context    │
                    │ + User Question      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   LLM Generation     │
                    │ Gemini / Ollama      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Final Answer      │
                    └──────────────────────┘
```

------------------------------------------------------------------------

# 🔄 RAG Workflow

## 1. Document Parsing

Documents are processed before entering the retrieval system.

The parsing stage is designed to preserve useful document information
such as:

-   Normal text
-   Tables
-   Images
-   Figure information
-   Captions
-   Page-level metadata

This is important for research papers and other PDFs where relevant
information may not exist as plain paragraphs.

## 2. Chunking

Large documents are divided into smaller, retrieval-friendly pieces.

Chunking improves retrieval because the search system can return a
focused section instead of an entire document.

A good chunk should contain enough surrounding context to preserve
meaning while remaining small enough for efficient retrieval.

## 3. Ingestion

The processed chunks are converted into searchable records and ingested
into the configured search/indexing layer.

Typical metadata can include:

``` text
content
content_type
page_number
document/source information
chunk information
```

Keeping metadata with every chunk makes retrieval easier to debug and
allows the application to preserve document context.

## 4. Retrieval

When the user submits a question, the system retrieves relevant chunks.

### Keyword Retrieval

Keyword search focuses on terms appearing in the query and indexed
content.

Useful when the question contains:

-   Exact terminology
-   Names
-   Acronyms
-   Technical keywords

### Semantic Retrieval

Semantic search uses embeddings to identify content with similar meaning
even when the exact words are different.

Useful for natural-language questions and concept-based retrieval.

### Hybrid Retrieval

Hybrid search combines lexical and semantic signals.

Conceptually:

``` text
Query
 ├── Keyword Search ──┐
 │                    ├── Combine / Rank
 └── Semantic Search ─┘
             │
             ▼
      Relevant Chunks
```

## 5. Context Construction

The retrieved chunks are assembled into a context that is passed to the
generation layer along with the user's question.

The LLM is instructed to use the retrieved information as the primary
source for the answer.

## 6. Answer Generation

The generation layer can use:

-   **Gemini** for cloud-based generation
-   **Ollama** for local generation

The final response is generated from the retrieved context rather than
treating the LLM as the only source of information.

------------------------------------------------------------------------

# 🤖 Supported AI Models

## Google Gemini

Gemini can be used as the cloud generation provider.

Set the API key in your environment configuration:

``` env
GEMINI_API_KEY=your_api_key_here
```

Do **not** commit your `.env` file or API keys to GitHub.

## Ollama

Ollama allows the generation model to run locally.

Example setup:

``` bash
ollama pull <your-model>
ollama serve
```

The exact model can be selected according to your available CPU/GPU/RAM
resources.

For a local RAG workflow, Ollama can be useful when you want the
generation step to remain on your machine.

------------------------------------------------------------------------

# 🖥️ User Interface

The application provides a clean interface with four main controls.

### Your Question

Enter a question about the indexed RAG documents.

Example:

``` text
How does RAG work?
```

### Search Method

Choose one:

-   `keyword`
-   `semantic`
-   `hybrid`

### AI Model

Choose:

-   `gemini`
-   `ollama`

### Stream Response

Enable streaming to display generated content progressively.

------------------------------------------------------------------------

# 🚀 Getting Started

## Prerequisites

Install the following before running the project:

-   Python 3.10+
-   Git
-   A supported search/indexing service used by the project
-   Optional: Ollama
-   Optional: Docker Desktop if your indexing/search service is
    containerized

> The exact Python version and backend configuration should match the
> versions pinned in `requirements.txt` and `docker-compose.yml`.

------------------------------------------------------------------------

## 1. Clone the Repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd PDF-Parsing
```

## 2. Create a Virtual Environment

### Windows

``` powershell
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

``` env
GEMINI_API_KEY=your_api_key_here
```

Add any additional backend/model variables required by your local
configuration.

### Security

Never commit secrets:

``` gitignore
.env
.venv/
__pycache__/
*.pyc
```

------------------------------------------------------------------------

# 🐳 Docker / Search Backend

If the project is configured to use the included Docker Compose service,
start Docker Desktop and run:

``` bash
docker compose -f docker-compose.yml up -d
```

Check running containers:

``` bash
docker ps
```

To stop the services:

``` bash
docker compose -f docker-compose.yml down
```

If Docker is not installed or the Docker CLI is unavailable, install
Docker Desktop and make sure the Docker engine is running before
executing the commands above.

------------------------------------------------------------------------

# 📥 Data Preparation

Place source PDF documents in the project's configured input directory.

A typical workflow is:

``` text
PDF Files
   ↓
Parsing
   ↓
Extracted Elements
   ↓
Chunking
   ↓
Embedding
   ↓
Index
```

Before ingestion, verify that:

-   Text is extracted correctly
-   Tables are preserved
-   Images/figures are handled appropriately
-   Page metadata is retained
-   Empty or duplicate chunks are removed where appropriate

------------------------------------------------------------------------

# ▶️ Running the Application

After completing the setup:

``` bash
python app.py
```

The application starts the Gradio interface.

Open the local URL displayed in the terminal, typically similar to:

``` text
http://127.0.0.1:7860
```

------------------------------------------------------------------------

# 🧪 Example Questions

The interface includes example questions such as:

``` text
How does RAG work?
```

``` text
What are the benefits of RAG compared to fine-tuning?
```

``` text
Explain RAG architecture with diagrams.
```

``` text
What are common challenges in RAG implementations?
```

These examples demonstrate how different retrieval methods and
generation models can be tested against the indexed knowledge base.

------------------------------------------------------------------------

# 📁 Project Structure

``` text
PDF-Parsing/
│
├── .venv/                  # Python virtual environment
├── files/                  # Input / processed document files
├── figures/                # Figures and visual assets
├── pages/                  # Page-level or extracted page data
│
├── app.py                  # Gradio application / user interface
├── chunking.py             # Document chunking logic
├── ingestion.py            # Data ingestion and indexing
├── retrieval.py            # Keyword, semantic and hybrid retrieval
├── generation.py           # LLM response generation
├── genai.py                # Gemini / AI model integration
├── helper.py               # Shared helper utilities
│
├── docker-compose.yml      # Containerized backend configuration
├── requirements.txt        # Python dependencies
├── .env                    # Local environment variables (do not commit)
└── README.md               # Project documentation
```

------------------------------------------------------------------------

# 🧩 Module Responsibilities

  -----------------------------------------------------------------------
  File                                Responsibility
  ----------------------------------- -----------------------------------
  `app.py`                            Gradio UI and application entry
                                      point

  `chunking.py`                       Splits parsed content into
                                      retrieval-friendly chunks

  `ingestion.py`                      Loads processed content into the
                                      search/indexing layer

  `retrieval.py`                      Implements keyword, semantic and
                                      hybrid retrieval

  `generation.py`                     Builds context and generates final
                                      responses

  `genai.py`                          Handles Gemini/AI model integration

  `helper.py`                         Utility and shared helper functions

  `docker-compose.yml`                Defines supporting container
                                      services

  `requirements.txt`                  Python package dependencies
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 📊 Retrieval Comparison

  Feature                              Keyword   Semantic   Hybrid
  ---------------------------------- --------- ---------- --------
  Exact word matching                       ✅         ⚠️       ✅
  Understands similar meaning               ❌         ✅       ✅
  Handles technical terms                   ✅         ✅       ✅
  Handles natural-language queries          ⚠️         ✅       ✅
  Uses embeddings                           ❌         ✅       ✅
  Uses lexical matching                     ✅         ❌       ✅

Hybrid retrieval is especially useful when a query contains both
**specific technical terms** and **conceptual language**.

------------------------------------------------------------------------

# 🛠️ Troubleshooting

## Gemini API Error

If Gemini requests fail:

1.  Verify the API key.
2.  Confirm the environment variable is loaded.
3.  Check that the configured model is available to your API account.
4.  Restart the application after changing `.env`.

Example check:

``` python
import os

print(bool(os.getenv("GEMINI_API_KEY")))
```

Do not print the actual API key.

## Ollama Connection Error

Check whether Ollama is running:

``` bash
ollama list
```

If necessary:

``` bash
ollama serve
```

Then verify that the model configured by the project is installed.

## Docker Command Not Found

If PowerShell reports:

``` text
docker : The term 'docker' is not recognized
```

check that:

-   Docker Desktop is installed
-   Docker Desktop is running
-   Docker was added to PATH
-   A new terminal was opened after installation

Then test:

``` bash
docker --version
docker compose version
```

## Port Already in Use

If the configured application or backend port is already occupied,
identify the process using the port and either stop it or change the
application's port configuration.

------------------------------------------------------------------------

# 🔐 Security Considerations

This project may use API credentials and locally running services.

Follow these practices:

-   Never commit `.env`
-   Never hard-code API keys
-   Never upload private documents to a public repository
-   Use environment variables for secrets
-   Restrict backend services to localhost when public access is
    unnecessary
-   Review retrieved document content before exposing the application
    publicly

------------------------------------------------------------------------

# 📈 Possible Improvements

Future versions can extend the system with:

-   Reranking using a cross-encoder
-   Query rewriting
-   Multi-query retrieval
-   Metadata filtering
-   Conversation memory
-   Source citations in answers
-   Retrieval score visualization
-   Document upload directly from the UI
-   OCR fallback for scanned PDFs
-   Multimodal retrieval for image-heavy documents
-   Evaluation using Recall@K, Precision@K and answer-groundedness
    metrics
-   Authentication for multi-user deployment
-   Production deployment with Docker

------------------------------------------------------------------------

# 🧠 Technologies Used

-   **Python** --- application and RAG pipeline
-   **Gradio** --- interactive web interface
-   **Embeddings** --- semantic representation of document chunks
-   **Keyword Search** --- lexical retrieval
-   **Semantic Search** --- embedding-based retrieval
-   **Hybrid Search** --- combined retrieval strategy
-   **Google Gemini** --- cloud LLM generation
-   **Ollama** --- local LLM generation
-   **Docker Compose** --- supporting service deployment

------------------------------------------------------------------------

# 🎯 Project Objectives

The project demonstrates how a complete RAG application can be built
from document processing to final answer generation.

The key objectives are:

1.  Build a reusable document-to-RAG pipeline.
2.  Preserve useful information from complex PDFs.
3.  Compare keyword, semantic and hybrid retrieval.
4.  Support both cloud and local LLM generation.
5.  Provide an easy-to-use interface for experimentation.
6.  Keep the architecture modular so individual RAG components can be
    replaced or improved independently.

------------------------------------------------------------------------

# 📌 Current Application Flow

``` text
                USER QUESTION
                      │
                      ▼
              ┌───────────────┐
              │ Search Method │
              └───────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
     Keyword       Semantic       Hybrid
        │             │             │
        └─────────────┼─────────────┘
                      ▼
             RETRIEVED CONTEXT
                      │
                      ▼
                ┌───────────┐
                │ AI Model  │
                └─────┬─────┘
                      │
             ┌────────┴────────┐
             ▼                 ▼
          Gemini             Ollama
             │                 │
             └────────┬────────┘
                      ▼
                FINAL ANSWER
```

------------------------------------------------------------------------

# 📸 Screenshots

Add project screenshots to a repository folder such as:

``` text
figures/
├── ui.png
├── architecture.png
└── pipeline.png
```

Then reference them here:

``` markdown
![LocalRAG Q&A System UI](figures/ui.png)
```

------------------------------------------------------------------------

# 📜 License

Add the license appropriate for your project, for example:

``` text
MIT License
```

A `LICENSE` file should be added to the repository if the project is
intended for public distribution.

------------------------------------------------------------------------

# 👨‍💻 Author

**Ayush Verma**

B.Tech Computer Science & Engineering

------------------------------------------------------------------------

## ⭐ Project Summary

**LocalRAG Q&A System** demonstrates an end-to-end RAG workflow where
documents are parsed, chunked, indexed and retrieved before an LLM
generates the final response.

Its modular architecture makes it suitable for experimenting with
different:

**Document Parsers → Chunking Strategies → Retrieval Methods → Embedding
Models → LLMs**

> **Retrieve relevant knowledge first. Generate the answer second.**
