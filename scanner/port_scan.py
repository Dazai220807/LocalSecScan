import subprocess
import re

PORT_REGEX = re.compile(r"(\d+)/tcp\s+open")

def scan_ports(ip, fast=False):
    """
    Scanne les ports ouverts d'une machine.
    Retourne un dict {port: 'open'}.
    """
    ports = {}

    # Choix de la commande selon le mode
    if fast :
        cmd = ["nmap", "-T4", "--top-ports", "100", ip]
    else:
        cmd = ["nmap", "-T4", "-p-", ip]

    try :
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=60
        )
    except FileNotFoundError:
        print("[ERREUR] Nmap n'est pas installé.")
        return {}
    except subprocess.CalledProcessError:
        print("[ERREUR] Le scan de ports a échoué.")
        return {}

    # Parsing des ports ouverts
    for line in result.stdout.splitlines():
        match = PORT_REGEX.search(line)
        if match:
            port = int(match.group(1))
            ports[port] = "open"

    return ports

