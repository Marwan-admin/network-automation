# 🚀 Network Automation Project

Automated network management using Python & Netmiko over SSH,
extended with Fortigate Firewall REST API integration.

---

## 🖥️ Lab Environment

| Device | Role | IP |
|--------|------|----|
| Cisco vIOS Router | R1 | 192.168.8.10 |
| Cisco vIOS Switch | SW1 | 192.168.8.20 |
| Ubuntu 22.04 | Controller | 192.168.8.30 |
| Fortigate Firewall | FW1 | 192.168.8.29 |

---

## 📁 Project Structure
```
network_automation/
├── devices.py           # Device inventory (Cisco)
├── backup.py            # Automated config backup
├── vlan_manager.py      # VLAN add/show automation
├── network_report.py    # Full network status report
├── ping_monitor.py      # Real-time ping monitor
├── app.py               # Flask Web Dashboard
├── templates/
│   └── index.html       # Dashboard UI
└── fortigate/           # Fortigate REST API module
    ├── __init__.py
    └── fortigate_api.py
```

---

## ⚙️ Features

### Part 1 — Cisco Automation
- ✅ SSH connection management via Netmiko
- ✅ Automated config backup with timestamps
- ✅ VLAN provisioning on Cisco switches
- ✅ Network status reporting
- ✅ Real-time ping monitoring
- ✅ Web Dashboard (Flask)

### Part 2 — Fortigate Firewall Integration
- ✅ Fortigate REST API connection via Python
- ✅ Read interfaces status and IP addresses
- ✅ Read and display Firewall Policies
- ✅ Automated config backup via API
- ✅ Fortigate section added to Web Dashboard

---

## 🔬 Lab 2 — Fortigate Firewall from Scratch

### 🎯 Goal
Extend the existing Network Automation project to support
Fortigate Firewall management via REST API, and integrate
it into the Flask Web Dashboard alongside Cisco devices.

---

### Step 1 — Configure WAN Interface (port1)
Set port1 to receive an IP address automatically via DHCP
from the existing network (192.168.8.0/24).
```bash
config system interface
    edit "port1"
        set mode dhcp
        set allowaccess ping https ssh
    next
end
```

**Result:** port1 received IP `192.168.8.29` from the network.

---

### Step 2 — Configure LAN Interface (port2)
Set port2 with a static IP to serve as the gateway
for internal devices.
```bash
config system interface
    edit "port2"
        set mode static
        set ip 192.168.1.1 255.255.255.0
        set allowaccess ping https ssh
        set role lan
    next
end
```

**Result:** port2 = `192.168.1.1` — internal LAN gateway.

---

### Step 3 — Configure Default Route
Tell the Fortigate to send all unknown traffic through
port1 toward the internet via the network gateway.
```bash
config router static
    edit 1
        set gateway 192.168.8.1
        set device "port1"
    next
end
```

**Result:** All internet-bound traffic routes through port1.

---

### Step 4 — Firewall Policy + NAT
Allow internal devices (LAN) to reach the internet (WAN)
and enable NAT so they use the Fortigate's public IP.
```bash
config firewall policy
    edit 1
        set name "LAN-to-WAN"
        set srcintf "port2"
        set dstintf "port1"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set nat enable
    next
end
```

**Result:** Internal devices can now access the internet.

---

### Step 5 — DHCP Server on LAN
Configure the Fortigate to automatically assign IP addresses
to devices connected to port2.
```bash
config system dhcp server
    edit 1
        set interface "port2"
        set default-gateway 192.168.1.1
        set netmask 255.255.255.0
        set dns-service default
        config ip-range
            edit 1
                set start-ip 192.168.1.10
                set end-ip 192.168.1.100
            next
        end
    next
end
```

**Result:** Any device on port2 gets an IP from `192.168.1.10–100`.

---

### Step 6 — Enable REST API on Fortigate
Created a REST API Admin account on Fortigate GUI:
```
System → Administrators → Create New → REST API Admin
- Username: python-api
- Profile: super_admin
- PKI Group: disabled
```

**Result:** Generated API Key used by Python to communicate
with the Fortigate.

---

### Step 7 — Python REST API Module
Created `fortigate/fortigate_api.py` — a Python class
that connects to the Fortigate API and provides methods for:
- Reading interfaces
- Reading firewall policies
- Backing up the configuration
```python
from fortigate.fortigate_api import FortigateAPI

fg = FortigateAPI(host="192.168.8.29", api_key="YOUR_KEY")
fg.get_interfaces()   # Read all interfaces
fg.get_policies()     # Read firewall policies
fg.backup_config()    # Download full config backup
```

---

### Step 8 — Dashboard Integration
Added a Fortigate section to the Flask Web Dashboard with:
- **Show Interfaces** — displays all interfaces with IP and status
- **Show Policies** — displays firewall policies in a table
- **Backup Config** — triggers a backup saved with timestamp

**Result:** Full visibility and control of the Fortigate
directly from the web dashboard at `http://192.168.8.30:5000`

---

## 🛠️ Installation
```bash
pip3 install netmiko flask requests
```

## 🚀 Usage
```bash
python3 backup.py           # Backup Cisco devices
python3 vlan_manager.py     # Manage VLANs
python3 network_report.py   # Generate report
python3 ping_monitor.py     # Start monitor
python3 app.py              # Launch dashboard → http://IP:5000
```

## 🔧 Tools

`Python 3.10` `Netmiko 4.6.0` `Flask` `Requests`
`Cisco IOS` `Fortigate FortiOS` `EVE-NG` `Ubuntu 22.04`