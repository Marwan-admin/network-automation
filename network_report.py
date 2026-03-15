# network_report.py - Full Network Report

import datetime
from netmiko import ConnectHandler
from devices import DEVICES

def get_report(name, config):
    print(f"[+] Collecting data from {name}...")
    conn = ConnectHandler(**config)
    conn.enable()

    interfaces = conn.send_command("show ip interface brief")
    version    = conn.send_command("show version")
    conn.disconnect()

    # استخراج IOS version
    ios_ver = ""
    for line in version.splitlines():
        if "Version" in line and "Cisco" in line:
            ios_ver = line.strip()
            break

    return {
        "name": name,
        "interfaces": interfaces,
        "ios_version": ios_ver,
    }

def main():
    print("=" * 50)
    print("   Network Status Report")
    print(f"   {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    for name, config in DEVICES.items():
        data = get_report(name, config)
        print(f"\n{'─'*40}")
        print(f"Device  : {data['name']}")
        print(f"Version : {data['ios_version']}")
        print(f"\nInterfaces:\n{data['interfaces']}")

    print("\n[✓] Report complete!")

if __name__ == "__main__":
    main()
