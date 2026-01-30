import subprocess
import re

IP_REGEX = re.compile(r"Nmap scan report for (\d+\.\d+\.\d+\.\d+)")


def discover_hosts(ip_range):
    """
    Découvre les machines actives sur le réseau via Nmap.
    Retourne une liste d'adresses IP actives.
    """

    hosts = []
    cmd = ["nmap", "-sn", ip_range]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
    except FileNotFoundError:
        print("[ERREUR] Nmap n'est pas installé sur ce système.")
        return []
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] La commande Nmap a échoué : {e}")
        return []

    for line in result.stdout.splitlines():
        match = IP_REGEX.search(line)
        if match:
            hosts.append(match.group(1))
            
    return hosts

