import subprocess
import re

SERVICE_REGEX = re.compile(r"(\d+)/tcp\s+open\s+([\w\-\./]+)\s*(.*)")

def detect_services(ip, ports):
    """
    Détecte les services et versions sur les ports ouverts.
    Retourne un dict {port: "service version"}.
    """
    services = {}
    port_list = ",".join(str(p) for p in ports.keys())
    cmd = ["nmap", "-sV", "-p", port_list, ip]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
    except FileNotFoundError:
        print("[ERREUR] Nmap n'est pas installé")
        return {}
    except subprocess.CalledProcessError as e:
        print("[ERREUR] Le scan de services a échoué :", e)
        return {}

    for line in result.stdout.splitlines():
        if "/tcp" not in line or "open" not in line:
            continue

        match = SERVICE_REGEX.search(line)

        if match:
            port = int(match.group(1))
            service = match.group(2)
            version = match.group(3).strip()
            services[port] = f"{service} {version}".strip()
            
    return services

