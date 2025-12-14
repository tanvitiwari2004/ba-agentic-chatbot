# backend/agents/reasoner.py
from typing import List, Dict
import ollama

class ReasonerAgent:
    """Generates responses based on retrieved context"""
    
    def __init__(self, model="llama3.2:1b"):
        self.model = model
    
    async def generate_response(
        self, 
        query: str, 
        context: List[Dict], 
        plan: Dict
    ) -> Dict:
        """Generate response using LLM with context"""
        
        # Build context string from retrieved documents
        context_text = self._build_context(context)
        
        # Create prompt
        prompt = self._create_prompt(query, context_text, plan)
        
        try:
            # Call LLM
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }]
            )
            
            return {
                "text": response["message"]["content"],
                "raw_context": context,
                "model_used": self.model
            }
        
        except Exception as e:
            return {
                "text": f"I apologize, but I encountered an error processing your request. Please try rephrasing your question or contact British Airways directly.",
                "raw_context": context,
                "error": str(e)
            }
    
    def _build_context(self, context: List[Dict]) -> str:
        """Build formatted context from retrieved documents"""
        if not context:
            return "No specific policy information available."
        
        context_parts = []
        for i, doc in enumerate(context, 1):
            context_parts.append(
                f"[Source {i} - {doc.get('source', 'Unknown')}]:\n{doc.get('content', '')}"
            )
        
        return "\n\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str, plan: Dict) -> str:
        """Create the prompt for the LLM"""
        
        return f"""You are a helpful British Airways customer service assistant. 

Your task is to answer the customer's question using ONLY the information provided in the context below. Be accurate, professional, and friendly.

Important guidelines:
- Use ONLY information from the provided context
- If the context doesn't contain the answer, say so politely
- Be specific and cite relevant policies
- Keep responses concise but complete
- Use a warm, helpful tone
- Don't make up information

Context (BA Policies):
{context}

Customer Question: {query}

Please provide a helpful, accurate answer based on the context above."""