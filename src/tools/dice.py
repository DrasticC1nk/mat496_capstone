
import random
from typing import Tuple, List


def roll_dice(sides: int = 6, count: int = 1) -> Tuple[int, List[int]]:
    rolls = [random.randint(1, sides) for _ in range(count)]
    return sum(rolls), rolls


def d20_roll() -> int:
    return random.randint(1, 20)


def skill_check(difficulty: int, modifier: int = 0) -> Tuple[bool, int, str]:
    roll = d20_roll()
    total = roll + modifier
    success = total >= difficulty
    
    if roll == 20:
        desc = "Critical Success! Natural 20!"
    elif roll == 1:
        desc = "Critical Failure! Natural 1!"
    elif success:
        desc = f"Success! ({roll} + {modifier} = {total} vs DC {difficulty})"
    else:
        desc = f"Failure. ({roll} + {modifier} = {total} vs DC {difficulty})"
    
    return success, total, desc


def combat_roll(attacker_level: int, defender_level: int, attacker_advantage: bool = False) -> Tuple[bool, int, int]:
    if attacker_advantage:
        roll1, roll2 = d20_roll(), d20_roll()
        attack_roll = max(roll1, roll2)
    else:
        attack_roll = d20_roll()
    
    attack_total = attack_roll + attacker_level
    defense = 10 + defender_level
    
    hit = attack_total >= defense
    
    if attack_roll == 20:
        damage = roll_dice(6, 2)[0] + attacker_level * 2
    elif hit:
        damage = roll_dice(6, 1)[0] + attacker_level
    else:
        damage = 0
    
    return hit, damage, attack_roll


def random_encounter_check(chance: float = 0.3) -> bool:
    return random.random() < chance


def loot_roll(rarity: str = "common") -> int:
    rarity_multipliers = {
        "common": (1, 10),
        "uncommon": (10, 50),
        "rare": (50, 200),
        "legendary": (200, 1000)
    }
    
    min_gold, max_gold = rarity_multipliers.get(rarity, (1, 10))
    return random.randint(min_gold, max_gold)
