import requests
from config import DEFAULT_API_ENDPOINT

def accept_cgu():
    print("Conditions Générales d'Utilisation (CGU)")
    print("[Insérer ici le texte des CGU]")
    accept = input("Acceptez-vous les CGU ? (yes/no): ")
    return accept.lower() == "yes"

def scan_subdomains(domain: str, endpoint: str = DEFAULT_API_ENDPOINT):
    url = f"{endpoint}/scan_subdomains/"
    response = requests.post(url, json={"domain": domain})
    return response.json()

def take_screenshot(url: str, endpoint: str = DEFAULT_API_ENDPOINT):
    api_url = f"{endpoint}/screenshot/"
    response = requests.post(api_url, json={"url": url})
    return response.json()

def scan_ports(domain: str, endpoint: str = DEFAULT_API_ENDPOINT):
    api_url = f"{endpoint}/scan_ports/"
    response = requests.post(api_url, json={"domain": domain})
    return response.json()

def get_hosting_provider(domain: str, endpoint: str = DEFAULT_API_ENDPOINT):
    api_url = f"{endpoint}/get_provider/"
    response = requests.post(api_url, json={"domain": domain})
    return response.json()
