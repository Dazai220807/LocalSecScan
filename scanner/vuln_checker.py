from .vuln_db import VULN_PORTS, VULN_SERVICES, VULN_VERSIONS
import re

VERSION_REGEX = re.compile(r"(\d+\.\d+(\.\d+)?)")

def extract_version(text):
    match = VERSION_REGEX.search(text)
    return match.group(1) if match else None

def compare_versions(v1, op, v2):
    def normalize(v):
        return [int(x) for x in v.split(".")]

    v1 = normalize(v1)
    v2 = normalize(v2)

    if op == "<":
        return v1 < v2
    if op == "<=":
        return v1 <= v2
    if op == ">":
        return v1 > v2
    if op == ">=":
        return v1 >= v2
    if op == "==":
        return v1 == v2

    return False

def analyze_vulnerabilities(ports, services):
    vulns = []

    for port in ports:
        if port in VULN_PORTS:
            issue, severity = VULN_PORTS[port]
            vulns.append({"port": port, "issue": issue, "severity": severity})

    for port, info in services.items():
        service = info.split()[0].lower()
        if service in VULN_SERVICES:
            issue, severity = VULN_SERVICES[service]
            vulns.append({"port": port, "issue": issue, "severity": severity})

    for port, info in services.items():
        for name, op, target_version, issue, severity in VULN_VERSIONS:
            if name.lower() in info.lower():
                detected = extract_version(info)
                if detected and compare_versions(detected, op, target_version):
                    vulns.append({"port": port, "issue": issue, "severity": severity})

    return vulns
