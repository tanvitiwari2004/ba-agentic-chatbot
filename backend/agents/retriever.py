# backend/agents/retriever.py
from typing import List, Dict

class RetrieverAgent:
    """Retrieves relevant information from vector store"""
    
    def __init__(self, vector_store=None):
        self.vector_store = vector_store
    
    async def retrieve(self, query: str, plan: Dict, top_k: int = 8) -> List[Dict]:
        """Retrieve relevant documents based on query and plan"""
        
        # If vector store exists, use it
        if self.vector_store:
            try:
                # Expand query with keywords for better matching
                expanded_query = f"{query} {' '.join(plan.get('keywords', []))}"
                results = self.vector_store.search(
                    query=expanded_query,
                    query_type=plan["query_type"],
                    top_k=top_k
                )
                
                return [
                    {
                        "content": r["text"],
                        "source": r["source"],
                        "score": r["score"],
                        "metadata": r.get("metadata", {})
                    }
                    for r in results
                ]
            except Exception as e:
                print(f"Vector store error: {e}")
                return self._get_fallback_context(plan["query_type"])
        
        # Fallback: return basic context based on query type
        return self._get_fallback_context(plan["query_type"])
    
    def _get_fallback_context(self, query_type: str) -> List[Dict]:
        """Provide basic context when vector store unavailable"""
        
        fallback_info = {
            "liquids": {
                "content": "Liquids must be in containers of 100ml or less, placed in a transparent resealable plastic bag (20x20cm, 1 litre capacity). Exceptions include baby food and medications.",
                "source": "BA Policy - Liquids",
                "score": 0.9
            },
            "baggage": {
                "content": "Hand baggage allowance varies by cabin class. Check your specific allowance in Manage My Booking. Checked baggage fees may apply.",
                "source": "BA Policy - Baggage",
                "score": 0.9
            },
            "medical": {
                "content": "Medical equipment and medications are permitted. Medical clearance may be required for certain conditions. Carry prescriptions with medications.",
                "source": "BA Policy - Medical",
                "score": 0.9
            }
        }
        
        info = fallback_info.get(query_type, {
            "content": "Please refer to British Airways website for detailed policy information.",
            "source": "BA General Policy",
            "score": 0.7
        })
        
        return [info]