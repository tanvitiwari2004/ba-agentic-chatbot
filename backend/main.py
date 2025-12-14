# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

# Import agents
from agents.planner import PlannerAgent
from agents.retriever import RetrieverAgent
from agents.reasoner import ReasonerAgent
from agents.evaluator import EvaluatorAgent
from database.vector_store import VectorStore

app = FastAPI(title="BA Chatbot API - Agentic System", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
print("🚀 Initializing BA Chatbot Agent System...")

vector_store = VectorStore()

# Load BA policy documents if available
data_file = "../data/ba_liquids_and_restrictions.txt"
if os.path.exists(data_file):
    print(f"📚 Loading BA policy documents from {data_file}")
    vector_store.load_documents(data_file)
else:
    print(f"⚠️ Warning: {data_file} not found. Using fallback responses.")

# Initialize agents
planner = PlannerAgent()
retriever = RetrieverAgent(vector_store)
reasoner = ReasonerAgent()
evaluator = EvaluatorAgent()

print("✅ All agents initialized successfully!")

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: List[dict]
    confidence: float

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "agents": ["planner", "retriever", "reasoner", "evaluator"],
        "vector_store": "active" if vector_store.initialized else "inactive"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint with full agentic workflow"""
    try:
        print(f"\n💬 New query: {request.message}")
        
        # Step 1: Planner Agent - Analyze query and create plan
        print("🧠 Planner: Analyzing query...")
        plan = await planner.create_plan(request.message)
        print(f"   → Query type: {plan['query_type']}")
        
        # Step 2: Retriever Agent - Get relevant information
        print("🔍 Retriever: Searching for relevant information...")
        retrieved_docs = await retriever.retrieve(
            query=request.message,
            plan=plan
        )
        print(f"   → Found {len(retrieved_docs)} relevant documents")
        
        # Step 3: Reasoner Agent - Generate response
        print("💡 Reasoner: Generating response...")
        response = await reasoner.generate_response(
            query=request.message,
            context=retrieved_docs,
            plan=plan
        )
        
        # Step 4: Evaluator Agent - Validate and score
        print("✅ Evaluator: Validating response...")
        evaluation = await evaluator.evaluate(
            query=request.message,
            response=response,
            sources=retrieved_docs
        )
        print(f"   → Confidence: {evaluation['confidence']:.2f}")
        
        return ChatResponse(
            response=evaluation["response"],
            conversation_id=request.conversation_id or "new",
            sources=evaluation["sources"],
            confidence=evaluation["confidence"]
        )
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "BA Chatbot API - Agentic Framework",
        "version": "2.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)