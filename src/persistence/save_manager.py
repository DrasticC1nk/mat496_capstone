
import json
import os
from datetime import datetime
from typing import Optional, List
from pathlib import Path

from src.game_state import GameState
from src.config import SAVE_DIRECTORY


def save_game(state: GameState, filename: Optional[str] = None) -> str:
    SAVE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"save_{state['player_name']}_{timestamp}"
    
    if not filename.endswith(".json"):
        filename += ".json"
    
    filepath = SAVE_DIRECTORY / filename
    
    state_copy = dict(state)
    state_copy["last_save_time"] = datetime.now().isoformat()
    
    with open(filepath, "w") as f:
        json.dump(state_copy, f, indent=2)
    
    print(f"Game saved to: {filepath}")
    return str(filepath)


def load_game(filename: str) -> GameState:
    if not filename.endswith(".json"):
        filename += ".json"
    
    filepath = SAVE_DIRECTORY / filename
    
    if not filepath.exists():
        raise FileNotFoundError(f"Save file not found: {filepath}")
    
    with open(filepath, "r") as f:
        state = json.load(f)
    
    print(f"Game loaded from: {filepath}")
    return GameState(**state)


def list_save_files() -> List[dict]:
    if not SAVE_DIRECTORY.exists():
        return []
    
    saves = []
    for filepath in SAVE_DIRECTORY.glob("*.json"):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                saves.append({
                    "filename": filepath.name,
                    "player_name": data.get("player_name", "Unknown"),
                    "last_save_time": data.get("last_save_time", "Unknown"),
                    "location": data.get("current_location", "Unknown"),
                    "level": data.get("level", 1)
                })
        except Exception as e:
            print(f"Error reading save file {filepath}: {e}")
    
    saves.sort(key=lambda x: x["last_save_time"], reverse=True)
    
    return saves


def get_last_save() -> Optional[str]:
    saves = list_save_files()
    if saves:
        return saves[0]["filename"]
    return None


def delete_save(filename: str) -> bool:
    if not filename.endswith(".json"):
        filename += ".json"
    
    filepath = SAVE_DIRECTORY / filename
    
    try:
        if filepath.exists():
            filepath.unlink()
            print(f"Deleted save file: {filepath}")
            return True
        else:
            print(f"Save file not found: {filepath}")
            return False
    except Exception as e:
        print(f"Error deleting save file: {e}")
        return False
