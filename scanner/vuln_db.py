VULN_PORTS = {
    21:  ("FTP non sécurisé", "high"),
    23:  ("Telnet non sécurisé", "critical"),
    69:  ("TFTP sans authentification", "high"),
    80:  ("HTTP non chiffré", "medium"),
    110: ("POP3 non chiffré", "medium"),
    143: ("IMAP non chiffré", "medium"),
    445: ("SMB vulnérable (EternalBlue)", "critical"),
    3389: ("RDP exposé", "high"),
    3306: ("MySQL exposé", "high"),
    5432: ("PostgreSQL exposé", "high"),
    6379: ("Redis sans authentification", "critical"),
}

VULN_SERVICES = {
    "ftp":      ("FTP non sécurisé", "high"),
    "telnet":   ("Telnet obsolète", "critical"),
    "http":     ("HTTP non chiffré", "medium"),
    "mysql":    ("MySQL accessible", "high"),
    "postgres": ("PostgreSQL accessible", "high"),
    "redis":    ("Redis sans auth", "critical"),
    "ldap":     ("LDAP non chiffré", "high"),
    "smb":      ("SMB vulnérable", "critical"),
}

VULN_VERSIONS = [
    ("OpenSSH", "<", "7.4", "OpenSSH obsolète", "medium"),
    ("Apache", "<", "2.4.50", "Apache vulnérable (path traversal)", "high"),
    ("nginx", "<", "1.18.0", "nginx obsolète", "medium"),
    ("MySQL", "<", "5.7", "MySQL obsolète", "high"),
]
