#!/bin/bash

# Inclure le fichier dns_enum.sh contenant la fonction enumerate_dns
source ./enum_dns.sh

# Inclure le fichier hebergement.sh contenant la fonction hebergement 
source ./hebergement.sh

# Fonction pour afficher la bannière ASCII
show_banner() {
    cat << 'EOF'
  
 _______   ________ ________  _______   ___          ___  ___  ________  ________  ___  __    _________  ________  ________  ___       ________      
|\  ___ \ |\  _____\\   __  \|\  ___ \ |\  \        |\  \|\  \|\   __  \|\   ____\|\  \|\  \ |\___   ___\\   __  \|\   __  \|\  \     |\   ____\     
\ \   __/|\ \  \__/\ \  \|\  \ \   __/|\ \  \       \ \  \\\  \ \  \|\  \ \  \___|\ \  \/  /|\|___ \  \_\ \  \|\  \ \  \|\  \ \  \    \ \  \___|_    
 \ \  \_|/_\ \   __\\ \   _  _\ \  \_|/_\ \  \       \ \   __  \ \   __  \ \  \    \ \   ___  \   \ \  \ \ \  \\\  \ \  \\\  \ \  \    \ \_____  \   
  \ \  \_|\ \ \  \_| \ \  \\  \\ \  \_|\ \ \  \       \ \  \ \  \ \  \ \  \ \  \____\ \  \\ \  \   \ \  \ \ \  \\\  \ \  \\\  \ \  \____\|____|\  \  
   \ \_______\ \__\   \ \__\\ _\\ \_______\ \__\       \ \__\ \__\ \__\ \__\ \_______\ \__\\ \__\   \ \__\ \ \_______\ \_______\ \_______\____\_\  \ 
    \|_______|\|__|    \|__|\|__|\|_______|\|__|        \|__|\|__|\|__|\|__|\|_______|\|__| \|__|    \|__|  \|_______|\|_______|\|_______|\_________\
                                                                                                                                         \|_________|                                                                                             
                                                                           
EOF
}

# Afficher les CGU et demander l'acceptation
show_cgu() {
    cat << 'EOF'
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
--------------------------------       EFREI HACKTOOLS              --------------------------------
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------

Conditions Générales d'Utilisation (CGU):
[Insérer ici le texte des CGU]

Appuyez sur :q pour quitter les CGU et revenir au menu des paramètres
EOF

    # Utiliser less pour afficher les CGU avec option de quitter :q
    less -Q
}

# Fonction pour afficher le menu principal
show_menu() {
    clear
    show_banner
    cat << 'EOF'
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
--------------------------------       EFREI HACKTOOLS              --------------------------------
----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------

# Options

0) Settings

1) Enumération DNS                     3) Screenshot du Site
2) Hebergeur du service                4) Scan Massif

/!\ on ne peux pas selectioner les options 1/2/3/4 tant qu'on a pas accepter les CGU 

EOF
}

# Fonction pour afficher le menu des paramètres
show_settings() {
    clear
    show_banner
    echo "----------------------------------------------------------------------------------------------------"
    echo "--------------------------------        Paramètres                     --------------------------------"
    echo "----------------------------------------------------------------------------------------------------"
    echo ""
    echo "1) Single domain or multidomain"
    echo "2) Accepter les CGU"
    echo "3) Domaine à tester"
    echo "4) Retour au menu principal"
    echo ""
}

# Variables de paramètres
cgu_accepted=false
single_or_multi=""
domain_to_test=""

# Gestion des paramètres
settings_menu() {
    while true; do
        show_settings
        read -p "Sélectionnez une option: " option
        case $option in
            1)
                read -p "Entrez 'single' pour un seul domaine ou 'multi' pour plusieurs domaines: " single_or_multi
                ;;
            2)
                show_cgu
                read -p "Acceptez-vous les CGU ? (yes/no): " accept_cgu
                if [[ "$accept_cgu" == "yes" ]]; then
                    cgu_accepted=true
                else
                    cgu_accepted=false
                fi
                ;;
            3)
                read -p "Entrez le domaine à tester: " domain_to_test
                ;;
            4)
                return
                ;;
            *)
                echo "Option invalide, veuillez réessayer."
                ;;
        esac
    done
}

# Fonction pour le scan massif
scan_massif() {
    enumerate_dns "$domain_to_test" true
    for sous_domaine in "${valid_domains[@]}"; do
        echo "Scan en cours pour $sous_domaine ...."
        # Commande pour scanner
        result=$(nmap -p 20-443 -sT -Pn "$sous_domaine" | grep "open" | awk '{print $1}' | paste -sd ',' -)  

        # Afficher le résultat 
        if [ -z "$result" ]; then
            echo "$sous_domaine : Aucun port ouvert."
        else
            echo "$sous_domaine : $result"
        fi
    done
}

# Afficher le menu principal et gérer la sélection des options
while true; do
    show_menu
    read -p "Sélectionnez une option: " option
    case $option in
        0)
            settings_menu
            ;;
        1)
            if [[ "$cgu_accepted" == true ]]; then
                if [[ -z "$domain_to_test" ]]; then
                    echo "Le domaine à tester n'est pas défini. Veuillez le définir dans les paramètres."
		    read -p "Appuyez sur Entrée pour continuer..."
                else
                    enumerate_dns "$domain_to_test"
                    read -p "Appuyez sur Entrée pour continuer..."
                fi
            else
                echo "Vous devez accepter les CGU avant de sélectionner cette option."
                read -p "Appuyez sur Entrée pour continuer..."
	    fi
            ;;
        2)
            if [[ "$cgu_accepted" == true ]]; then
		if [[ -z "$domain_to_test" ]]; then
                    echo "Le domaine à tester n'est pas défini. Veuillez le définir dans les paramètres."
                    read -p "Appuyez sur Entrée pour continuer..."
                else
                    echo "Afficher l'hébergeur du service pour le domaine: $domain_to_test"
                    ./hebergement.sh "$domain_to_test"
                    read -p "Appuyez sur Entrée pour continuer..."
		fi
            else
                echo "Vous devez accepter les CGU avant de sélectionner cette option."
		read -p "Appuyez sur Entrée pour continuer..."
            fi
            ;;
        3)
            if [[ "$cgu_accepted" == true ]]; then
                if [[ -z "$domain_to_test" ]]; then
                    echo "Le domaine à tester n'est pas défini. Veuillez le définir dans les paramètres."
		    read -p "Appuyez sur Entrée pour continuer..."
                else
                    python3 screenshots.py "$domain_to_test"
                    read -p "Appuyez sur Entrée pour continuer..."
                fi
            else
                echo "Vous devez accepter les CGU avant de sélectionner cette option."
		read -p "Appuyez sur Entrée pour continuer..."
            fi
            ;;
        4)
            if [[ "$cgu_accepted" == true ]]; then
                if [[ -z "$domain_to_test" ]]; then
                    echo "Le domaine à tester n'est pas défini. Veuillez le définir dans les paramètres."
                    read -p "Appuyez sur Entrée pour continuer..."
                else
                    scan_massif
                    read -p "Appuyez sur Entrée pour continuer..."
                fi
            else
                echo "Vous devez accepter les CGU avant de sélectionner cette option."
                read -p "Appuyez sur Entrée pour continuer..."
            fi
            ;;
        *)
            echo "Option invalide, veuillez réessayer."
            ;;
    esac
done
