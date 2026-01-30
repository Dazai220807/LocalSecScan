#!/usr/bin/env python3

import argparse
from scanner.network_scan import discover_hosts
from scanner.port_scan import scan_ports
from scanner.service_scan import detect_services
from scanner.vuln_checker import analyze_vulnerabilities
from utils.display import (
    print_banner,
    print_hosts,
    print_scan_results,
    print_vuln_summary
)

def parse_arguments():
    parser = argparse.ArgumentParser(description="LocalSecScan - Scanner réseau local")
    parser.add_argument("--ip", required=True, help="Plage IP à scanner (ex: 192.168.1.0/24)")
    parser.add_argument("--fast", action="store_true", help="Scan rapide")
    parser.add_argument("--verbose", action="store_true", help="Affichage détaillé")
    return parser.parse_args()

def main():
    print_banner()
    args = parse_arguments()

    hosts = discover_hosts(args.ip)
    print_hosts(hosts)

    results = {}

    for host in hosts:
        ports = scan_ports(host, fast=args.fast)
        services = detect_services(host, ports)
        vulns = analyze_vulnerabilities(ports, services)

        results[host] = {
            "ports": ports,
            "services": services,
            "vulns": vulns
        }

        print_scan_results(host, ports, services, vulns, verbose=args.verbose)

    print_vuln_summary(results)

if __name__ == "__main__":
    main()
