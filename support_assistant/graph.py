import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from support_assistant.rag import query_rag
from support_assistant.prompts import RAG_ANSWER_PROMPT

class GraphState(TypedDict):
    query: str
    intent: str
    context: str
    sources: List[str]
    answer: str
    confidence: float

def classify_intent_node(state: GraphState):
    q = state["query"].lower()
    # Rule-based fallback classifier for robust mock mode
    if any(keyword in q for keyword in ["deliver", "return", "refund", "membership", "cancel", "shipping", "track"]):
        intent = "policy_rag"
    elif any(keyword in q for keyword in ["hello", "hi", "hey", "help"]):
        intent = "general"
    else:
        intent = "policy_rag" # Default to RAG lookup
    return {"intent": intent}

def retrieve_node(state: GraphState):
    query = state["query"]
    context, sources = query_rag(query, n_results=2)
    return {"context": context, "sources": sources}

def generate_node(state: GraphState):
    query = state["query"]
    context = state["context"]
    sources = state["sources"]
    
    if state["intent"] == "general":
        answer = "Hello! Welcome to Zepto Customer Support. How can I assist you with your orders or policies today?"
        confidence = 0.99
    elif context.strip():
        # Mock LLM generation synthesizing retrieved context
        answer = f"Based on our official company policies: {context[:300]}... Please let me know if you need further clarification!"
        confidence = 0.92
    else:
        answer = "I'm sorry, I couldn't find specific policy details regarding your request. Please reach out to our human support team."
        confidence = 0.50
        
    return {"answer": answer, "sources": sources, "confidence": confidence}

def build_support_graph():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("classify_intent", classify_intent_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    
    workflow.set_entry_point("classify_intent")
    
    # Conditional routing based on intent
    def route_intent(state: GraphState):
        if state["intent"] == "general":
            return "generate"
        return "retrieve"

    workflow.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "retrieve": "retrieve",
            "generate": "generate"
        }
    )
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()

# Compiled graph instance
support_graph = build_support_graph()