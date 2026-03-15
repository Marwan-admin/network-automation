from flask import Flask, jsonify, render_template_string
import subprocess
import datetime
from devices import DEVICES
from netmiko import ConnectHandler

app = Flask(__name__)

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

@app.route("/")
def index():
    return render_template_string(open("templates/index.html").read())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)