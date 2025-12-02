from typing import List, Tuple, Optional, Dict
from src.game_state import InventoryAction


def add_item(inventory: List[str], item: str, max_size: int = 20) -> InventoryAction:
    if len(inventory) >= max_size:
        return InventoryAction(
            action="add",
            item=item,
            success=False,
            message=f"Inventory full! Cannot add {item}. (Max: {max_size} items)"
        )
    
    inventory.append(item)
    return InventoryAction(
        action="add",
        item=item,
        success=True,
        message=f"Added {item} to inventory."
    )


def remove_item(inventory: List[str], item: str) -> InventoryAction:
    if item not in inventory:
        return InventoryAction(
            action="remove",
            item=item,
            success=False,
            message=f"{item} not in inventory."
        )
    
    inventory.remove(item)
    return InventoryAction(
        action="remove",
        item=item,
        success=True,
        message=f"Removed {item} from inventory."
    )


def check_item(inventory: List[str], item: str) -> bool:
    return item in inventory


def use_item(inventory: List[str], item: str, item_effects: Optional[Dict[str, Dict]] = None) -> InventoryAction:
    if item not in inventory:
        return InventoryAction(
            action="use",
            item=item,
            success=False,
            message=f"You don't have {item}."
        )
    
    default_effects = {
        "health_potion": {"health": 30},
        "mana_potion": {"mana": 20},
        "elixir": {"health": 50, "mana": 30},
    }
    
    if item_effects and item in item_effects:
        effects = item_effects[item].get("effects", {})
        consumable = item_effects[item].get("consumable", True)
    else:
        effects = default_effects.get(item, {})
        consumable = True
    
    if consumable:
        inventory.remove(item)
        message = f"Used {item}."
    else:
        message = f"Activated {item}."
    
    return InventoryAction(
        action="use",
        item=item,
        success=True,
        message=message,
        effects=effects
    )


def equip_item(
    inventory: List[str],
    item: str,
    slot: str,
    currently_equipped: Optional[str]
) -> Tuple[InventoryAction, Optional[str]]:
    if item not in inventory:
        return InventoryAction(
            action="equip",
            item=item,
            success=False,
            message=f"{item} not in inventory."
        ), currently_equipped
    
    if currently_equipped:
        message = f"Unequipped {currently_equipped} and equipped {item}."
    else:
        message = f"Equipped {item}."
    
    return InventoryAction(
        action="equip",
        item=item,
        success=True,
        message=message
    ), item


def list_inventory(inventory: List[str]) -> str:
    if not inventory:
        return "Your inventory is empty."
    
    return "Inventory:\n" + "\n".join(f"  - {item}" for item in inventory)
