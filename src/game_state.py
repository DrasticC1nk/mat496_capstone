
from typing import TypedDict, List, Dict, Optional, Literal, Any
from pydantic import BaseModel, Field
from datetime import datetime


class GameState(TypedDict):
    player_name: str
    current_location: str
    health: int
    max_health: int
    gold: int
    level: int
    experience: int
    
    inventory: List[str]
    equipped_weapon: Optional[str]
    equipped_armor: Optional[str]
    
    quest_log: List[Dict]
    completed_quests: List[str]
    
    npc_relationships: Dict[str, int]
    
    conversation_history: List[Dict]
    world_events: List[str]
    game_flags: Dict[str, bool]
    
    current_action: str
    last_output: str
    
    turn_count: int
    last_save_time: Optional[str]


class InventoryAction(BaseModel):
    action: Literal["add", "remove", "use", "equip", "unequip"]
    item: str
    quantity: int = 1
    success: bool
    message: str
    effects: Optional[Dict[str, int]] = None


class LocationChange(BaseModel):
    from_location: str
    to_location: str
    success: bool
    description: str
    encounters: List[str] = Field(default_factory=list)
    available_actions: List[str] = Field(default_factory=list)


class NPCDialogue(BaseModel):
    npc_name: str
    dialogue: str
    relationship_change: int = 0
    quest_offered: Optional[str] = None
    items_given: List[str] = Field(default_factory=list)
    information_revealed: List[str] = Field(default_factory=list)


class CombatAction(BaseModel):
    enemy_name: str
    player_damage_dealt: int
    player_damage_taken: int
    player_hit: bool
    enemy_hit: bool
    combat_over: bool
    victory: bool
    narrative: str
    rewards: Optional[Dict[str, int]] = None
    loot: List[str] = Field(default_factory=list)


class QuestUpdate(BaseModel):
    quest_id: str
    quest_name: str
    status: Literal["started", "in_progress", "completed", "failed"]
    objectives_completed: List[str] = Field(default_factory=list)
    objectives_remaining: List[str] = Field(default_factory=list)
    rewards: Optional[Dict[str, int]] = None
    narrative: str


class GameEvent(BaseModel):
    event_type: Literal["combat", "dialogue", "discovery", "quest", "travel", "trade"]
    description: str
    state_changes: Dict[str, Any] = Field(default_factory=dict)
    flags_set: Dict[str, bool] = Field(default_factory=dict)


class StoryOutput(BaseModel):
    narrative: str
    suggested_actions: List[str] = Field(default_factory=list)
    context_used: List[str] = Field(default_factory=list)
    tone: Literal["dramatic", "mysterious", "casual", "combat", "peaceful"] = "casual"


def create_initial_state(player_name: str) -> GameState:
    from src.config import STARTING_HEALTH, STARTING_GOLD
    
    return GameState(
        player_name=player_name,
        current_location="tavern",
        health=STARTING_HEALTH,
        max_health=STARTING_HEALTH,
        gold=STARTING_GOLD,
        level=1,
        experience=0,
        inventory=["rusty_sword", "health_potion"],
        equipped_weapon="rusty_sword",
        equipped_armor=None,
        quest_log=[],
        completed_quests=[],
        npc_relationships={},
        conversation_history=[],
        world_events=[],
        game_flags={},
        current_action="",
        last_output="",
        turn_count=0,
        last_save_time=None
    )


def validate_state(state: GameState) -> bool:
    try:
        if state["health"] < 0:
            state["health"] = 0
        if state["health"] > state["max_health"]:
            state["health"] = state["max_health"]
        
        if state["gold"] < 0:
            state["gold"] = 0
        
        if state["level"] < 1:
            state["level"] = 1
        
        return True
    except Exception as e:
        print(f"State validation error: {e}")
        return False
