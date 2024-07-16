import json
from termcolor import colored 
from rich.json import JSON
from rich.console import Console
from rich.table import Table


console = Console()

def generate_report(data, filename: str):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    console.print(f"[green]Rapport enregistré dans {filename}[/]")
    if 'open_ports' in data:
        display_ports_table(data['open_ports'])
    else:
        console.print("[cyan]Contenu du rapport :[/]")  
        console.print(data, style="bold")
        table = Table(title="Rapport de Données")
    #print(colored(f'Rapport enregistré dans {filename}', 'green'))
    #print(colored('Contenu du rapport :', 'cyan'))
    #print(json.dumps(data, indent=4, sort_keys=True))

        if isinstance(data, dict):
            for key in data.keys():
                table.add_column(str(key), style="magenta")
            table.add_row(*[json.dumps(item, ensure_ascii=False) for item in data.values()])
        elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
            keys = data[0].keys()
            for key in keys:
                table.add_column(str(key), style="magenta")
            for item in data:
                table.add_row(*[json.dumps(item[key], ensure_ascii=False) if key in item else "" for key in keys])
    
        console.print(table)

def display_ports_table(ports_data):
    table = Table(title="Rapport des Ports Ouverts")

    # Colonnes
    table.add_column("Port", style="dim", width=12)
    table.add_column("Etat", justify="center")
    table.add_column("Service", justify="right")

    for port, details in ports_data.items():
        table.add_row(port, details['state'], details['service'])
    
    console.print(table)

