
import json
from typing import Optional

from src.game_state import GameState, create_initial_state
from src.graph.graph import game_graph
from src.persistence.save_manager import save_game, load_game, list_save_files, get_last_save
from src.rag.vector_store import get_vector_store
from src.utils.display import *


class GameEngine:
    
    def __init__(self):
        self.state: Optional[GameState] = None
        self.vector_store = get_vector_store()
        self.graph = game_graph
    
    def initialize_rag_system(self):
        print_info("Initializing game world lore...")
        try:
            self.vector_store.initialize_lore(force_reload=False)
            print_success("Game world loaded successfully!")
        except Exception as e:
            print_error(f"Error loading game world: {e}")
            print_info("Continuing without RAG system...")
    
    def new_game(self, player_name: str) ->GameState:
        print_header(f"Welcome, {player_name}!")
        
        self.state = create_initial_state(player_name)
        
        try:
            with open("data/locations.json", "r") as f:
                locations = json.load(f)
            
            tavern = locations.get("tavern", {})
            starting_narrative = f"\n{tavern.get('description', '')}\n"
            
            actions = "\n".join([f"- {a}" for a in tavern.get("available_actions", [])])
            starting_narrative += f"\nWhat would you like to do?\n{actions}"
            
            self.state["last_output"] = starting_narrative
            
        except Exception as e:
            print_error(f"Error loading location data: {e}")
            self.state["last_output"] = "You awaken in an unfamiliar place..."
        
        return self.state
    
    def load_saved_game(self, filename: str) -> GameState:
        self.state = load_game(filename)
        print_success(f"Welcome back, {self.state['player_name']}!")
        return self.state
    
    def save_current_game(self, filename: Optional[str] = None) -> str:
        if self.state is None:
            raise ValueError("No active game to save")
        
        filepath = save_game(self.state, filename)
        print_success("Game saved successfully!")
        return filepath
    
    def process_action(self, action: str) -> str:
        if self.state is None:
            raise ValueError("No active game")
        
        self.state["current_action"] = action
        
        try:
            result = self.graph.invoke(self.state)
            
            self.state.update(result)
            
            return self.state["last_output"]
        
        except Exception as e:
            print_error(f"Error processing action: {e}")
            return "Something went wrong. Please try again."
    
    def get_state(self) -> Optional[GameState]:
        return self.state
    
    def is_game_over(self) -> bool:
        if self.state is None:
            return True
        
        return self.state["health"] <= 0
    
    def list_available_saves(self) -> list:
        return list_save_files()
