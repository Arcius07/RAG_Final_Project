from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import CHROMA_DIR, TOP_K

def get_docs(query):
    try:
        emb=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        db=Chroma(persist_directory=CHROMA_DIR, embedding_function=emb)
        return db.similarity_search(query, k=TOP_K)
    except Exception as e:
        # Database failure - raise error to be caught by graph
        raise RuntimeError(f'Database retrieval failed: {str(e)}')
