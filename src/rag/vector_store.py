
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import os

from src.config import VECTOR_STORE_PATH, get_embeddings
from src.rag.lore_data import get_all_lore_documents


class LoreVectorStore:
    
    def __init__(self, persist_directory: Optional[str] = None):
        self.persist_directory = persist_directory or str(VECTOR_STORE_PATH)
        
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.collection = self.client.get_or_create_collection(
            name="game_lore",
            metadata={"description": "Medieval fantasy RPG world lore"}
        )
        
        self.embeddings = get_embeddings()
    
    def initialize_lore(self, force_reload: bool = False):
        if self.collection.count() > 0 and not force_reload:
            print(f"Vector store already contains {self.collection.count()} documents.")
            return
        
        if force_reload:
            self.client.delete_collection("game_lore")
            self.collection = self.client.create_collection(
                name="game_lore",
                metadata={"description": "Medieval fantasy RPG world lore"}
            )
        
        documents = get_all_lore_documents()
        
        ids = [doc["id"] for doc in documents]
        contents = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        
        print(f"Adding {len(documents)} lore documents to vector store...")
        embeddings_list = self.embeddings.embed_documents(contents)
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings_list,
            documents=contents,
            metadatas=metadatas
        )
        
        print(f"Successfully initialized vector store with {self.collection.count()} documents.")
    
    def search(
        self,
        query: str,
        n_results: int = 3,
        filter_tags: Optional[List[str]] = None
    ) -> List[Dict]:
        query_embedding = self.embeddings.embed_query(query)
        
        where_filter = None
        if filter_tags:
            where_filter = {"tags": {"$in": filter_tags}}
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter if where_filter else None
        )
        
        formatted_results = []
        if results['documents'] and len(results['documents']) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def get_by_category(self, category: str, n_results: int = 5) -> List[Dict]:
        results = self.collection.get(
            where={"category": category},
            limit=n_results
        )
        
        formatted_results = []
        if results['documents']:
            for i in range(len(results['documents'])):
                formatted_results.append({
                    "content": results['documents'][i],
                    "metadata": results['metadatas'][i]
                })
        
        return formatted_results


_vector_store_instance = None


def get_vector_store() -> LoreVectorStore:
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = LoreVectorStore()
    return _vector_store_instance
