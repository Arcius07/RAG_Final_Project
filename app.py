from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from ingest import ingest
from graph import app_graph
from config import CHROMA_DIR

# -----------------------------
# Initial Setup
# -----------------------------
st.set_page_config(
    page_title="RAG Customer Support Assistant",
    page_icon="🤖",
    layout="centered"
)

# Build vector DB if missing
if not os.path.exists(CHROMA_DIR):
    try:
        ingest()
    except Exception as e:
        st.error(f"Startup Error: {e}")

# -----------------------------
# UI
# -----------------------------
st.title("🤖 RAG Customer Support Assistant")
st.markdown("Ask questions based on your PDF knowledge base.")

query = st.text_input("Enter your query")

if st.button("Submit"):

    query = query.strip()

    # Validation
    if not query:
        st.warning("Query cannot be empty.")
    
    elif len(query) < 3:
        st.warning("Query too short (minimum 3 characters).")

    elif len(query) > 500:
        st.warning("Query too long (maximum 500 characters).")

    else:
        with st.spinner("Generating response..."):
            result = app_graph.invoke({"query": query})

        # Error Case
        if "error" in result:
            st.error(result["error"])

        else:
            st.success("Response Generated")

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Confidence")
            st.progress(float(result["confidence"]))
            st.write(round(result["confidence"], 2))

            st.subheader("Escalation Status")
            if result["escalate"]:
                st.error("Escalated to Human Support")
            else:
                st.success("Handled by AI")