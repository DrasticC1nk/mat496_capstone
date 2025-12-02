
import json
from typing import Dict
from langchain_core.messages import HumanMessage, SystemMessage

from src.game_state import GameState, StoryOutput, NPCDialogue, CombatAction, LocationChange
from src.config import get_llm
from src.rag.retriever import get_retriever
from src.prompts.system_prompts import (
    format_story_prompt,
    format_npc_prompt,
    COMBAT_NARRATOR_PROMPT
)
from src.tools.dice import combat_roll, d20_roll
from src.tools.inventory import use_item
import json as json_module


def story_generator_node(state: GameState) -> Dict:
    print("[Node: Story Generator]")
    
    retriever = get_retriever()
    lore_context = retriever.get_action_context(
        action=state["current_action"],
        location=state["current_location"],
        n_results=2
    )
    
    prompt = format_story_prompt(
        location=state["current_location"],
        action=state["current_action"],
        lore_context=lore_context
    )
    
    llm = get_llm()
    
    try:
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"Generate narrative for: {state['current_action']}")
        ]
        
        response = llm.invoke(messages)
        
        try:
            story_data = json.loads(response.content)
            narrative = story_data.get("narrative", response.content)
        except json.JSONDecodeError:
            narrative = response.content
        
        return {
            "last_output": narrative
        }
    
    except Exception as e:
        print(f"Story generation error: {e}")
        return {
            "last_output": f"You {state['current_action']} at {state['current_location']}."
        }


def npc_interaction_node(state: GameState) -> Dict:
    print("[Node: NPC Interaction]")
    
    action = state["current_action"].lower()
    
    try:
        with open("data/npcs.json", "r") as f:
            npc_data = json.load(f)
    except Exception as e:
        print(f"Error loading NPC data: {e}")
        return {}
    
    npc_key = None
    for key, npc in npc_data.items():
        if key.replace("_", " ") in action:
            npc_key = key
            break
        if npc["name"].lower() in action:
            npc_key = key
            break
        npc_words = npc["name"].lower().split()
        if any(word in action for word in npc_words if len(word) > 3):
            npc_key = key
            break
        if npc.get("location") == state["current_location"]:
            if "keeper" in action and "tavern_keeper" == key:
                npc_key = key
                break
            if "guard" in action and "castle_guard" == key:
                npc_key = key
                break
            if "guardian" in action and "forest_guardian" == key:
                npc_key = key
                break
            if "merchant" in action or "trader" in action and "merchant" in key:
                npc_key = key
                break
    
    if not npc_key:
        location_npcs = [key for key, npc in npc_data.items() if npc.get("location") == state["current_location"]]
        if len(location_npcs) == 1:
            npc_key = location_npcs[0]
        else:
            return {
                "last_output": "There's no one here to talk to. Try being more specific, like 'talk to the tavern keeper'."
            }
    
    npc = npc_data[npc_key]
    
    current_relationship = state["npc_relationships"].get(npc["name"], npc.get("initial_relationship", 0))
    
    prompt = format_npc_prompt(
        npc_data=npc,
        player_name=state["player_name"],
        current_location=state["current_location"],
        player_action=state["current_action"],
        conversation_history=state["conversation_history"],
        relationship=current_relationship
    )
    
    llm = get_llm()
    
    try:
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=state["current_action"])
        ]
        
        response = llm.invoke(messages)
        
        try:
            npc_response = json.loads(response.content)
            dialogue = npc_response.get("dialogue", response.content)
            relationship_change = npc_response.get("relationship_change", 0)
        except json.JSONDecodeError:
            dialogue = response.content
            relationship_change = 0
        
        new_history = state["conversation_history"].copy()
        new_history.append({
            "speaker": state["player_name"],
            "message": state["current_action"]
        })
        new_history.append({
            "speaker": npc["name"],
            "message": dialogue
        })
        
        new_history = new_history[-10:]
        
        new_relationships = state["npc_relationships"].copy()
        new_relationships[npc["name"]] = min(100, max(-100, current_relationship + relationship_change))
        
        return {
            "last_output": f"{npc['name']}: \"{dialogue}\"",
            "conversation_history": new_history,
            "npc_relationships": new_relationships
        }
    
    except Exception as e:
        print(f"NPC interaction error: {e}")
        return {
            "last_output": f"{npc['name']} doesn't respond."
        }


def combat_node(state: GameState) -> Dict:
    print("[Node: Combat]")
    
    combat_active = state["game_flags"].get("combat_active", False)
    
    if not combat_active:
        enemy_name = "Bandit"
        enemy_level = 2
        enemy_health = 30
        
        new_flags = state["game_flags"].copy()
        new_flags["combat_active"] = True
        new_flags["enemy_name"] = enemy_name
        new_flags["enemy_level"] = enemy_level
        new_flags["enemy_health"] = enemy_health
        
        narrative = f"⚔️ Combat begins! You face a {enemy_name}!\n\n"
    else:
        enemy_name = state["game_flags"].get("enemy_name", "Bandit")
        enemy_level = state["game_flags"].get("enemy_level", 2)
        enemy_health = state["game_flags"].get("enemy_health", 30)
        narrative = ""
        new_flags = state["game_flags"].copy()
    
    hit, damage, roll = combat_roll(
        attacker_level=state["level"],
        defender_level=enemy_level
    )
    
    if hit:
        enemy_health -= damage
        new_flags["enemy_health"] = enemy_health
        
        if roll == 20:
            narrative += f"🌟 CRITICAL HIT! You strike with devastating force!\n"
        
        narrative += f"⚔️ You hit the {enemy_name} for {damage} damage! (rolled {roll})\n"
        
        if enemy_health <= 0:
            gold_reward = 30
            xp_reward = 50
            
            narrative += f"\n💀 The {enemy_name} falls defeated!\n"
            narrative += f"🏆 Victory! You gained {gold_reward} gold and {xp_reward} experience!"
            
            new_flags["combat_active"] = False
            new_flags.pop("enemy_name", None)
            new_flags.pop("enemy_level", None)
            new_flags.pop("enemy_health", None)
            
            return {
                "last_output": narrative,
                "gold": state["gold"] + gold_reward,
                "experience": state["experience"] + xp_reward,
                "game_flags": new_flags
            }
        else:
            narrative += f"Enemy Health: {enemy_health}/30\n"
    else:
        narrative += f"❌ You miss! (rolled {roll})\n"
    
    enemy_hit, enemy_damage, _ = combat_roll(
        attacker_level=enemy_level,
        defender_level=state["level"]
    )
    
    if enemy_hit:
        narrative += f"💥 The {enemy_name} strikes back for {enemy_damage} damage!"
        new_health = max(0, state["health"] - enemy_damage)
        
        if new_health <= 0:
            narrative += "\n\n☠️ You have been defeated..."
            new_flags["combat_active"] = False
            new_flags.pop("enemy_name", None)
            new_flags.pop("enemy_level", None)
            new_flags.pop("enemy_health", None)
            
            return {
                "last_output": narrative,
                "health": 0,
                "current_location": "tavern",
                "game_flags": new_flags
            }
        
        return {
            "last_output": narrative,
            "health": new_health,
            "game_flags": new_flags
        }
    else:
        narrative += f"🛡️ The {enemy_name} misses!"
        return {
            "last_output": narrative,
            "game_flags": new_flags
        }


def location_change_node(state: GameState) -> Dict:
    print("[Node: Location Change]")
    
    try:
        with open("data/locations.json", "r") as f:
            locations = json.load(f)
    except Exception as e:
        print(f"Error loading locations: {e}")
        return {}
    
    action = state["current_action"].lower()
    current_loc = state["current_location"]
    
    target_location = None
    for loc_key, loc_data in locations.items():
        if loc_key in action or loc_data["name"].lower() in action:
            if current_loc in locations and loc_key in locations[current_loc].get("connections", []):
                target_location = loc_key
                break
            elif current_loc == loc_key:
                return {
                    "last_output": f"You're already at {loc_data['name']}."
                }
    
    if target_location:
        loc_data = locations[target_location]
        description = loc_data["description"]
        actions = "\n".join([f"- {a}" for a in loc_data.get("available_actions", [])])
        
        narrative = f"You travel to {loc_data['name']}.\n\n{description}\n\nWhat would you like to do?\n{actions}"
        
        return {
            "current_location": target_location,
            "last_output": narrative
        }
    else:
        return {
            "last_output": "You can't go there from here."
        }


def state_update_node(state: GameState) -> Dict:
    print("[Node: State Update]")
    
    new_turn = state["turn_count"] + 1
    
    health = min(state["health"], state["max_health"])
    health = max(0, health)
    
    gold = max(0, state["gold"])
    
    return {
        "turn_count": new_turn,
        "health": health,
        "gold": gold
    }


def inventory_node(state: GameState) -> Dict:
    print("[Node: Inventory]")
    
    action = state["current_action"].lower()
    
    if any(word in action for word in ["rest", "heal", "sleep", "recover"]):
        if state["current_location"] == "tavern":
            if state["health"] < state["max_health"]:
                health_restored = state["max_health"] - state["health"]
                return {
                    "health": state["max_health"],
                    "last_output": f"You rest at the tavern and recover {health_restored} health. You feel refreshed! (Health: {state['max_health']}/{state['max_health']})"
                }
            else:
                return {
                    "last_output": "You're already at full health!"
                }
        else:
            return {
                "last_output": "You can only rest and recover at the tavern."
            }
    
    give_keywords = ["give", "tip", "donate", "pay", "offer", "here's", "here is", "take", "have"]
    if any(word in action for word in give_keywords):
        receiving_patterns = [
            "give me", "gives me", "gave me",
            "take from", "taken from", "get from",
            "receive from", "borrow from"
        ]
        
        is_trying_to_receive = any(pattern in action for pattern in receiving_patterns)
        
        import re
        gold_match = re.search(r'(\d+)\s*(gold|coin|money|g\b)', action)
        
        if gold_match:
            amount = int(gold_match.group(1))
            
            if is_trying_to_receive:
                return {
                    "last_output": (
                        f"You can't just take gold from NPCs! 💰\n\n"
                        f"To get gold, try:\n"
                        f"- Complete quests and get rewards\n"
                        f"- Win combat encounters\n"
                        f"- Sell items to merchants (not implemented yet)\n\n"
                        f"Current gold: {state['gold']}"
                    )
                }
            
            if amount > state["gold"]:
                return {
                    "last_output": f"You don't have {amount} gold. You only have {state['gold']} gold."
                }
            
            new_gold = state["gold"] - amount
            
            recipient = None
            if "keeper" in action or "marta" in action:
                recipient = "Marta the Tavern Keeper"
            elif "guard" in action or "borin" in action:
                recipient = "Captain Borin"
            elif "merchant" in action or "tobias" in action:
                recipient = "Tobias the Merchant"
            elif "guardian" in action or "elara" in action:
                recipient = "Elara Moonwhisper"
            else:
                try:
                    import json
                    with open("data/npcs.json", "r") as f:
                        npc_data = json.load(f)
                    
                    for key, npc in npc_data.items():
                        if npc.get("location") == state["current_location"]:
                            recipient = npc["name"]
                            break
                except:
                    pass
            
            if not recipient:
                recipient = "someone"
            
            return {
                "gold": new_gold,
                "last_output": f"You give {amount} gold to {recipient}. You now have {new_gold} gold remaining."
            }
        
        for item in state["inventory"]:
            if item.lower() in action or item.replace("_", " ") in action:
                new_inventory = state["inventory"].copy()
                new_inventory.remove(item)
                return {
                    "inventory": new_inventory,
                    "last_output": f"You give {item} away. It's no longer in your inventory."
                }
        
        return {
            "last_output": "What do you want to give? Specify an item from your inventory or an amount of gold (e.g., 'give 5 gold')."
        }
    
    if "drop" in action:
        import re
        gold_match = re.search(r'(\d+)\s*(gold|coin)', action)
        
        if gold_match:
            amount = int(gold_match.group(1))
            if amount > state["gold"]:
                return {
                    "last_output": f"You don't have {amount} gold to drop."
                }
            new_gold = state["gold"] - amount
            return {
                "gold": new_gold,
                "last_output": f"You drop {amount} gold on the ground. You now have {new_gold} gold."
            }
        
        for item in state["inventory"]:
            if item.lower() in action or item.replace("_", " ") in action:
                new_inventory = state["inventory"].copy()
                new_inventory.remove(item)
                return {
                    "inventory": new_inventory,
                    "last_output": f"You drop {item} on the ground."
                }
    
    if "use" in action or "drink" in action or "eat" in action:
        item_to_use = None
        for item in state["inventory"]:
            if item.lower() in action or item.replace("_", " ") in action:
                item_to_use = item
                break
        
        if item_to_use:
            result = use_item(state["inventory"], item_to_use)
            
            updates = {
                "last_output": result.message
            }
            
            if result.success and result.effects:
                if "health" in result.effects:
                    new_health = min(state["health"] + result.effects["health"], state["max_health"])
                    updates["health"] = new_health
                    updates["last_output"] += f"\nYou recovered {result.effects['health']} health! (Health: {new_health}/{state['max_health']})"
            
            return updates
    
    elif "inventory" in action or "check items" in action:
        items_list = "\n".join([f"- {item}" for item in state["inventory"]])
        return {
            "last_output": f"Your inventory:\n{items_list}\n\nGold: {state['gold']}"
        }
    
    return {}
