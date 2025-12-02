

WORLD_LORE = {
    "kingdom_history": {
        "title": "The Kingdom of Ironhold",
        "content": """The Kingdom of Ironhold has stood for three centuries, founded by King Aldric the Brave after he united the warring clans. The kingdom is known for its strong martial tradition and the legendary Iron Keep, a castle that has never fallen to siege. The current ruler, Lord Harmond, maintains peace through a network of loyal guards and just laws.""",
        "tags": ["history", "kingdom", "politics"]
    },
    
    "dark_forest_mystery": {
        "title": "The Dark Forest's Secret",
        "content": """The Dark Forest is said to be older than the kingdom itself. Ancient elves guard its depths, protecting secrets lost to time. Travelers speak of strange lights, mysterious voices, and ruins of a civilization that predates human memory. The forest has a will of its own, they say, allowing passage only to those it deems worthy.""",
        "tags": ["location", "mystery", "elves", "ancient"]
    },
    
    "dragon_legend": {
        "title": "The Red Dragon",
        "content": """Twenty years ago, a great red dragon terrorized the kingdom, burning villages and hoarding treasure. A band of heroes confronted it in its mountain lair. The battle was fierce, and though the dragon fell, only one member of that party survived: Marta, who now runs the Red Dragon Tavern, named in memory of her fallen friends and their greatest battle.""",
        "tags": ["history", "dragon", "marta", "tragedy"]
    },
    
    "bandit_problem": {
        "title": "The Rise of Banditry",
        "content": """In recent months, bandit activity has increased dramatically in the Dark Forest. Led by a ruthless figure known as Grimjaw, these outlaws prey on travelers and have even raided the town. The captain of the guard has offered bounties for bandit leaders, but few have dared to venture into the forest to claim them.""",
        "tags": ["current_events", "bandits", "danger"]
    },
    
    "elven_guardians": {
        "title": "Guardians of the Ancient Woods",
        "content": """The elves of the Dark Forest are reclusive and long-lived. They view themselves as stewards of nature and ancient knowledge. Elara Moonwhisper, one of the eldest, has guarded the forest for over 500 years. She rarely speaks to humans, but those who earn her respect gain a powerful ally.""",
        "tags": ["elves", "forest", "ancient", "guardian"]
    }
}

LOCATION_LORE = {
    "tavern_extended": {
        "title": "The Red Dragon Tavern - A Haven for Adventurers",
        "content": """The Red Dragon Tavern sits at the crossroads between the town and the Dark Forest. Its warm hearth and strong ale make it a favorite gathering spot for adventurers, merchants, and locals alike. Marta keeps a quest board updated with opportunities for brave souls. The walls are decorated with trophies from her adventuring days, including a massive dragon scale mounted above the fireplace.""",
        "tags": ["location", "tavern", "social_hub"]
    },
    
    "forest_dangers": {
        "title": "Dangers of the Dark Forest",
        "content": """The Dark Forest is home to more than bandits. Travelers report sightings of dire wolves, giant spiders, and stranger things that lurk in the shadows. The mist that clings to the ground is said to disorient travelers, leading them in circles. Only those with a guide or exceptional woodcraft can navigate safely.""",
        "tags": ["location", "forest", "danger", "creatures"]
    },
    
    "castle_description": {
        "title": "Ironhold Castle - Seat of Power",
        "content": """Ironhold Castle dominates the skyline, its thick walls and towers a testament to military engineering. The castle houses the lord's court, barracks for the guard, and a marketplace for quality goods. Captain Borin oversees security with an iron fist, ensuring that only those with legitimate business enter the inner keep.""",
        "tags": ["location", "castle", "military", "politics"]
    }
}

NPC_LORE = {
    "marta_past": {
        "title": "Marta's Adventuring Days",
        "content": """Before becoming a tavern keeper, Marta adventured with a legendary party: Ser Gareth the Paladin, Lyssa the Mage, Torvin the Dwarf, and Kael the Rogue. Together they cleared dungeons, saved villages, and finally faced the Red Dragon. Only Marta survived, saved by Ser Gareth's sacrifice. She carries the weight of their memory in every story she tells.""",
        "tags": ["npc", "marta", "backstory", "tragedy"]
    },
    
    "elara_wisdom": {
        "title": "Elara Moonwhisper's Knowledge",
        "content": """Elara has witnessed the rise and fall of kingdoms, the coming of the dragon, and countless smaller dramas of human and elven life. She knows the location of ancient ruins, the properties of rare herbs, and secrets of magic long forgotten. But she shares her knowledge sparingly, only with those who prove their respect for nature and wisdom.""",
        "tags": ["npc", "elara", "magic", "knowledge"]
    },
    
    "borin_loyalty": {
        "title": "Captain Borin's Service",
        "content": """Captain Borin joined the guard as a young soldier and fought in the Dragon War. He lost many friends but earned his rank through courage and tactical brilliance. He's utterly loyal to Lord Harmond and the kingdom, but he also has a personal code of honor that sometimes puts him at odds with courtly politics.""",
        "tags": ["npc", "borin", "military", "honor"]
    }
}

ITEM_LORE = {
    "amulet_significance": {
        "title": "The Dragon Amulet's History",
        "content": """Marta's amulet was gifted to her party by Lord Harmond's father after they saved his life from assassins. Each member of the party received a token, but Marta's amulet is the only one that survived the dragon battle. It bears an enchantment of protection, though Marta never speaks of it. To her, its sentimental value far exceeds any magical power.""",
        "tags": ["item", "amulet", "magic", "history"]
    },
    
    "moonleaf_properties": {
        "title": "Moonleaf Herb and Its Uses",
        "content": """Moonleaf grows only in places where elven magic is strong. It glows faintly under moonlight and has potent healing properties. Alchemists prize it for creating powerful potions, but the elves consider it sacred. Harvesting it without permission from the forest guardian is said to bring a curse.""",
        "tags": ["item", "herb", "magic", "elven"]
    }
}

def get_all_lore_documents():
    documents = []
    
    for key, lore in WORLD_LORE.items():
        documents.append({
            "id": f"world_{key}",
            "content": lore["content"],
            "metadata": {
                "title": lore["title"],
                "tags": lore["tags"],
                "category": "world_lore"
            }
        })
    
    for key, lore in LOCATION_LORE.items():
        documents.append({
            "id": f"location_{key}",
            "content": lore["content"],
            "metadata": {
                "title": lore["title"],
                "tags": lore["tags"],
                "category": "location_lore"
            }
        })
    
    for key, lore in NPC_LORE.items():
        documents.append({
            "id": f"npc_{key}",
            "content": lore["content"],
            "metadata": {
                "title": lore["title"],
                "tags": lore["tags"],
                "category": "npc_lore"
            }
        })
    
    for key, lore in ITEM_LORE.items():
        documents.append({
            "id": f"item_{key}",
            "content": lore["content"],
            "metadata": {
                "title": lore["title"],
                "tags": lore["tags"],
                "category": "item_lore"
            }
        })
    
    return documents
