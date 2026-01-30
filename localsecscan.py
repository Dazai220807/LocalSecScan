#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import netifaces
import webbrowser

from scanner.network_scan import discover_hosts
from scanner.port_scan import scan_ports
from scanner.service_scan import detect_services
from scanner.vuln_checker import analyze_vulnerabilities
from utils.export import export_json, export_html
from utils.display import (
    print_banner,
    print_hosts,
    print_scan_results,
    print_vuln_summary
)
import sys
import os
import shutil
import platform

def check_nmap():
    if platform.system() == "Windows":
        if shutil.which("nmap") is None:
            webbrowser.open("https://nmap.org/download.html")
            raise SystemExit("[ERREUR] Nmap n'est pas installé. Télécharge-le depuis la page ouverte.")


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_local_network():
    gateways = netifaces.gateways()
    default_iface = gateways['default'][netifaces.AF_INET][1]

    addr_info = netifaces.ifaddresses(default_iface)[netifaces.AF_INET][0]
    ip = addr_info['addr']
    netmask = addr_info['netmask']

    cidr = mask_to_cidr(netmask)
    network = ip_to_network(ip, cidr)

    return f"{network}/{cidr}"

def mask_to_cidr(mask):
    return sum(bin(int(x)).count("1") for x in mask.split("."))

def ip_to_network(ip, cidr):
    ip_parts = list(map(int, ip.split(".")))
    mask = (0xffffffff << (32 - cidr)) & 0xffffffff
    ip_int = (ip_parts[0] << 24) | (ip_parts[1] << 16) | (ip_parts[2] << 8) | ip_parts[3]
    network_int = ip_int & mask
    return ".".join(str((network_int >> (8 * i)) & 0xff) for i in reversed(range(4)))


def parse_arguments():
    parser = argparse.ArgumentParser(description="LocalSecScan - Scanner réseau local")
    parser.add_argument("--ip", help="Plage IP à scanner (ex: 192.168.1.0/24)")
    parser.add_argument("--fast", action="store_true", help="Scan rapide")
    parser.add_argument("--verbose", action="store_true", help="Affichage détaillé")
    parser.add_argument("--json", help="Exporter les résultats au format JSON")
    parser.add_argument("--html", help="Exporter les résultats au format HTML")
    return parser.parse_args()


def scan_host(host, fast):
    ports = scan_ports(host, fast=fast)
    services = detect_services(host, ports)
    vulns = analyze_vulnerabilities(ports, services)
    return host, ports, services, vulns



def main():
    try:
        webbrowser.open(resource_path("splash.html"))
    except:
        pass

    print_banner()
    check_nmap()
    args = parse_arguments()

    if args.ip:
        network = args.ip
    else:
        print("[INFO] Détection automatique du réseau local…")
        network = get_local_network()
        print(f"[INFO] Réseau détecté : {network}")

    hosts = discover_hosts(network)
    print_hosts(hosts)

    results = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(scan_host, host, args.fast): host
            for host in hosts
        }

        for future in as_completed(futures):
            host, ports, services, vulns = future.result()
            results[host] = {
                "ports": ports,
                "services": services,
                "vulns": vulns
            }
            print_scan_results(host, ports, services, vulns, verbose=args.verbose)

    if args.json:
        export_json(results, args.json)

    if args.html:
        export_html(results, args.html)
        try:
            webbrowser.open(args.html)
        except:
            pass

    print_vuln_summary(results)


if __name__ == "__main__":
    main()
