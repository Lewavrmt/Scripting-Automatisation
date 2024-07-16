import requests
import socket

def dns_check(domain: str):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False
    
def get_subdomains(domain: str):
    url = f"https://crt.sh/?q={domain}&output=json"
    response = requests.get(url)
    return {entry['common_name'] for entry in response.json()} if response.status_code == 200 else set()

def is_blacklisted(domain: str):
    with open("Blacklist.txt", "r") as file:
        blacklisted_domains = {line.strip() for line in file.readlines()}
    return domain in blacklisted_domains
