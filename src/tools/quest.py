
from typing import Dict, List, Optional
from src.game_state import QuestUpdate


def create_quest(
    quest_id: str,
    quest_name: str,
    description: str,
    objectives: List[str],
    rewards: Optional[Dict[str, int]] = None
) -> Dict:
    return {
        "id": quest_id,
        "name": quest_name,
        "description": description,
        "objectives": objectives,
        "objectives_completed": [],
        "status": "started",
        "rewards": rewards or {"gold": 0, "experience": 0}
    }


def start_quest(quest_log: List[Dict], quest_data: Dict) -> QuestUpdate:
    quest_log.append(quest_data)
    
    return QuestUpdate(
        quest_id=quest_data["id"],
        quest_name=quest_data["name"],
        status="started",
        objectives_remaining=quest_data["objectives"],
        narrative=f"New quest accepted: {quest_data['name']}!\n{quest_data['description']}"
    )


def update_quest_progress(
    quest_log: List[Dict],
    quest_id: str,
    objective: str
) -> Optional[QuestUpdate]:
    for quest in quest_log:
        if quest["id"] == quest_id:
            if objective in quest["objectives"] and objective not in quest["objectives_completed"]:
                quest["objectives_completed"].append(objective)
                
                all_complete = set(quest["objectives_completed"]) == set(quest["objectives"])
                
                if all_complete:
                    quest["status"] = "completed"
                    return QuestUpdate(
                        quest_id=quest_id,
                        quest_name=quest["name"],
                        status="completed",
                        objectives_completed=quest["objectives_completed"],
                        objectives_remaining=[],
                        rewards=quest["rewards"],
                        narrative=f"Quest Completed: {quest['name']}!"
                    )
                else:
                    remaining = [obj for obj in quest["objectives"] if obj not in quest["objectives_completed"]]
                    return QuestUpdate(
                        quest_id=quest_id,
                        quest_name=quest["name"],
                        status="in_progress",
                        objectives_completed=quest["objectives_completed"],
                        objectives_remaining=remaining,
                        narrative=f"Quest objective completed: {objective}"
                    )
    
    return None


def check_quest_completion(quest: Dict) -> bool:
    return set(quest["objectives_completed"]) == set(quest["objectives"])


def get_active_quests(quest_log: List[Dict]) -> List[Dict]:
    return [q for q in quest_log if q["status"] != "completed"]


def format_quest_log(quest_log: List[Dict]) -> str:
    if not quest_log:
        return "No active quests."
    
    output = "Quest Log:\n"
    for quest in quest_log:
        output += f"\n[{quest['status'].upper()}] {quest['name']}\n"
        output += f"  {quest['description']}\n"
        output += "  Objectives:\n"
        for obj in quest["objectives"]:
            status = "✓" if obj in quest["objectives_completed"] else "○"
            output += f"    {status} {obj}\n"
    
    return output
