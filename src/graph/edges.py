
from src.game_state import GameState


def route_action(state: GameState) -> str:
    action = state["current_action"].lower()
    
    if any(word in action for word in ["give", "tip", "donate", "pay", "offer", "here's", "here is", "take", "have"]):
        if any(word in action for word in ["gold", "coin", "money"]) or any(char.isdigit() for char in action):
            return "inventory"
    
    if any(word in action for word in ["rest", "heal", "sleep", "recover"]):
        if state["current_location"] == "tavern":
            return "inventory"
        else:
            return "story_generator"
    
    if any(word in action for word in ["talk", "speak", "ask", "tell", "greet", "chat"]):
        known_npcs = ["keeper", "marta", "guard", "borin", "elara", "guardian", "merchant", "tobias", "bandit", "grimjaw"]
        if any(npc in action for npc in known_npcs):
            return "npc_interaction"
        else:
            return "story_generator"
    
    elif any(word in action for word in ["attack", "fight", "combat", "challenge", "punch", "hit", "strike"]):
        return "combat"
    
    elif any(word in action for word in ["go to", "travel", "walk", "head", "move", "visit", "leave"]):
        return "location_change"
    
    elif any(word in action for word in ["use", "drink", "eat", "equip"]):
        return "inventory"
    
    elif any(word in action for word in ["inventory", "check items", "show items"]):
        return "inventory"
    
    else:
        return "story_generator"


def should_continue(state: GameState) -> str:
    if state["health"] <= 0:
        return "end"
    
    if "quit" in state["current_action"].lower() or "exit" in state["current_action"].lower():
        return "end"
    
    return "continue"
