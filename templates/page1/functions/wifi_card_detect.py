# templates/page1/functions/wifi_card_detect.py
import subprocess
import platform
import re
import csv
from io import StringIO


def detect_wifi_adapters():
    """
    Détecte les cartes Wi-Fi connectées à l'ordinateur en fonction du système d'exploitation.

    Returns:
        list of dict: Une liste de dictionnaires contenant les informations des cartes Wi-Fi détectées.
    """
    os_name = platform.system()
    adapters = []

    try:
        if os_name == "Windows":
            adapters = detect_wifi_windows()
        elif os_name == "Linux":
            adapters = detect_wifi_linux()
        elif os_name == "Darwin":
            adapters = detect_wifi_mac()
        else:
            print(f"Système d'exploitation non supporté: {os_name}")
    except Exception as e:
        print(f"Erreur lors de la détection des cartes Wi-Fi: {e}")

    return adapters


def detect_wifi_windows():
    """
    Détecte les cartes Wi-Fi USB sur Windows en utilisant PowerShell.

    Returns:
        list of dict: Liste des cartes Wi-Fi USB détectées.
    """
    # PowerShell command to get network adapters with 'USB' in their InterfaceDescription
    powershell_command = (
        "Get-NetAdapter | Where-Object {$_.InterfaceDescription -like '*USB*'} | "
        "Select Name, MacAddress, InterfaceDescription, Status | ConvertTo-CSV -NoTypeInformation"
    )
    try:
        # Exécuter la commande PowerShell
        output = subprocess.check_output(
            ["powershell.exe", "-Command", powershell_command],
            encoding='utf-8',
            errors="ignore"
        )

        # Parser le CSV
        csv_reader = csv.DictReader(StringIO(output))
        adapters = []
        for row in csv_reader:
            adapters.append({
                "Name": row.get("Name", "N/A"),
                "MacAddress": row.get("MacAddress", "N/A"),
                "InterfaceDescription": row.get("InterfaceDescription", "N/A"),
                "Status": row.get("Status", "N/A")
            })
        return adapters
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande PowerShell: {e}")
        return []


def detect_wifi_linux():
    """
    Détecte les cartes Wi-Fi sur Linux en utilisant la commande 'iwconfig'.

    Returns:
        list of dict: Liste des cartes Wi-Fi détectées.
    """
    command = ["iwconfig"]
    try:
        output = subprocess.check_output(command, encoding='utf-8', errors="ignore")
    except subprocess.CalledProcessError:
        output = ""
    adapters = []
    adapter_info = {}

    for line in output.split('\n'):
        if not line.strip():
            continue
        if not line.startswith(' '):
            # Nouvelle interface
            adapter_name = line.split()[0]
            adapter_info = {'Interface': adapter_name}
        if "ESSID" in line:
            essid = re.search(r'ESSID:"(.*?)"', line)
            adapter_info['ESSID'] = essid.group(1) if essid else "N/A"
        if "Access Point" in line:
            ap = re.search(r'Access Point: (.*?)$', line)
            adapter_info['Access Point'] = ap.group(1) if ap else "N/A"
            adapters.append(adapter_info)
            adapter_info = {}
    return adapters


def detect_wifi_mac():
    """
    Détecte les cartes Wi-Fi sur macOS en utilisant la commande 'networksetup'.

    Returns:
        list of dict: Liste des cartes Wi-Fi détectées.
    """
    # Liste toutes les interfaces matérielles
    command = ["networksetup", "-listallhardwareports"]
    output = subprocess.check_output(command, encoding='utf-8', errors="ignore")
    adapters = []
    adapter_info = {}

    for block in output.strip().split("\n\n"):
        for line in block.split('\n'):
            if line.startswith("Hardware Port"):
                adapter_info['Hardware Port'] = line.split(" : ")[1]
            elif line.startswith("Device"):
                adapter_info['Device'] = line.split(" : ")[1]
            elif line.startswith("Ethernet Address"):
                adapter_info['Ethernet Address'] = line.split(" : ")[1]
        if 'Hardware Port' in adapter_info and 'Device' in adapter_info:
            if 'Wi-Fi' in adapter_info['Hardware Port']:
                adapters.append(adapter_info)
            adapter_info = {}
    return adapters
