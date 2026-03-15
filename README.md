# 🚀 Network Automation Project

Automated network management using Python & Netmiko over SSH.

## 🖥️ Lab Environment
| Device | Role | IP |
|--------|------|----|
| Cisco vIOS Router | R1 | 192.168.8.10 |
| Cisco vIOS Switch | SW1 | 192.168.8.20 |
| Ubuntu 22.04 | Controller | 192.168.8.30 |

## 📁 Project Structure
```
network_automation/
├── devices.py         # Device inventory
├── backup.py          # Automated config backup
├── vlan_manager.py    # VLAN add/show automation
├── network_report.py  # Full network status report
├── ping_monitor.py    # Real-time ping monitor
├── app.py             # Flask Web Dashboard
└── templates/
    └── index.html     # Dashboard UI
```

## ⚙️ Features
- ✅ SSH connection management via Netmiko
- ✅ Automated config backup with timestamps
- ✅ VLAN provisioning on Cisco switches
- ✅ Network status reporting
- ✅ Real-time ping monitoring
- ✅ Web Dashboard (Flask)

## 🛠️ Installation
```bash
pip3 install netmiko flask
```

## 🚀 Usage
```bash
python3 backup.py          # Backup all devices
python3 vlan_manager.py    # Manage VLANs
python3 network_report.py  # Generate report
python3 ping_monitor.py    # Start monitor
python3 app.py             # Launch dashboard → http://IP:5000
```

## 🔧 Tools
`Python 3.10` `Netmiko 4.6.0` `Flask` `Cisco IOS` `EVE-NG` `Ubuntu 22.04`
