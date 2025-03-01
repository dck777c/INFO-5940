import streamlit as st
import fitz # PyMuPDF for PDF text extraction
import os
import shutil  
from openai import OpenAI
from os import environ
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.schema import Document
from chromadb.config import Settings 

st.title("📝 File Q&A with OpenAI")

# File uploader for text and PDF files
uploaded_files = st.file_uploader("Upload documents (txt, pdf)", type=("txt", "pdf"), accept_multiple_files=True)

question = st.chat_input("Ask me anything about the document", disabled=not uploaded_files)
# Store chat messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask me anything about the document"}]

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Extract text from uploaded files
def extract_text(file):
    file_extension = file.name.split(".")[-1].lower()
    text = ""
    try:
        if file_extension == "txt":
            text = file.read().decode("utf-8")
        elif file_extension == "pdf":
            doc = fitz.open(stream=file.read(), filetype="pdf")   # Open PDF
            text = "\n".join([page.get_text() for page in doc])
    except Exception as e:
        st.error(f"Error reading file {file.name}: {e}")

    return f"\n\n==== {file.name} Start ====\n\n{text}\n\n==== {file.name} End ====\n\n" if text else ""

documents = []
combined_content = ""

# Process uploaded files
if uploaded_files:
    if os.path.exists("./chroma_db"):
        shutil.rmtree("./chroma_db")  

    for file in uploaded_files:
        extracted_text = extract_text(file)
        if extracted_text:
            documents.append(Document(page_content=extracted_text))# Store extracted text
            combined_content += extracted_text

embeddings = OpenAIEmbeddings(model="openai.text-embedding-3-large", api_key=environ["OPENAI_API_KEY"])

# Set up ChromaDB for retrieval
chroma_settings = Settings(
    persist_directory="./chroma_db",
    anonymized_telemetry=False 
)

vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings, 
    client_settings=chroma_settings 
)

retriever = vector_store.as_retriever()

# Process user question
if question and documents:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    # Retrieve relevant parts
    relevant_chunks = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in relevant_chunks])

    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    # Generate response using OpenAI
    client = OpenAI(api_key=environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="openai.gpt-4o",
        messages=[
            {"role": "system", "content": f"Below is the content of all uploaded documents:\n\n{combined_content}"},
            {"role": "system", "content": f"Use the following context to answer:\n\n{context}"},
            {"role": "user", "content": question},
        ],
    )

    answer = response.choices[0].message.content
    st.chat_message("assistant").write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
