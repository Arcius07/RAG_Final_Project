from config import MODEL
def generate_answer(context, query):
    try:
        from langchain_groq import ChatGroq
        llm=ChatGroq(model=MODEL, temperature=0)
        prompt=f'''You are a customer support assistant. Use only context below.
Context:
{context}

Question: {query}
If answer missing, say insufficient information.'''
        return llm.invoke(prompt).content
    except Exception as e:
        # Raise error for graph to handle (LLM failure case)
        raise RuntimeError(f'LLM generation failed: {str(e)}')
