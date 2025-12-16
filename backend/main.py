# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import uuid

# Import agents
from agents.planner import PlannerAgent
from agents.retriever import RetrieverAgent
from agents.reasoner import ReasonerAgent
from agents.evaluator import EvaluatorAgent
from database.vector_store import VectorStore
from database.memory import ConversationMemory

app = FastAPI(title="BA Chatbot API - Agentic System with Memory", version="2.1.0")

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

# Initialize conversation memory
memory = ConversationMemory()

print("✅ All agents initialized successfully!")
print("🧠 Conversation memory enabled!")

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
        "version": "2.1.0",
        "features": ["agents", "vector_store", "conversation_memory"],
        "agents": ["planner", "retriever", "reasoner", "evaluator"],
        "vector_store": "active" if vector_store.initialized else "inactive"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint with full agentic workflow and conversation memory"""
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        print(f"\n💬 New query: {request.message}")
        print(f"🆔 Conversation ID: {conversation_id}")
        
        # Step 0: Get conversation history
        conversation_context = memory.get_context_string(conversation_id)
        if conversation_context:
            print(f"🧠 Retrieved conversation history ({len(memory.get_history(conversation_id))} messages)")
        
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
        
        # Step 3: Reasoner Agent - Generate response with conversation context
        print("💡 Reasoner: Generating response with conversation context...")
        response = await reasoner.generate_response(
            query=request.message,
            context=retrieved_docs,
            plan=plan,
            conversation_context=conversation_context
        )
        
        # Step 4: Evaluator Agent - Validate and score
        print("✅ Evaluator: Validating response...")
        evaluation = await evaluator.evaluate(
            query=request.message,
            response=response,
            sources=retrieved_docs
        )
        print(f"   → Confidence: {evaluation['confidence']:.2f}")
        
        # Step 5: Save to conversation memory
        memory.add_message(conversation_id, "user", request.message)
        memory.add_message(conversation_id, "assistant", evaluation["response"])
        print(f"💾 Saved to conversation memory")
        
        return ChatResponse(
            response=evaluation["response"],
            conversation_id=conversation_id,
            sources=evaluation["sources"],
            confidence=evaluation["confidence"]
        )
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/conversation/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear a specific conversation history"""
    memory.clear_conversation(conversation_id)
    return {"message": f"Conversation {conversation_id} cleared"}

class FeedbackRequest(BaseModel):
    satisfied: bool
    reason: Optional[str] = None
    query: Optional[str] = None
    response: Optional[str] = None

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Store user feedback for future model improvements (Offline Learning)"""
    import json
    from datetime import datetime
    
    feedback_file = "../data/feedback_history.json"
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "satisfied": feedback.satisfied,
        "reason": feedback.reason,
        "query": feedback.query,
        "response": feedback.response
    }
    
    try:
        # Append to feedback log
        history = []
        if os.path.exists(feedback_file):
            with open(feedback_file, "r") as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []
        
        history.append(entry)
        
        # Write back to file
        with open(feedback_file, "w") as f:
            json.dump(history, f, indent=2)
            
        print(f"📝 Feedback stored: Satisfied={feedback.satisfied}, Reason={feedback.reason}")
        return {"status": "success", "message": "Feedback recorded for learning"}
        
    except Exception as e:
        print(f"❌ Error saving feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save feedback")

@app.get("/")
async def root():
    return {
        "message": "BA Chatbot API - Agentic Framework with Memory",
        "version": "2.1.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)