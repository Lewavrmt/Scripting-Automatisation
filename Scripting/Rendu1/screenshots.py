import sys
import requests
import socket
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import platform

def get_subdomains(domain):
    url = f"https://crt.sh/?q={domain}&output=json"
    response = requests.get(url)
    if response.status_code == 200:
       data = response.json()
       return {entry['common_name'] for entry in data}
    return set()

def get_hosting_provider(ip):
    url = f"https://ipinfo.io/{ip}"
    response = requests.get(url)
    if response.status_code == 200:
       data = response.json()
       return data.get('org', '').split(' ')[1:]
    return "Erreur"

def screenshot(url, output_dir):
    options = Options()
    options.add_argument("--headless=new")
    if platform.system() == "Windows":
        # Chemin à vérifier
        chromedriver_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe'
    else:
        chromedriver_path = '/usr/local/bin/chromedriver'

    service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        filename = url.replace("https://", "").replace("/", "_") + ".png"
        filepath = os.path.join(output_dir, filename)
        driver.save_screenshot(filepath)
        print(f"Capture d'écran enregistrée : {filepath}")
    except Exception as e:
        print(f"Erreur lors de la capture d'ecran de {url} : {e}")
    finally:
        driver.quit()

def main(domain):
    subdomains = get_subdomains(domain)
    results = []
    for subdomain in subdomains:
        try:
            ip = socket.gethostbyname(subdomain)
            provider = ' '.join(get_hosting_provider(ip)) or "NC"
            results.append({"Sous-domaine": subdomain, "@IP": ip, "Hébergeur": provider})
        except socket.gaierror:
            results.append({"Sous-domaine": subdomain, "@IP": "Erreur de résolution DNS", "Hébergeur": ""})
    output_dir = "screenshots"
    os.makedirs(output_dir, exist_ok=True)

    for entry in results:
        subdomain = entry["Sous-domaine"]
        if entry['@IP'] != "Erreur de résolution DNS":
            url = f"https://{subdomain}"
            screenshot(url, output_dir)
    return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python screenshots.py <domain>")
        sys.exit(1)
    
    domain = sys.argv[1]
    hosting_info = main(domain)

    print("\nSous-domaine\tAdresse IP\t\tHébergeur")
    print("-" * 50)
    for entry in hosting_info:
        print(f"{entry['Sous-domaine']}\t{entry['@IP']}\t{entry['Hébergeur']}")
