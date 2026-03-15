# backup.py - Automated Config Backup

import datetime
import os
from netmiko import ConnectHandler
from devices import DEVICES

BACKUP_DIR = "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_device(name, config):
    print(f"\n[+] Connecting to {name}...")
    conn = ConnectHandler(**config)
    conn.enable()

    output = conn.send_command("show running-config")
    conn.disconnect()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{BACKUP_DIR}/{name}_{timestamp}.cfg"

    with open(filename, "w") as f:
        f.write(output)

    print(f"[✓] {name} backup saved → {filename}")

def main():
    print("=" * 40)
    print("   Network Backup Tool")
    print("=" * 40)
    for name, config in DEVICES.items():
        backup_device(name, config)
    print("\n[✓] All backups completed!")

if __name__ == "__main__":
    main()