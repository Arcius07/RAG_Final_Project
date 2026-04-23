import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import PDF_PATH, CHROMA_DIR

def ingest():
    # Error Case 1: Missing PDF file
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f'Place PDF at {PDF_PATH}')
    
    # Error Case 2: Invalid PDF or loading failure
    try:
        docs=PyPDFLoader(PDF_PATH).load()
    except Exception as e:
        raise ValueError(f'Invalid PDF file: {str(e)}. Ensure it is a valid text-based PDF.')
    
    # Error Case 3: No content extracted
    if not docs:
        raise ValueError('PDF contains no extractable text. Use text-based PDF, not scanned images.')
    
    splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks=splitter.split_documents(docs)
    
    if not chunks:
        raise ValueError('PDF text too short or unreadable. Check PDF content.')
    
    emb=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db=Chroma.from_documents(chunks, emb, persist_directory=CHROMA_DIR)
    db.persist()
    return len(chunks)
