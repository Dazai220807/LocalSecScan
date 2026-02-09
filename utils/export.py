import json
import os
from utils.paths import rapport

def export_json(results, filename):
    serializable = {}

    for ip, data in results.items():
        ports = {str(p): state for p, state in data.get("ports", {}).items()}
        services = {str(p): svc for p, svc in data.get("services", {}).items()}
        vulns = data.get("vulns", [])

        serializable[ip] = {
            "ports": ports,
            "services": services,
            "vulns": vulns,
        }

    # Création du dossier si nécessaire
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=4, ensure_ascii=False)

    print(f"[OK] Résultats exportés en JSON : {filename}")


def export_html(results, filename="rapport.html"):
    # Nouveau chemin propre : Documents/LocalSecScan/rapport.html
    base_dir = os.path.join(os.path.expanduser("~"), "Documents", "LocalSecScan")
    os.makedirs(base_dir, exist_ok=True)

    output_path = os.path.join(base_dir, filename)

    total_hosts = len(results)
    total_vulns = 0
    sev_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}

    for data in results.values():
        vulns = data.get("vulns", [])
        total_vulns += len(vulns)
        for v in vulns:
            sev = v.get("severity", "").lower()
            if sev in sev_counts:
                sev_counts[sev] += 1

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Rapport LocalSecScan</title>

<style>
/* (tout ton CSS inchangé) */
body {{
    font-family: "Segoe UI", Roboto, Arial, sans-serif;
    background: #0d1117;
    color: #e6edf3;
    padding: 20px;
}}
h1 {{
    text-align: center;
    color: #58a6ff;
    margin-bottom: 20px;
}}
.dashboard {{
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
}}
.card {{
    flex: 1;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 12px rgba(0,0,0,0.4);
    text-align: center;
}}
.card-title {{
    font-size: 0.9rem;
    color: #9ca3af;
    margin-bottom: 5px;
}}
.card-value {{
    font-size: 1.6rem;
    font-weight: bold;
}}
.card-critical {{ color: #ff0033; }}
.card-high {{ color: #f85149; }}
.card-medium {{ color: #d29922; }}
.card-low {{ color: #3fb950; }}

.host {{
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 20px;
    margin-bottom: 30px;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(0,0,0,0.4);
}}
h2 {{
    color: #79c0ff;
    margin-top: 0;
}}
h3 {{
    color: #9ecbff;
    margin-bottom: 10px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    margin-bottom: 20px;
}}
th {{
    background: #161b22;
    color: #c9d1d9;
    padding: 10px;
    border-bottom: 2px solid #30363d;
}}
td {{
    padding: 10px;
    border-bottom: 1px solid #21262d;
}}
tr:hover {{
    background: rgba(255, 255, 255, 0.05);
}}
.severity-low {{
    color: #3fb950;
    font-weight: bold;
}}
.severity-medium {{
    color: #d29922;
    font-weight: bold;
}}
.severity-high {{
    color: #f85149;
    font-weight: bold;
}}
.severity-critical {{
    color: #ff0033;
    font-weight: bold;
    text-shadow: 0 0 6px rgba(255,0,0,0.6);
}}
</style>

</head>
<body>

<h1>Rapport LocalSecScan</h1>

<div class="dashboard">
  <div class="card">
    <div class="card-title">Hôtes scannés</div>
    <div class="card-value">{total_hosts}</div>
  </div>
  <div class="card">
    <div class="card-title">Vulnérabilités totales</div>
    <div class="card-value">{total_vulns}</div>
  </div>
  <div class="card card-critical">
    <div class="card-title">Critiques</div>
    <div class="card-value">{sev_counts["critical"]}</div>
  </div>
  <div class="card card-high">
    <div class="card-title">High</div>
    <div class="card-value">{sev_counts["high"]}</div>
  </div>
  <div class="card card-medium">
    <div class="card-title">Medium</div>
    <div class="card-value">{sev_counts["medium"]}</div>
  </div>
  <div class="card card-low">
    <div class="card-title">Low</div>
    <div class="card-value">{sev_counts["low"]}</div>
  </div>
</div>
"""

    for ip, data in results.items():
        html += f"<div class='host'>"
        html += f"<h2>{ip}</h2>"

        html += "<h3>Ports ouverts</h3>"
        if data.get("ports"):
            html += "<table><tr><th>Port</th><th>État</th></tr>"
            for port, state in data["ports"].items():
                html += f"<tr><td>{port}</td><td>{state}</td></tr>"
            html += "</table>"
        else:
            html += "<p>Aucun port ouvert.</p>"

        html += "<h3>Services détectés</h3>"
        if data.get("services"):
            html += "<table><tr><th>Port</th><th>Service</th></tr>"
            for port, service in data["services"].items():
                html += f"<tr><td>{port}</td><td>{service}</td></tr>"
            html += "</table>"
        else:
            html += "<p>Aucun service détecté.</p>"

        html += "<h3>Vulnérabilités</h3>"
        if data.get("vulns"):
            html += "<table><tr><th>Port</th><th>Problème</th><th>Gravité</th></tr>"
            for v in data["vulns"]:
                sev = v["severity"].lower()
                html += (
                    f"<tr><td>{v['port']}</td>"
                    f"<td>{v['issue']}</td>"
                    f"<td class='severity-{sev}'>{sev}</td></tr>"
                )
            html += "</table>"
        else:
            html += "<p>Aucune vulnérabilité détectée.</p>"

        html += "</div>"

    html += "</body></html>"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] Rapport HTML généré : {output_path}")
    return output_path
