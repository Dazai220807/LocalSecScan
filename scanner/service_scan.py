import subprocess
import re

SERVICE_REGEX = re.compile(r"(\d+)/tcp\s+open\s+([\w\-\./]+)\s*(.*)")

def detect_services(ip, ports):
    if not ports:
        return {}

    port_list = ",".join(str(p) for p in ports.keys())
    cmd = ["nmap", "-sV", "-T4", "-p", port_list, ip]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=20,
            check=True
        )
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] Service scan trop long pour {ip}, skip.")
        return {}
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] Le scan de services a échoué : {e}")
        return {}

    services = {}
    for line in result.stdout.splitlines():
        match = SERVICE_REGEX.search(line)
        if match:
            port = int(match.group(1))
            service = match.group(2)
            version = match.group(3).strip()
            services[port] = f"{service} {version}".strip()

    return services
