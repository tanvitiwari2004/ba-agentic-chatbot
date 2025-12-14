# backend/database/vector_store.py
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os
from typing import List, Dict

class VectorStore:
    """Handles document storage and retrieval using ChromaDB"""
    
    def __init__(self, persist_dir="./chroma_db"):
        try:
            self.client = chromadb.PersistentClient(path=persist_dir)
            
            self.collection = self.client.get_or_create_collection(
                name="ba_policies",
                metadata={"hnsw:space": "cosine"}
            )
            
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            self.initialized = True
            print("✅ Vector store initialized successfully")
            
        except Exception as e:
            print(f"⚠️ Vector store initialization failed: {e}")
            self.initialized = False
    
    def load_documents(self, file_path: str):
        """Load BA policies from text file"""
        if not self.initialized:
            print("Vector store not initialized")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into sections
            sections = self._split_into_sections(content)
            
            print(f"📄 Loading {len(sections)} sections into vector store...")
            
            # Add to vector store
            for i, section in enumerate(sections):
                embedding = self.encoder.encode(section["text"]).tolist()
                
                self.collection.add(
                    ids=[f"doc_{i}"],
                    embeddings=[embedding],
                    documents=[section["text"]],
                    metadatas=[{
                        "source": "ba_liquids_and_restrictions.txt",
                        "section": section["title"],
                        "category": section["category"]
                    }]
                )
            
            print(f"✅ Successfully loaded {len(sections)} sections")
            
        except Exception as e:
            print(f"❌ Error loading documents: {e}")
    
    def search(self, query: str, query_type: str = "general", top_k: int = 5) -> List[Dict]:
        """Search for relevant documents"""
        if not self.initialized:
            return []
        
        try:
            query_embedding = self.encoder.encode(query).tolist()
            
            # Search with optional category filter
            if query_type != "general":
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where={"category": query_type}
                )
            else:
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k
                )
            
            # Format results
            formatted_results = []
            if results["documents"] and len(results["documents"][0]) > 0:
                for i in range(len(results["documents"][0])):
                    formatted_results.append({
                        "text": results["documents"][0][i],
                        "source": results["metadatas"][0][i].get("source", ""),
                        "score": 1.0 - results["distances"][0][i],  # Convert distance to similarity
                        "metadata": results["metadatas"][0][i]
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def _split_into_sections(self, content: str) -> List[Dict]:
        """Split content into meaningful sections"""
        sections = []
        lines = content.split('\n')
        
        current_section = {"title": "Introduction", "text": "", "category": "general"}
        current_text = []
        
        for line in lines:
            # Check if this is a section header
            if line.startswith('===') or line.startswith('---'):
                # Save previous section if it has content
                if current_text:
                    current_section["text"] = '\n'.join(current_text).strip()
                    if len(current_section["text"]) > 50:  # Only add substantial sections
                        sections.append(current_section.copy())
                    current_text = []
                
                # Start new section
                current_section["title"] = line.strip('= -')
                current_section["category"] = self._categorize(line)
            else:
                if line.strip():
                    current_text.append(line)
        
        # Add last section
        if current_text:
            current_section["text"] = '\n'.join(current_text).strip()
            if len(current_section["text"]) > 50:
                sections.append(current_section)
        
        return sections
    
    def _categorize(self, title: str) -> str:
        """Categorize section based on title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ["liquid", "powder", "gel", "aerosol"]):
            return "liquids"
        elif any(word in title_lower for word in ["medical", "medicine", "pregnant", "health"]):
            return "medical"
        elif any(word in title_lower for word in ["sport", "bike", "golf", "ski", "equipment"]):
            return "sports"
        elif any(word in title_lower for word in ["prohibited", "forbidden", "restricted", "banned"]):
            return "prohibited"
        elif any(word in title_lower for word in ["battery", "electronic", "device", "laptop"]):
            return "electronics"
        elif any(word in title_lower for word in ["baggage", "luggage", "bag", "allowance"]):
            return "baggage"
        else:
            return "general"