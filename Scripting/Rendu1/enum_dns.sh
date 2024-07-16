#!/bin/bash

# Fonction pour l'énumération DNS
enumerate_dns() {
    local domain=$1
    local suppress_output=${2:-false}  # Paramètre optionnel pour supprimer l'affichage
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    NOCOLOR='\033[0m'

    get_domain=$(curl -s "https://crt.sh/?q=$domain&output=json" | jq -r '.[].common_name' | sort -u )

    # Création de listes
    # Initialisation
    valid_domains=()
    invalid_domains=()

    # Boucle avec nslookup
    for domain in $get_domain; do
      if nslookup "$domain" > /dev/null 2>&1; then
        valid_domains+=("$domain")
      else
        invalid_domains+=("$domain")
      fi
    done

    # Afficher le résultat des domaines valides
    echo "Domaines valides:"
    for domain in "${valid_domains[@]}"; do
      echo -e "${GREEN}$domain${NOCOLOR}"
    done

    echo "Domaines invalides:"
    for domain in "${invalid_domains[@]}"; do
      echo -e "${RED}$domain${NOCOLOR}"
    done
}
