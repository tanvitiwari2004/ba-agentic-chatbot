# backend/database/memory.py
from typing import List, Dict, Optional
from datetime import datetime

class ConversationMemory:
    """Manages conversation history"""
    
    def __init__(self):
        self.conversations = {}  # {conversation_id: [messages]}
    
    def add_message(self, conversation_id: str, role: str, content: str):
        """Add a message to conversation history"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        self.conversations[conversation_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 10 messages to avoid memory issues
        if len(self.conversations[conversation_id]) > 10:
            self.conversations[conversation_id] = self.conversations[conversation_id][-10:]
    
    def get_history(self, conversation_id: str, limit: int = 5) -> List[Dict]:
        """Get conversation history"""
        if conversation_id not in self.conversations:
            return []
        
        # Return last N messages
        return self.conversations[conversation_id][-limit:]
    
    def get_context_string(self, conversation_id: str, limit: int = 3) -> str:
        """Get formatted conversation context for LLM"""
        history = self.get_history(conversation_id, limit)
        
        if not history:
            return ""
        
        context_parts = ["Previous conversation:"]
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            context_parts.append(f"{role}: {msg['content']}")
        
        return "\n".join(context_parts)
    
    def clear_conversation(self, conversation_id: str):
        """Clear a specific conversation"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]