# templates/page1/functions/scan_wifi.py
import subprocess
import re


def scan_wifi(interface_name):
    """
    Scanne les réseaux Wi-Fi disponibles en utilisant une interface Wi-Fi spécifique.

    Args:
        interface_name (str): Le nom de l'interface Wi-Fi à utiliser pour le scan.

    Returns:
        list of dict: Une liste de dictionnaires contenant les informations des réseaux Wi-Fi détectés.
    """
    try:
        # Effectuer le scan
        scan_command = ["netsh", "wlan", "show", "networks", "mode=Bssid", f"interface={interface_name}"]
        scan_output = subprocess.check_output(scan_command, encoding='utf-8', errors="ignore")

        networks = []
        current_network = {}

        for line in scan_output.split('\n'):
            line = line.strip()
            if line.startswith("SSID "):
                if current_network:
                    networks.append(current_network)
                    current_network = {}
                ssid_match = re.match(r'SSID \d+ : (.+)', line)
                if ssid_match:
                    current_network['SSID'] = ssid_match.group(1)
            elif line.startswith("BSSID "):
                bssid_match = re.match(r'BSSID \d+ : (.+)', line)
                if bssid_match:
                    current_network['BSSID'] = bssid_match.group(1)
            elif line.startswith("Signal"):
                signal_match = re.match(r'Signal : (\d+)%', line)
                if signal_match:
                    current_network['Signal'] = int(signal_match.group(1))
            elif line.startswith("Authentication"):
                auth_match = re.match(r'Authentication : (.+)', line)
                if auth_match:
                    current_network['Authentication'] = auth_match.group(1)
            elif line.startswith("Cipher"):
                cipher_match = re.match(r'Cipher : (.+)', line)
                if cipher_match:
                    current_network['Cipher'] = cipher_match.group(1)

        if current_network:
            networks.append(current_network)

        return networks
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du scan Wi-Fi: {e}")
        return []
