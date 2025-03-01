# Development of a RAG App

## Overview

This Retrieval-Augmented Generation (RAG) chatbot enables users to upload multiple documents (`.txt` or `.pdf`) and interact with their content through a conversational interface. The application efficiently processes large files by breaking them into smaller chunks and retrieving relevant information based on user queries.

## Features

- **Multi-Document Upload** – Supports uploading multiple `.txt` and `.pdf` files.
- **Efficient Document Processing** – Extracts text from PDFs and plain text files.
- **Chunking Mechanism** – Splits large documents into smaller, structured parts for retrieval.
- **AI-Driven Responses** – Uses OpenAI's GPT-4o to generate responses based on document content.
- **Vector-Based Search** – Utilizes ChromaDB for efficient document chunk retrieval.
- **Container Deployment** – Provides a consistent environment using Docker and Devcontainers.

### System Requirements

- **Docker**
- **VS Code** (recommended)
- **Git**

### Python Dependencies

The application installs all required dependencies inside the container automatically, including:

- **Document Processing**: `PyMuPDF (fitz)`
- **AI & Retrieval**: `OpenAI`, `LangChain`
- **Vector Database**: `ChromaDB`, `faiss-cpu`
- **Web Interface**: `Streamlit`
- **Data Handling**: `pandas`, `protobuf`, `pydantic`

## Installation and Setup

### Method 1: Running via Git Clone

#### 1. Clone the Repository

```sh
git clone <your_repo_url>
cd <your_repo_folder>
```

#### 2. Create an Environment File (.env) if Not Seeing Any

Create a `.env` file in the project folder and add the OpenAI API Key:

```sh
echo "OPENAI_API_KEY=your-api-key-here" > .env
echo "OPENAI_BASE_URL=https://api.ai.it.cornell.edu/" >> .env
```

Alternatively, manually create a `.env` file with the following content:

```
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.ai.it.cornell.edu/
```

#### 3. Start the Application with Docker

```sh
docker-compose up --build
```

This command will build and start the container. The first run may take a few minutes.

#### 4. Access the Chatbot
Run:
```sh
streamlit run chat_with_pdf.py
```
Once running, open:

```
http://localhost:8501
```

in a web browser.

### Method 2: Running via ZIP File

#### 1. Extract the ZIP File

- Locate and extract the `.zip` file.

```sh
unzip your_project.zip -d your_project_folder
```

#### 2. Open a Terminal and Navigate to the Project Folder

```sh
cd your_project_folder
```

#### 3. Create a `.env` File if Not Seeing Any

```sh
echo "OPENAI_API_KEY=your-api-key-here" > .env
echo "OPENAI_BASE_URL=https://api.ai.it.cornell.edu/" >> .env
```

#### 4. Start the Application with Docker

```sh
docker-compose up --build
```

Run:
```sh
streamlit run chat_with_pdf.py
```

Once complete, open:

```
http://localhost:8501
```

in a web browser.

## Development and Debugging

### Rebuilding the Container

If changes are made, rebuild the container with:

```sh
docker-compose down --volumes
docker-compose up --build
```

### Accessing the Running Container

```sh
docker exec -it info-5940-devcontainer /bin/bash
```

### Manually Running Streamlit

```sh
streamlit run chat_with_pdf.py
```

## Configuration (Environment Variables)

The `.env` file should contain:

```
OPENAI_API_KEY=your-api-key-here
```

```
OPENAI_BASE_URL=https://api.ai.it.cornell.edu/
```

## Documentation of Configuration Changes

1. **Dockerfile Adjustments**

   - Installed necessary system dependencies including `poppler-utils` for PDF processing.
   - Used `Poetry` for dependency management and disabled virtual environment creation within the container.

2. **Docker-Compose Changes**

   - Specified pymupdf = "^1.23.0"  
   - Used chromadb = "^0.4.22"

3. **Application Adjustments**

   - Updated `chat_with_pdf.py` to ensure documents are processed efficiently using `ChromaDB`.
   - Implemented `RecursiveCharacterTextSplitter` to handle large file chunking.
   - Ensured Streamlit launches correctly when the container starts.

This guide provides all necessary steps to install, run, and debug the chatbot application. If issues arise, refer to the **Development and Debugging** section for troubleshooting.

