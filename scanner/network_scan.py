import subprocess
import re

HOST_REGEX = re.compile(r"Nmap scan report for ([\d\.]+)")

def discover_hosts(network):
    cmd = ["nmap", "-sn", network]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=20
        )
    except FileNotFoundError:
        print("[ERREUR] Nmap n'est pas installé sur ce système.")
        return []
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] La commande Nmap a échoué : {e}")
        return []
    
    hosts = []
    for line in result.stdout.splitlines():
        match = HOST_REGEX.search(line)
        if match:
            hosts.append(match.group(1))

    return hosts

