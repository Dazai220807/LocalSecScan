def print_banner():
    print("=== LocalSecScan - Scanner réseau local ===")

def print_hosts(hosts):
    print("\n[+] Machines détectées :")
    for h in hosts:
        print(f" - {h}")

def print_scan_results(ip, ports, services, vulns, verbose=False):
    print(f"\n[+] Résultats pour {ip}")
    print("Ports ouverts :", list(ports.keys()))
    if verbose:
        print("Services :", services)
        print("Vulnérabilités :", vulns)

def print_vuln_summary(results):
    print("\n=== Résumé des vulnérabilités ===")
    for ip, data in results.items():
        if data["vulns"]:
            print(f"{ip} : {len(data['vulns'])} vulnérabilité(s)")
        else:
            print(f"{ip} : aucune vulnérabilité détectée")
