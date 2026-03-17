from flask import Flask, jsonify, render_template_string
import subprocess
import datetime
from devices import DEVICES
from netmiko import ConnectHandler
from fortigate.fortigate_api import FortigateAPI

app = Flask(__name__)

FG = FortigateAPI(
    host="192.168.8.29",
    api_key="ffGzfzhfzcz0q0NHj19dgd615dNtxx"
)

def ping(ip):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", ip],
        capture_output=True
    )
    return result.returncode == 0

def ssh_command(device_name, command):
    conn = ConnectHandler(**DEVICES[device_name])
    conn.enable()
    output = conn.send_command(command)
    conn.disconnect()
    return output

DEVICE_IPS = {
    "R1": "192.168.8.10",
    "SW1": "192.168.8.20",
}

# ── Cisco Routes ──────────────────────────────

@app.route("/api/status")
def status():
    result = []
    for name, ip in DEVICE_IPS.items():
        result.append({
            "name": name,
            "ip": ip,
            "status": "up" if ping(ip) else "down"
        })
    return jsonify(result)

@app.route("/api/interfaces/<device>")
def interfaces(device):
    try:
        output = ssh_command(device, "show ip interface brief")
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/vlans")
def vlans():
    try:
        output = ssh_command("SW1", "show vlan brief")
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/backup/<device>", methods=["POST"])
def backup(device):
    try:
        conn = ConnectHandler(**DEVICES[device])
        conn.enable()
        config = conn.send_command("show running-config")
        conn.disconnect()
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"backups/{device}_{ts}.cfg"
        with open(fname, "w") as f:
            f.write(config)
        return jsonify({"status": "success", "file": fname})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Fortigate Routes ──────────────────────────

@app.route("/api/fortigate/interfaces")
def fg_interfaces():
    try:
        data = FG.get_interfaces()
        result = []
        for iface in data["results"]:
            result.append({
                "name": iface["name"],
                "ip": iface["ip"],
                "status": iface["status"]
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/fortigate/policies")
def fg_policies():
    try:
        data = FG.get_policies()
        result = []
        for policy in data["results"]:
            result.append({
                "id": policy["policyid"],
                "name": policy["name"],
                "srcintf": policy["srcintf"][0]["name"],
                "dstintf": policy["dstintf"][0]["name"],
                "action": policy["action"]
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/fortigate/backup", methods=["POST"])
def fg_backup():
    try:
        config = FG.backup_config()
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"backups/fortigate_{ts}.cfg"
        with open(fname, "w") as f:
            f.write(config)
        return jsonify({"status": "success", "file": fname})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Dashboard ─────────────────────────────────

@app.route("/")
def index():
    return render_template_string(open("templates/index.html").read())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)