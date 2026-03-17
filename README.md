# 🚀 Network Automation Project

Automated network management platform built with **Python**, **Netmiko**, and **REST API** —
covering Cisco IOS device automation over SSH and FortiGate Firewall integration via FortiOS API,
unified under a **Flask Web Dashboard**.

---

## 🖥️ Lab Environment

| Device | Role | OS / Version | IP Address |
|--------|------|-------------|------------|
| Cisco vIOS Router | R1 — Core Router | Cisco IOS 15.9(3)M6 | 192.168.8.10 |
| Cisco vIOS Switch | SW1 — Access Switch | Cisco IOS 15.2(4)E | 192.168.8.20 |
| Ubuntu 22.04 | Controller (Automation Host) | Ubuntu 22.04 LTS | 192.168.8.30 |
| FortiGate Firewall | FW1 — Perimeter Firewall | FortiOS 7.4.11-build2878 | 192.168.8.29 |

> **Platform:** EVE-NG virtual lab. All devices on subnet `192.168.8.0/24`.

---

## 📁 Project Structure
```
network-automation/
├── devices.py              # Cisco device inventory
├── test_coonection.py      # Initial SSH connectivity test
├── backup.py               # Automated config backup
├── vlan_manager.py         # VLAN provisioning on SW1
├── network_report.py       # Network status report
├── ping_monitor.py         # Real-time ping monitor
├── app.py                  # Flask Web Dashboard
├── templates/
│   └── index.html          # Dashboard frontend
├── backups/                # Auto-generated .cfg backup files
└── fortigate/
    ├── __init__.py
    └── fortigate_api.py    # FortigateAPI class
```

---

## 🛠️ Installation
```bash
git clone https://github.com/Marwan-admin/network-automation.git
cd network-automation
pip3 install netmiko flask requests
```

---

## 🚀 Usage
```bash
python3 backup.py           # Backup running-config from R1 and SW1
python3 vlan_manager.py     # Show or add VLANs on SW1
python3 network_report.py   # Print interface status + IOS version
python3 ping_monitor.py     # Start real-time ping monitor (Ctrl+C to stop)
python3 app.py              # Launch dashboard → http://192.168.8.30:5000
```

---

## 📅 Day 1 — Cisco Device Automation
**Date:** March 13, 2026

Set up a full Python automation framework for managing Cisco devices over SSH using Netmiko.
Started by building a centralized device inventory, then tested the first live SSH connection to R1.
From there, built scripts to automatically back up device configurations with timestamps,
manage VLANs on SW1, generate a full network status report pulling interface states and IOS versions,
and run a real-time ping monitor that alerts on device state changes.
Wrapped everything up with a Flask web dashboard exposing all these functions through a browser interface at `http://192.168.8.30:5000`.

| Script | What it does |
|--------|-------------|
| `devices.py` | Centralized SSH credentials for R1 and SW1 |
| `test_coonection.py` | Verified first SSH connection to R1 |
| `backup.py` | Auto-saves running-config with timestamp to `backups/` |
| `vlan_manager.py` | Add or list VLANs on SW1 |
| `network_report.py` | Collects interfaces + IOS version from all devices |
| `ping_monitor.py` | Pings all devices every 30s, alerts on UP/DOWN change |
| `app.py` | Flask dashboard with REST API for all functions |

---

## 📅 Day 2 — FortiGate Firewall Integration
**Date:** March 17, 2026

Extended the platform to include FortiGate Firewall management.
Started by configuring the FortiGate from scratch via CLI inside EVE-NG —
setting up WAN (port1 via DHCP) and LAN (port2 static `192.168.1.1/24`) interfaces,
adding a default route, creating a LAN-to-WAN firewall policy with NAT,
and enabling a DHCP server on the LAN.
Then enabled the FortiOS REST API and created a dedicated API admin account.
Built a Python `FortigateAPI` class to read interfaces, read firewall policies,
and download configuration backups via the API.
Finished by integrating all three functions into the existing Flask dashboard
as new endpoints alongside the Cisco section.

| Component | What it does |
|-----------|-------------|
| FortiGate CLI config | WAN/LAN interfaces, routing, NAT policy, DHCP server |
| REST API admin | `python-api` account with API key for programmatic access |
| `fortigate/fortigate_api.py` | Python class — interfaces, policies, config backup via API |
| `test_fortigate.py` | Verified API connectivity and data retrieval |
| `app.py` (updated) | 3 new FortiGate endpoints added to the dashboard |

---

## 🔧 Tools & Versions

| Tool | Version | Role |
|------|---------|------|
| Python | 3.10 | Main automation language |
| Netmiko | 4.6.0 | SSH handler for Cisco devices |
| Flask | latest | Web dashboard framework |
| Requests | latest | HTTP client for FortiOS REST API |
| Cisco IOS | 15.9 / 15.2 | Router and Switch OS |
| FortiOS | 7.4.11-build2878 | FortiGate Firewall OS |
| EVE-NG | — | Virtual network lab platform |
| Ubuntu | 22.04 LTS | Automation controller OS |