import os
from openai import OpenAI
from typing import List, Dict

class ReasonerAgent:
    """Generates responses based on retrieved context and conversation history"""
    
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
    
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
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful British Airways customer service assistant. Use the provided context to answer questions accurately."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return {
                "text": response.choices[0].message.content,
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

CRITICAL RULES:
- Use ONLY information from the context below
- DO NOT invent phone numbers, URLs, or any information not in the context
- If information is not in the context, say "I don't have that specific information"
- DO NOT make assumptions or add extra details
- Be accurate, professional, and friendly
- Remember the conversation history to provide contextual answers
- ALWAYS end your response by politely asking if there is anything else you can assist with (e.g., "Is there anything else I can help you with regarding your journey?")

{history_section}
Context (BA Policies):
{context}

Customer Question: {query}

Provide a helpful answer using ONLY the information above. Do not add contact numbers or information not provided. Ensure you end with a polite offer of further assistance."""
