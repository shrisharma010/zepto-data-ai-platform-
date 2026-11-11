from fastapi import FastAPI, HTTPException
from support_assistant.schemas import AskRequest, AskResponse
from support_assistant.graph import support_graph

app = FastAPI(
    title="Zepto Support Assistant RAG API",
    version="1.0.0",
    description="Local RAG-powered customer support API built with FastAPI, ChromaDB, and LangGraph."
)

@app.get("/")
def read_root():
    return {"status": "online", "service": "Zepto Support Assistant API"}

@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    try:
        initial_state = {
            "query": request.query,
            "intent": "",
            "context": "",
            "sources": [],
            "answer": "",
            "confidence": 0.0
        }
        
        # Invoke LangGraph workflow
        final_state = support_graph.invoke(initial_state)
        
        return AskResponse(
            answer=final_state["answer"],
            sources=final_state["sources"],
            intent=final_state["intent"],
            confidence=final_state["confidence"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))