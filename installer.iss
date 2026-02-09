; ---------------------------------------------------------
; LocalSecScan - Installateur Windows
; ---------------------------------------------------------

[Setup]
AppName=LocalSecScan
AppVersion=1.0
DefaultDirName={pf}\LocalSecScan
DefaultGroupName=LocalSecScan
OutputDir=output
OutputBaseFilename=LocalSecScan-Setup
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
ChangesEnvironment=yes

[Files]
Source: "release\localsecscan.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "release\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\LocalSecScan"; Filename: "{app}\localsecscan.exe"
Name: "{commondesktop}\LocalSecScan"; Filename: "{app}\localsecscan.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Créer un raccourci sur le bureau"

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
ValueType: expandsz; ValueName: "Path"; ValueData: "{app};{olddata}"

[Run]
; Télécharger Nmap (avec Npcap inclus)
Filename: "powershell.exe"; \
Parameters: "-Command ""Invoke-WebRequest 'https://nmap.org/dist/nmap-7.95-setup.exe' -OutFile '{tmp}\nmap.exe'"""; \
Flags: runhidden

; Lancer l'installation normale (interface visible)
Filename: "{tmp}\nmap.exe"; Flags: shellexec postinstall

; Lancer LocalSecScan à la fin
Filename: "{app}\localsecscan.exe"; Flags: nowait postinstall skipifsilent
