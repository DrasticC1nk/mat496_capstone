
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.game_engine import GameEngine
from src.utils.display import *


def show_main_menu(engine: GameEngine):
    clear_screen()
    print_banner()
    
    options = [
        "New Game",
        "Continue Last Save",
        "Load Game",
        "Exit"
    ]
    
    print_menu(options)
    
    choice = input(f"{Fore.CYAN}Choose an option (1-{len(options)}): {Style.RESET_ALL}").strip()
    
    if choice == "1":
        start_new_game(engine)
    elif choice == "2":
        continue_game(engine)
    elif choice == "3":
        load_game_menu(engine)
    elif choice == "4":
        print_info("Thanks for playing! Goodbye!")
        sys.exit(0)
    else:
        print_error("Invalid choice. Please try again.")
        input("Press Enter to continue...")
        show_main_menu(engine)


def start_new_game(engine: GameEngine):
    print_header("New Game")
    
    player_name = input(f"{Fore.CYAN}Enter your character's name: {Style.RESET_ALL}").strip()
    
    if not player_name:
        player_name = "Adventurer"
    
    state = engine.new_game(player_name)
    game_loop(engine)


def continue_game(engine: GameEngine):
    from src.persistence.save_manager import get_last_save
    
    last_save = get_last_save()
    
    if last_save:
        try:
            engine.load_saved_game(last_save)
            game_loop(engine)
        except Exception as e:
            print_error(f"Failed to load save: {e}")
            input("Press Enter to return to main menu...")
            show_main_menu(engine)
    else:
        print_error("No saved games found.")
        input("Press Enter to return to main menu...")
        show_main_menu(engine)


def load_game_menu(engine: GameEngine):
    print_header("Load Game")
    
    saves = engine.list_available_saves()
    
    if not saves:
        print_error("No saved games found.")
        input("Press Enter to return to main menu...")
        show_main_menu(engine)
        return
    
    print(f"{Fore.CYAN}Available saves:{Style.RESET_ALL}\n")
    for i, save in enumerate(saves, 1):
        print(f"  {i}. {save['player_name']} - Level {save['level']} - {save['location']}")
        print(f"     {Fore.YELLOW}Saved: {save['last_save_time']}{Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.CYAN}Select a save (1-{len(saves)}) or 'b' to go back: {Style.RESET_ALL}").strip()
    
    if choice.lower() == 'b':
        show_main_menu(engine)
        return
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(saves):
            engine.load_saved_game(saves[index]['filename'])
            game_loop(engine)
        else:
            print_error("Invalid selection.")
            input("Press Enter to try again...")
            load_game_menu(engine)
    except ValueError:
        print_error("Invalid input.")
        input("Press Enter to try again...")
        load_game_menu(engine)


def game_loop(engine: GameEngine):
    
    while True:
        state = engine.get_state()
        
        if state is None:
            print_error("Game state lost. Returning to main menu.")
            break
        
        if engine.is_game_over():
            print_combat("GAME OVER")
            print_narrative("You have fallen in battle. Your adventure ends here...")
            input("\nPress Enter to return to main menu...")
            show_main_menu(engine)
            return
        
        print_status_bar(state)
        
        if state["last_output"]:
            print_narrative(state["last_output"])
        
        print(f"{Fore.MAGENTA}Commands: 'save' to save, 'quit' to return to menu, 'help' for help{Style.RESET_ALL}")
        action = input(f"\n{Fore.GREEN}> {Style.RESET_ALL}").strip()
        
        if not action:
            print_error("Please enter an action.")
            continue
        
        if action.lower() == "save":
            engine.save_current_game()
            input("Press Enter to continue...")
            continue
        
        elif action.lower() == "quit":
            print_info("Returning to main menu...")
            show_main_menu(engine)
            return
        
        elif action.lower() == "help":
            show_help()
            continue
        
        elif action.lower() in ["status", "stats"]:
            show_detailed_status(state)
            continue
        
        print_info("\nProcessing...")
        try:
            result = engine.process_action(action)
        except Exception as e:
            print_error(f"Error: {e}")
            input("Press Enter to continue...")


def show_help():
    print_header("Game Help")
    
    help_text = """
    HOW TO PLAY:
    
    This is a text-based RPG. Type what you want to do, and the game will respond.
    
    EXAMPLE ACTIONS:
    - "Talk to the tavern keeper"
    - "Go to the dark forest"
    - "Attack the bandit"
    - "Use health potion"
    - "Check inventory"
    - "Look around"
    
    SPECIAL COMMANDS:
    - save: Save your game
    - quit: Return to main menu
    - help: Show this help
    - status: Show detailed character status
    
    TIPS:
    - Pay attention to NPC dialogue for quest hints
    - Manage your health with potions
    - Explore different locations
    - Combat uses dice rolls, so strategy and luck both matter
    """
    
    print(help_text)
    input("\nPress Enter to continue...")


def show_detailed_status(state: dict):
    print_header("Character Status")
    
    print(f"{Fore.CYAN}Name:{Style.RESET_ALL} {state.get('player_name', 'Unknown')}")
    print(f"{Fore.CYAN}Level:{Style.RESET_ALL} {state.get('level', 1)}")
    print(f"{Fore.CYAN}Experience:{Style.RESET_ALL} {state.get('experience', 0)}")
    print(f"{Fore.CYAN}Health:{Style.RESET_ALL} {state.get('health', 0)}/{state.get('max_health', 100)}")
    print(f"{Fore.CYAN}Gold:{Style.RESET_ALL} {state.get('gold', 0)}")
    print(f"{Fore.CYAN}Location:{Style.RESET_ALL} {state.get('current_location', 'Unknown')}")
    
    print(f"\n{Fore.YELLOW}Inventory:{Style.RESET_ALL}")
    inventory = state.get('inventory', [])
    if inventory:
        for item in inventory:
            print(f"  - {item}")
    else:
        print("  (empty)")
    
    print(f"\n{Fore.YELLOW}Active Quests:{Style.RESET_ALL}")
    quests = state.get('quest_log', [])
    if quests:
        for quest in quests:
            status = quest.get('status', 'unknown')
            print(f"  - {quest.get('name', 'Unknown Quest')} [{status}]")
    else:
        print("  No active quests")
    
    input("\nPress Enter to continue...")


def main():
    try:
        engine = GameEngine()
        
        engine.initialize_rag_system()
        
        show_main_menu(engine)
    
    except KeyboardInterrupt:
        print_info("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print_error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
