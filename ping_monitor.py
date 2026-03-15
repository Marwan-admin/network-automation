import subprocess
import time
import datetime

DEVICES = {
    "R1": "192.168.8.10",
    "SW1": "192.168.8.20",
    "Ubuntu": "192.168.8.30",
    "GW": "192.168.8.1",
}

STATUS = {name: True for name in DEVICES}

def ping(ip):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", ip],
        capture_output=True
    )
    return result.returncode == 0

def check_all():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"\n[{now}] Checking devices...")
    print("-" * 40)
    for name, ip in DEVICES.items():
        reachable = ping(ip)
        status = "UP  " if reachable else "DOWN"
        if STATUS[name] != reachable:
            if not reachable:
                print(f"  ALERT: {name} ({ip}) went DOWN!")
            else:
                print(f"  RECOVERY: {name} ({ip}) is back UP!")
            STATUS[name] = reachable
        print(f"  {status} | {name:10} | {ip}")
    up = sum(STATUS.values())
    print("-" * 40)
    print(f"  Summary: {up}/{len(DEVICES)} devices UP")

def main():
    print("=" * 40)
    print("   Network Monitor Started")
    print("   Press Ctrl+C to stop")
    print("=" * 40)
    while True:
        check_all()
        time.sleep(30)

if __name__ == "__main__":
    main()