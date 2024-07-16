#!/bin/bash


# boucler sur chaque sous domaine à la recherche d'une @ip
# apt search bind9-utils
# détecter l'herbergeur à partir de l'AS de l'ip (ipinfo.io)

# Afiche le résultat à l'utilisateur 

main_domain=$1

subdomains=$(curl -s "https://crt.sh/?q=${main_domain}&output=json" | jq -r '.[].common_name' | sort -u )


for subdomain in $subdomains; do
    ip=$(dig +short $subdomain | tail -n1)

    if [ -z "$ip" ]; then
        #echo " Aucune @IP trouvé pour $subdomain"
        continue
    fi

    # Api ipinfo 
    org_info=$(curl -s "https://ipinfo.io/${ip}" | jq -r '.org' | sed 's/AS[0-9]* //')
    
    echo "$subdomain est herbergé par : $org_info"
done
    

