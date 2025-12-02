
from typing import List, Dict, Optional
from src.rag.vector_store import get_vector_store


class LoreRetriever:
    
    def __init__(self):
        self.vector_store = get_vector_store()
    
    def get_location_context(self, location: str, n_results: int = 2) -> List[str]:
        query = f"information about {location} location setting description"
        results = self.vector_store.search(
            query=query,
            n_results=n_results,
            filter_tags=["location"]
        )
        
        return [result["content"] for result in results]
    
    def get_npc_context(self, npc_name: str, n_results: int = 2) -> List[str]:
        query = f"information about {npc_name} backstory personality"
        results = self.vector_store.search(
            query=query,
            n_results=n_results,
            filter_tags=["npc"]
        )
        
        return [result["content"] for result in results]
    
    def get_item_context(self, item: str, n_results: int = 1) -> List[str]:
        query = f"information about {item} history properties"
        results = self.vector_store.search(
            query=query,
            n_results=n_results,
            filter_tags=["item"]
        )
        
        return [result["content"] for result in results]
    
    def get_action_context(self, action: str, location: str, n_results: int = 3) -> List[str]:
        query = f"{action} at {location}"
        results = self.vector_store.search(
            query=query,
            n_results=n_results
        )
        
        return [result["content"] for result in results]
    
    def get_world_context(self, topic: str, n_results: int = 2) -> List[str]:
        results = self.vector_store.search(
            query=topic,
            n_results=n_results,
            filter_tags=["history", "world_lore"]
        )
        
        return [result["content"] for result in results]
    
    def format_context_for_prompt(self, context_pieces: List[str], max_length: int = 500) -> str:
        if not context_pieces:
            return "No specific lore available."
        
        combined = "\n\n".join(context_pieces)
        
        if len(combined) > max_length:
            combined = combined[:max_length] + "..."
        
        return combined


_retriever_instance = None


def get_retriever() -> LoreRetriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = LoreRetriever()
    return _retriever_instance
