import requests
import urllib3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
urllib3.disable_warnings()

from config import FORTIGATE_IP, FORTIGATE_KEY, ABUSEIPDB_KEY
from fortigate.fortigate_api import FortigateAPI

fg = FortigateAPI(host=FORTIGATE_IP, api_key=FORTIGATE_KEY)

def get_malicious_ips(limit=10, confidence=90):
    """سحب IPs خطيرة من AbuseIPDB"""
    headers = {
        "Key": ABUSEIPDB_KEY,
        "Accept": "application/json"
    }
    params = {
        "confidenceMinimum": confidence,
        "limit": limit
    }
    response = requests.get(
        "https://api.abuseipdb.com/api/v2/blacklist",
        headers=headers,
        params=params,
        timeout=15
    )
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        return [item["ipAddress"] for item in data["data"]]
    elif response.status_code == 422:
        print("  ❌ API Key غير صحيح أو الـ plan لا يدعم blacklist")
        return []
    else:
        print(f"  ❌ Error: {response.status_code} — {response.text}")
        return []

def run_threat_feed():
    print("=" * 40)
    print("  Threat Intelligence Feed")
    print("=" * 40)

    # سحب الـ IPs الخطيرة
    print("\n[1] Fetching malicious IPs from AbuseIPDB...")
    ips = get_malicious_ips(limit=10, confidence=90)

    if not ips:
        print("❌ No IPs fetched — check API key")
        return

    print(f"✅ Fetched {len(ips)} malicious IPs")

    # الـ IPs المحجوبة مسبقاً
    already_blocked = [item["ip"] for item in fg.get_blocked_ips()]

    # حجب كل IP جديد
    print("\n[2] Blocking IPs on Fortigate...")
    blocked_count = 0
    skipped_count = 0

    for ip in ips:
        if ip in already_blocked:
            print(f"  ⏭️  {ip} — already blocked")
            skipped_count += 1
        else:
            result = fg.block_ip(ip)
            if result["policy_status"] == 200:
                print(f"  ❌ {ip} — blocked ✅")
                blocked_count += 1
            else:
                print(f"  ⚠️  {ip} — error {result['policy_status']}")

    # ملخص
    print("\n" + "=" * 40)
    print(f"  Blocked  : {blocked_count} IPs")
    print(f"  Skipped  : {skipped_count} IPs (already blocked)")
    print(f"  Total    : {len(ips)} IPs fetched")
    print("=" * 40)

if __name__ == "__main__":
    run_threat_feed()