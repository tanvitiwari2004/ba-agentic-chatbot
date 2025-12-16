import os
from openai import OpenAI
import json
from typing import Dict

class PlannerAgent:
    
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
    
    async def create_plan(self, query: str) -> Dict:
        """Analyze query and create a retrieval plan"""
        
        prompt = f"""
        Analyze the following user query for a British Airways chatbot.
        Query: "{query}"
        
        Determine:
        1. The primary category (liquids, baggage, medical, sports, prohibited, electronics, food, or general).
        2. Relevant search keywords/phrases to find in the policy documents.
        3. The user's underlying intent (informational, specific-restriction, allowance-check).
        
        Output JSON only:
        {{
            "query_type": "string",
            "keywords": ["string", "string"],
            "intent": "string",
            "priority": "high/medium/low",
            "search_queries": ["string"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a strategic planner for a search agent. Output JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            
            plan = json.loads(response.choices[0].message.content)
            return plan
            
        except Exception as e:
            print(f"Planning failed: {e}")
            # Fallback to simple keyword extraction
            return {
                "query_type": "general",
                "keywords": query.split(),
                "priority": "medium",
                "search_queries": [query]
            }