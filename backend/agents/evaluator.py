# backend/agents/evaluator.py
from typing import Dict, List
import ollama

class EvaluatorAgent:
    """Evaluates response quality and accuracy"""
    
    def __init__(self, model="llama3.2:1b"):
        self.model = model
    
    async def evaluate(
        self, 
        query: str, 
        response: Dict, 
        sources: List[Dict]
    ) -> Dict:
        """Evaluate response quality and calculate confidence"""
        
        # Calculate confidence based on multiple factors
        confidence = self._calculate_confidence(response, sources)
        
        # Extract response text
        response_text = response.get("text", "")
        
        # Check for errors
        if "error" in response:
            confidence = 0.3
        
        # Prepare sources for output
        formatted_sources = self._format_sources(sources)
        
        return {
            "response": response_text,
            "sources": formatted_sources,
            "confidence": confidence,
            "evaluation": {
                "has_sources": len(sources) > 0,
                "source_count": len(sources),
                "model_used": response.get("model_used", "unknown")
            }
        }
    
    def _calculate_confidence(self, response: Dict, sources: List[Dict]) -> float:
        """Calculate confidence score based on various factors"""
        
        confidence = 0.5  # Base confidence
        
        # Boost confidence if we have sources
        if sources and len(sources) > 0:
            confidence += 0.2
            
            # Higher confidence with more sources
            if len(sources) >= 3:
                confidence += 0.1
            
            # Boost based on source scores
            avg_source_score = sum(s.get("score", 0.5) for s in sources) / len(sources)
            confidence += (avg_source_score * 0.2)
        
        # Check response quality
        response_text = response.get("text", "")
        if len(response_text) > 50:  # Reasonable length
            confidence += 0.05
        
        if "I don't know" in response_text or "I apologize" in response_text:
            confidence -= 0.2
        
        # Cap confidence between 0 and 1
        return max(0.0, min(1.0, confidence))
    
    def _format_sources(self, sources: List[Dict]) -> List[Dict]:
        """Format sources for output"""
        
        formatted = []
        for source in sources[:3]:  # Top 3 sources only
            formatted.append({
                "content": source.get("content", "")[:200] + "...",  # Truncate
                "source": source.get("source", "Unknown"),
                "score": round(source.get("score", 0.0), 2)
            })
        
        return formatted