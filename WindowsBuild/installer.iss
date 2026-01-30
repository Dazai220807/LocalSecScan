; -----------------------------------------
; Installeur Windows pour LocalSecScan
; -----------------------------------------

[Setup]
AppName=LocalSecScan
AppVersion=1.0
DefaultDirName={pf}\LocalSecScan
DefaultGroupName=LocalSecScan
OutputDir=.
OutputBaseFilename=LocalSecScan_Installer
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "localsecscan.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "splash.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\LocalSecScan"; Filename: "{app}\localsecscan.exe"; IconFilename: "{app}\icon.ico"
Name: "{commondesktop}\LocalSecScan"; Filename: "{app}\localsecscan.exe"; IconFilename: "{app}\icon.ico"

[Run]
; Lancer le programme à la fin de l'installation
Filename: "{app}\localsecscan.exe"; Description: "Lancer LocalSecScan"; Flags: nowait postinstall skipifsilent

; Vérifier si Python est installé
Filename: "cmd.exe"; Parameters: "/c python --version"; Flags: runhidden; StatusMsg: "Vérification de Python..."

; Installer Python si absent
Filename: "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"; \
    Parameters: "/quiet InstallAllUsers=1 PrependPath=1"; \
    Flags: skipifdoesntexist

; Vérifier si Nmap est installé
Filename: "cmd.exe"; Parameters: "/c nmap --version"; Flags: runhidden; StatusMsg: "Vérification de Nmap..."

; Installer Nmap si absent
Filename: "https://nmap.org/dist/nmap-7.95-setup.exe"; \
    Parameters: "/S"; \
    Flags: skipifdoesntexist
