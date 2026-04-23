from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from retriever import get_docs
from llm import generate_answer
from hitl import escalate
from config import CONFIDENCE_THRESHOLD

class State(TypedDict, total=False):
    query:str
    chunks:list
    context:str
    answer:str
    confidence:float
    escalate:bool
    error:str

def process(state):
    try:
        # Attempt to retrieve relevant chunks from vector database
        docs=get_docs(state['query'])
        chunks=[d.page_content for d in docs]
        
        # Error Case 1: No relevant chunks found
        if not chunks:
            return {
                'chunks':[],
                'context':'',
                'answer':'I could not find relevant information in the knowledge base. Please escalate.',
                'confidence':0.0,
                'escalate':True,
                'error':'No relevant chunks found'
            }
        
        context='\n\n'.join(chunks)
        
        # Generate answer with error handling for LLM
        try:
            ans=generate_answer(context, state['query'])
        except Exception as e:
            # Error Case 3: LLM failure - return fallback response
            return {
                'chunks':chunks,
                'context':context,
                'answer':'Service temporarily unavailable. Your request has been escalated.',
                'confidence':0.0,
                'escalate':True,
                'error':f'LLM failure: {str(e)}'
            }
        
        conf=0.85 if chunks else 0.0
        if 'insufficient information' in ans.lower(): conf=0.2
        esc = conf < CONFIDENCE_THRESHOLD or any(k in state['query'].lower() for k in ['refund','legal','complaint'])
        return {'chunks':chunks,'context':context,'answer':ans,'confidence':conf,'escalate':esc}
    
    except Exception as e:
        # Error Case 2: Database or retrieval failure
        return {
            'chunks':[],
            'context':'',
            'answer':'Service temporarily unavailable. Your request has been escalated.',
            'confidence':0.0,
            'escalate':True,
            'error':f'Database error: {str(e)}'
        }

def output(state):
    if state['escalate']:
        return {'answer':escalate(state['query'], state['answer']), 'confidence':state['confidence'], 'escalate':True}
    return {'answer':state['answer'],'confidence':state['confidence'],'escalate':False}

g=StateGraph(State)
g.add_node('process', process)
g.add_node('output', output)
g.set_entry_point('process')
g.add_edge('process','output')
g.add_edge('output', END)
app_graph=g.compile()
