#!/usr/bin/env python3

import argparse
import platform
import shutil
import sys
import os
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed

import netifaces

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


# ------------------------------
# Terminal utilities
# ------------------------------

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def restore_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def print_progress(current, total, width=40):
    ratio = current / total if total else 1
    filled = int(ratio * width)
    bar = "█" * filled + "░" * (width - filled)
    percent = int(ratio * 100)

    sys.stdout.write("\033[2K\r")  # clear line
    sys.stdout.write(f"[SCAN] {bar} {percent}%")
    sys.stdout.flush()


# ------------------------------
# Network utilities
# ------------------------------

def check_nmap():
    if platform.system() == "Windows" and shutil.which("nmap") is None:
        webbrowser.open("https://nmap.org/download.html")
        raise SystemExit("[ERREUR] Nmap n'est pas installé. Télécharge-le depuis la page ouverte.")

def mask_to_cidr(mask):
    return sum(bin(int(x)).count("1") for x in mask.split("."))

def ip_to_network(ip, cidr):
    parts = list(map(int, ip.split(".")))
    mask = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF
    ip_int = (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3]
    net_int = ip_int & mask
    return ".".join(str((net_int >> (8 * i)) & 0xFF) for i in reversed(range(4)))

def get_local_network():
    gateways = netifaces.gateways()
    iface = gateways['default'][netifaces.AF_INET][1]
    info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]

    ip = info['addr']
    netmask = info['netmask']
    cidr = mask_to_cidr(netmask)
    network = ip_to_network(ip, cidr)

    return f"{network}/{cidr}"


# ------------------------------
# Argument parsing
# ------------------------------

def parse_arguments():
    parser = argparse.ArgumentParser(description="LocalSecScan - Scanner réseau local")
    parser.add_argument("--ip", help="Plage IP à scanner (ex: 192.168.1.0/24)")
    parser.add_argument("--fast", action="store_true", help="Scan rapide")
    parser.add_argument("--verbose", action="store_true", help="Affichage détaillé")
    parser.add_argument("--json", help="Exporter les résultats au format JSON")
    parser.add_argument("--html", nargs="?", const="rapport.html", help="Exporter les résultats au format HTML")
    return parser.parse_args()


# ------------------------------
# Host scanning
# ------------------------------

def scan_host(host, fast):
    ports = scan_ports(host, fast=fast)
    services = detect_services(host, ports)
    vulns = analyze_vulnerabilities(ports, services)
    return host, ports, services, vulns


# ------------------------------
# Main program
# ------------------------------

def main():
    print_banner()
    check_nmap()
    args = parse_arguments()

    # Network selection
    if args.ip:
        network = args.ip
    else:
        print("[INFO] Détection automatique du réseau local…")
        network = get_local_network()
        print(f"[INFO] Réseau détecté : {network}")

    # Host discovery
    hosts = discover_hosts(network)
    print_hosts(hosts)

    results = {}
    total_hosts = len(hosts)
    completed = 0

    hide_cursor()
    print("\nDémarrage du scan...\n")
    print_progress(0, total_hosts)

    # Parallel scanning
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(scan_host, h, args.fast): h for h in hosts}

        for future in as_completed(futures):
            host, ports, services, vulns = future.result()
            results[host] = {"ports": ports, "services": services, "vulns": vulns}

            completed += 1
            print_progress(completed, total_hosts)

            print()
            print_scan_results(host, ports, services, vulns, verbose=args.verbose)

    print_progress(total_hosts, total_hosts)
    print("\n\nScan terminé.\n")

    # Exports
    if args.json:
        export_json(results, args.json)

    html_path = export_html(results, args.html or "rapport.html")

    try:
        webbrowser.open(html_path)
    except:
        pass

    print_vuln_summary(results)

    # Restore terminal state
    os.system("stty sane")
    restore_cursor()


if __name__ == "__main__":
    main()
