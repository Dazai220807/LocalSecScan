
# 🛡️ LocalSecScan  
Scanner réseau local — Détection d’hôtes, ports, services et vulnérabilités

---

## 🚀 Présentation

**LocalSecScan** est un scanner réseau local complet, conçu pour analyser rapidement un réseau, identifier les hôtes actifs, détecter les ports ouverts, reconnaître les services exposés et repérer les vulnérabilités courantes.

Pensé comme un outil pédagogique et professionnel, il combine :

- une architecture Python modulaire  
- un rapport HTML premium (dark cyber)  
- un splash animé  
- une UX claire et efficace  
- une détection réseau automatique  

Ce projet est idéal pour démontrer des compétences en **cybersécurité**, **réseau**, **Python**, **architecture logicielle**, et **UX technique**.

---

## ✨ Fonctionnalités

### 🔍 Scan réseau
- Détection automatique du réseau local (gateway + masque)
- Découverte des hôtes actifs
- Scan rapide ou complet

### 🔐 Analyse de sécurité
- Détection des ports ouverts
- Identification des services exposés
- Analyse de vulnérabilités basiques (par service/port)
- Score global par hôte

### 📊 Rapport HTML premium
- Dashboard cyber (cartes, couleurs, stats)
- Liste des hôtes analysés
- Ports ouverts + services détectés
- Vulnérabilités classées par sévérité
- Thème dark moderne
- Export automatique (`rapport/rapport.html`)

### 🎬 Splash animé
- Barre de progression dynamique
- Thème cyber cohérent

### 🧩 Architecture modulaire
- `scanner/` → logique réseau, ports, services, vulnérabilités  
- `utils/` → affichage, export, chemins  
- `assets/` → splash, icônes  
- `rapport/` → rapports générés  

---

## 🗂️ Structure du projet

```
LocalSecScan/
│
├── scanner/
│   ├── network_scan.py
│   ├── port_scan.py
│   ├── service_scan.py
│   ├── vuln_checker.py
│   └── vuln_db.py
│
├── utils/
│   ├── display.py
│   ├── export.py
│   └── paths.py
│
├── assets/
│   ├── splash.html
│   ├── icon.png
│   └── icon.ico
│
├── rapport/
│   └── rapport.html   (généré automatiquement)
│
├── localsecscan.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation

### 1) Installer les dépendances

```
pip install -r requirements.txt
```

### 2) Installer Nmap (obligatoire)

- **Linux** :  
  ```
  sudo apt install nmap
  ```
- **Windows** :  
  Téléchargement automatique si non installé.

---

## ▶️ Utilisation

### Scan automatique + rapport HTML (par défaut)

```
python3 localsecscan.py
```

### Scan d’une plage IP spécifique

```
python3 localsecscan.py --ip 192.168.1.0/24
```

### Scan rapide

```
python3 localsecscan.py --fast
```

### Export JSON

```
python3 localsecscan.py --json resultat.json
```

---

## 📸 Aperçu du rapport HTML

*(Ajoute ici une capture d’écran du rapport pour ton portfolio)*

---

## 🧠 Points techniques mis en avant

- Architecture Python modulaire et maintenable  
- Gestion propre des chemins (compatible PyInstaller)  
- ThreadPoolExecutor pour paralléliser les scans  
- Analyse réseau automatique via `netifaces`  
- Génération HTML dynamique avec dashboard  
- UX cyber (splash animé, thème dark)  
- Gestion d’erreurs et fallback propre  

---

## 🧭 Roadmap

- [ ] Ajout d’un score de sécurité global  
- [ ] Graphiques (camemberts, barres) dans le rapport  
- [ ] Détection avancée (bannières, fingerprinting)  
- [ ] Export PDF  
- [ ] Interface graphique (Tkinter / PyQt)  
- [ ] Mode “audit complet”  

---

## 👤 Auteur

**Maël**  
Étudiant en cybersécurité & développeur Python  
Portfolio : *(à ajouter)*  
GitHub : *(ton lien)*

---

## 📄 Licence

Projet open‑source — utilisation libre à des fins éducatives et personnelles.

---
