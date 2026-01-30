import subprocess
import re

PORT_REGEX = re.compile(r"(\d+)/tcp\s+open")

def scan_ports(ip, fast=False):
    """
    Scanne les ports ouverts d'une machine.
    Retourne un dict {port: 'open'}.
    """
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
            timeout=15
        )
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] Scan trop long pour {ip}, skip.")
        return {}
    except subprocess.CalledProcessError:
        print(f"[ERREUR] Le scan de ports a échoué pour {ip}.")
        return {}
 
    ports = {}
    for line in result.stdout.splitlines():
        match = PORT_REGEX.search(line)
        if match:
            port = int(match.group(1))
            ports[port] = "open"

    return ports

