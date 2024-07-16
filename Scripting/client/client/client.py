import os
from config import DEFAULT_API_ENDPOINT
from utils import validate_url, validate_domain
from api import accept_cgu, scan_subdomains, take_screenshot, scan_ports, get_hosting_provider
from report import generate_report
import pyfiglet
from colorama import Fore, Back, Style, init

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_rainbow_text(text):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    figlet_text = pyfiglet.figlet_format(text, font="slant")  
    lines = figlet_text.split('\n')

    for line in lines:
        colored_line = ''
        for i, char in enumerate(line):
            if char != ' ':
                colored_line += colors[i % len(colors)] + char
            else:
                colored_line += char
        print(colored_line)



def display_menu():
    clear_screen()
    print_rainbow_text("EFREI-SECLAB")
    print("""
Menu :
1) Énumération DNS
2) Analyse de ports
3) Capture d'écran Web
4) Informations sur l'hébergeur
5) Paramètres
0) Quitter
    """)

def get_user_choice():
    try:
        choice = int(input("Sélectionnez une option : "))
        if 0 <= choice <= 5:
            return choice
        else:
            print("Option invalide. Veuillez choisir entre 0 et 5.")
    except ValueError:
        print("Veuillez entrer un nombre valide.")
    return None

def main():
    clear_screen()
    if not accept_cgu():
        print("Vous devez accepter les CGU pour utiliser cet outil.")
        return

    endpoint = DEFAULT_API_ENDPOINT
    
    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 0:
            print("Au revoir !")
            break
        
        elif choice == 1:
            domain = input("Entrez le domaine à tester : ")
            if validate_domain(domain):
                result = scan_subdomains(domain, endpoint)
                generate_report(result, "subdomains_report.json")
            else:
                print("Domaine invalide.")

        elif choice == 2:
            domain = input("Entrez le domaine à tester : ")
            if validate_domain(domain):
                result = scan_ports(domain, endpoint)
                generate_report(result, "ports_report.json")
            else:
                print("Domaine invalide.")

        elif choice == 3:
            url = input("Entrez l'URL à capturer : ")
            if validate_url(url):
                result = take_screenshot(url, endpoint)
                generate_report(result, "screenshot_report.json")
            else:
                print("URL invalide.")

        elif choice == 4:
            domain = input("Entrez le domaine à tester : ")
            if validate_domain(domain):
                result = get_hosting_provider(domain, endpoint)
                generate_report(result, "hosting_provider_report.json")
            else:
                print("Domaine invalide.")

        elif choice == 5:
            endpoint = input(f"Entrez le nouvel endpoint de l'API (actuel : {endpoint}) : ") or endpoint

        input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
