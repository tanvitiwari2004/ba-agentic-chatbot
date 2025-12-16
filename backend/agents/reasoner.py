# backend/agents/reasoner.py
from typing import List, Dict
import ollama

class ReasonerAgent:
    """Generates responses based on retrieved context and conversation history"""
    
    def __init__(self, model="llama3.2:1b"):
        self.model = model
    
    async def generate_response(
        self, 
        query: str, 
        context: List[Dict], 
        plan: Dict,
        conversation_context: str = ""
    ) -> Dict:
        """Generate response using LLM with context and conversation history"""
        
        # Build context string from retrieved documents
        context_text = self._build_context(context)
        
        # Create prompt with conversation history
        prompt = self._create_prompt(query, context_text, plan, conversation_context)
        
        try:
            # Call LLM with temperature to reduce repetition
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }],
                options={
                    'temperature': 0.7,  # Lower = more focused, less repetitive
                    'top_p': 0.9,
                    'repeat_penalty': 1.2  # Penalize repetition
                }
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
    
    def _create_prompt(self, query: str, context: str, plan: Dict, conversation_context: str) -> str:
        """Create the prompt for the LLM with conversation history"""
        
        history_section = ""
        if conversation_context:
            history_section = f"\n{conversation_context}\n"
        
        return f"""You are a helpful British Airways customer service assistant.

CRITICAL INSTRUCTIONS:
1. Give SPECIFIC, DETAILED answers - not generic ones
2. If the customer asks about a specific item (like "water bottle"), answer ONLY about that item
3. Quote exact rules, sizes, and requirements from the context
4. If multiple rules apply, explain each one clearly
5. DO NOT give general answers when specific ones are available
6. Use ONLY information from the context below
7. DO NOT invent phone numbers, URLs, or any information not in the context
8. If information is not in the context, say "I don't have that specific information"

EXAMPLE OF GOOD vs BAD:
❌ BAD: "Liquids must be in containers of 100ml or less"
✅ GOOD: "Water bottles are allowed in hand baggage if they contain 100ml or less and are placed in a transparent, resealable plastic bag. You can bring an empty water bottle and fill it after security."
{history_section}
Context (BA Policies):
{context}

Customer Question: {query}

Provide a SPECIFIC, DETAILED answer about exactly what the customer asked. Be precise and helpful."""
