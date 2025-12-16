import os
from openai import OpenAI
import json
from typing import Dict, List

class EvaluatorAgent:
    """Evaluates response quality and accuracy using LLM verification"""
    
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
    
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
        """Calculate confidence score using LLM verification"""
        
        response_text = response.get("text", "")
        # Format sources for the LLM
        context_text = "\n\n".join([f"Source: {s.get('content', '')}" for s in sources])
        
        prompt = f"""
        You are a strict fact-checker for a British Airways customer support bot.
        
        Context provided to the bot:
        {context_text}
        
        Bot's Response:
        {response_text}
        
        Task:
        1. Verify if the Bot's Response is FULLY supported by the Context.
        2. Identify any hallucinations or information not in the context.
        3. Rate confidence from 0.0 to 1.0 (1.0 = fully supported, 0.0 = completely unsupported or hallucinated).
        
        Output JSON only:
        {{
            "supported": boolean,
            "confidence_score": float,
            "reasoning": "string"
        }}
        """
        
        try:
            evaluation = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an evaluator. Output only JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            
            result = json.loads(evaluation.choices[0].message.content)
            return float(result.get("confidence_score", 0.5))
            
        except Exception as e:
            print(f"Evaluation failed: {e}")
            return 0.5 # Fallback
    
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