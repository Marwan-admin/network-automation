# vlan_manager.py - VLAN Automation

from netmiko import ConnectHandler
from devices import DEVICES

def add_vlan(vlan_id, vlan_name):
    print(f"\n[+] Adding VLAN {vlan_id} ({vlan_name}) to SW1...")
    conn = ConnectHandler(**DEVICES["SW1"])
    conn.enable()

    commands = [
        f"vlan {vlan_id}",
        f"name {vlan_name}",
        "exit",
    ]
    conn.send_config_set(commands)

    output = conn.send_command("show vlan brief")
    conn.disconnect()

    if str(vlan_id) in output:
        print(f"[✓] VLAN {vlan_id} added successfully!")
    else:
        print(f"[✗] Failed to add VLAN {vlan_id}")

    return output

def show_vlans():
    print("\n[+] Getting VLANs from SW1...")
    conn = ConnectHandler(**DEVICES["SW1"])
    conn.enable()
    output = conn.send_command("show vlan brief")
    conn.disconnect()
    print(output)

def main():
    print("=" * 40)
    print("   VLAN Manager")
    print("=" * 40)
    print("\n1. Show VLANs")
    print("2. Add VLAN")
    choice = input("\nChoice: ")

    if choice == "1":
        show_vlans()
    elif choice == "2":
        vid = input("VLAN ID: ")
        vname = input("VLAN Name: ")
        add_vlan(int(vid), vname)

if __name__ == "__main__":
    main()
