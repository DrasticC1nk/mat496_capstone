
from langgraph.graph import StateGraph, END
from src.game_state import GameState
from src.graph.nodes import (
    story_generator_node,
    npc_interaction_node,
    combat_node,
    location_change_node,
    state_update_node,
    inventory_node
)
from src.graph.edges import route_action, should_continue


def create_game_graph():
    workflow = StateGraph(GameState)
    
    workflow.add_node("story_generator", story_generator_node)
    workflow.add_node("npc_interaction", npc_interaction_node)
    workflow.add_node("combat", combat_node)
    workflow.add_node("location_change", location_change_node)
    workflow.add_node("inventory", inventory_node)
    workflow.add_node("state_update", state_update_node)
    
    workflow.set_conditional_entry_point(
        route_action,
        {
            "story_generator": "story_generator",
            "npc_interaction": "npc_interaction",
            "combat": "combat",
            "location_change": "location_change",
            "inventory": "inventory"
        }
    )
    
    workflow.add_edge("story_generator", "state_update")
    workflow.add_edge("npc_interaction", "state_update")
    workflow.add_edge("combat", "state_update")
    workflow.add_edge("location_change", "state_update")
    workflow.add_edge("inventory", "state_update")
    
    workflow.add_edge("state_update", END)
    
    app = workflow.compile()
    
    return app


game_graph = create_game_graph()
