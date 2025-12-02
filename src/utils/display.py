
from colorama import Fore, Style, init

init(autoreset=True)


def print_header(text: str):
    print("\n" + "=" * 60)
    print(f"{Fore.CYAN}{Style.BRIGHT}{text.center(60)}{Style.RESET_ALL}")
    print("=" * 60 + "\n")


def print_narrative(text: str):
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}\n")


def print_dialogue(speaker: str, text: str):
    print(f"{Fore.YELLOW}{Style.BRIGHT}{speaker}:{Style.RESET_ALL} {Fore.YELLOW}\"{text}\"{Style.RESET_ALL}\n")


def print_combat(text: str):
    print(f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}\n")


def print_success(text: str):
    print(f"{Fore.GREEN}{Style.BRIGHT}✓ {text}{Style.RESET_ALL}\n")


def print_error(text: str):
    print(f"{Fore.RED}{Style.BRIGHT}✗ {text}{Style.RESET_ALL}\n")


def print_info(text: str):
    print(f"{Fore.CYAN}{text}{Style.RESET_ALL}\n")


def print_status_bar(state: dict):
    health = state.get("health", 0)
    max_health = state.get("max_health", 100)
    gold = state.get("gold", 0)
    location = state.get("current_location", "Unknown")
    level = state.get("level", 1)
    
    health_percent = health / max_health if max_health > 0 else 0
    bar_length = 20
    filled = int(bar_length * health_percent)
    health_bar = "█" * filled + "░" * (bar_length - filled)
    
    if health_percent > 0.6:
        health_color = Fore.GREEN
    elif health_percent > 0.3:
        health_color = Fore.YELLOW
    else:
        health_color = Fore.RED
    
    print("\n" + "─" * 60)
    print(f"{Fore.CYAN}Location:{Style.RESET_ALL} {location.replace('_', ' ').title()}  |  " + 
          f"{Fore.YELLOW}Level:{Style.RESET_ALL} {level}  |  " +
          f"{Fore.YELLOW}Gold:{Style.RESET_ALL} {gold}")
    print(f"{Fore.RED}Health:{Style.RESET_ALL} {health_color}{health_bar}{Style.RESET_ALL} {health}/{max_health}")
    print("─" * 60 + "\n")


def print_menu(options: list):
    print()
    for i, option in enumerate(options, 1):
        print(f"  {Fore.CYAN}{i}.{Style.RESET_ALL} {option}")
    print()


def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║          MEDIEVAL FANTASY RPG                            ║
    ║          Powered by LangGraph & LLMs                     ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(Fore.MAGENTA + Style.BRIGHT + banner + Style.RESET_ALL)


def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
