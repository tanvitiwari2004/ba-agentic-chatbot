# backend/agents/planner.py
from typing import Dict, List
import ollama

class PlannerAgent:
    """Plans the retrieval and reasoning strategy"""
    
    def __init__(self, model="llama3.2:1b"):
        self.model = model
    
    async def create_plan(self, query: str) -> Dict:
        """Analyze query and create a retrieval plan"""
        
        # Classify the query type
        query_type = self._classify_query(query)
        
        # Extract keywords
        keywords = self._extract_keywords(query)
        
        return {
            "query_type": query_type,
            "keywords": keywords,
            "priority": "high",
            "depth": "detailed"
        }
    
    def _classify_query(self, query: str) -> str:
        """Classify query into categories"""
        query_lower = query.lower()
        
        categories = {
            "liquids": ["liquid", "water", "bottle", "gel", "cream", "shampoo", "100ml"],
            "baggage": ["bag", "luggage", "suitcase", "carry-on", "checked", "allowance", "weight"],
            "medical": ["medicine", "medical", "wheelchair", "oxygen", "pregnant", "disability", "prescription"],
            "sports": ["bike", "golf", "ski", "surfboard", "diving", "equipment", "bicycle"],
            "prohibited": ["prohibited", "forbidden", "not allowed", "banned", "restricted", "dangerous"],
            "electronics": ["battery", "laptop", "phone", "charger", "power bank", "lithium"],
            "food": ["food", "snack", "meal", "eat", "drink", "infant", "baby"]
        }
        
        for category, terms in categories.items():
            if any(term in query_lower for term in terms):
                return category
        
        return "general"
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from query"""
        # Remove common words
        stop_words = {"can", "i", "my", "the", "a", "an", "is", "are", "what", "how", "do", "does"}
        words = query.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords[:5]  # Top 5 keywords