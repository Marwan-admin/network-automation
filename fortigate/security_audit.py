import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import FORTIGATE_IP, FORTIGATE_KEY
from fortigate.fortigate_api import FortigateAPI
import requests
import urllib3
urllib3.disable_warnings()

fg = FortigateAPI(host=FORTIGATE_IP, api_key=FORTIGATE_KEY)

def check_admin_access():
    """تحقق من إعدادات الـ Admin Access"""
    print("\n[1] Checking Admin Access...")
    response = requests.get(
        f"https://{FORTIGATE_IP}/api/v2/cmdb/system/interface",
        headers=fg.headers,
        verify=False
    )
    issues = []
    for iface in response.json()["results"]:
        access = iface.get("allowaccess", "")
        if "telnet" in access:
            issues.append(f"  ⚠️  {iface['name']} — Telnet enabled (insecure!)")
        if "http" in access:
            issues.append(f"  ⚠️  {iface['name']} — HTTP enabled (use HTTPS)")
        if "ping" in access and iface["name"] == "port1":
            issues.append(f"  ℹ️  {iface['name']} — Ping enabled on WAN")

    if issues:
        for i in issues:
            print(i)
    else:
        print("  ✅ Admin access looks good")
    return issues

def check_firewall_policies():
    """تحقق من الـ Firewall Policies"""
    print("\n[2] Checking Firewall Policies...")
    policies = fg.get_policies()
    issues = []
    for policy in policies["results"]:
        name = policy["name"]
        src  = policy["srcaddr"][0]["name"]
        dst  = policy["dstaddr"][0]["name"]
        svc  = policy["service"][0]["name"]
        action = policy["action"]

        # Policy مفتوحة كلياً
        if src == "all" and dst == "all" and svc == "ALL" and action == "accept":
            issues.append(f"  ⚠️  Policy [{policy['policyid']}] '{name}' — too permissive (all→all)")

        # Policy بدون logging
        if policy.get("logtraffic") == "disable":
            issues.append(f"  ⚠️  Policy [{policy['policyid']}] '{name}' — logging disabled")

    if issues:
        for i in issues:
            print(i)
    else:
        print("  ✅ Policies look good")
    return issues

def check_dns():
    """تحقق من إعدادات الـ DNS"""
    print("\n[3] Checking DNS Settings...")
    response = requests.get(
        f"https://{FORTIGATE_IP}/api/v2/cmdb/system/dns",
        headers=fg.headers,
        verify=False
    )
    data = response.json().get("results", {})
    primary   = data.get("primary", "N/A")
    secondary = data.get("secondary", "N/A")
    print(f"  Primary DNS   : {primary}")
    print(f"  Secondary DNS : {secondary}")
    issues = []
    if primary == "0.0.0.0":
        issues.append("  ⚠️  Primary DNS not configured")
    return issues

def check_blocked_ips():
    """عرض الـ IPs المحجوبة"""
    print("\n[4] Checking Blocked IPs...")
    blocked = fg.get_blocked_ips()
    if blocked:
        print(f"  ❌ {len(blocked)} IPs currently blocked:")
        for item in blocked:
            print(f"     {item['ip']}")
    else:
        print("  ℹ️  No IPs blocked")
    return blocked

def run_audit():
    print("=" * 45)
    print("       Fortigate Security Audit Report")
    print("=" * 45)
    print(f"  Target : {FORTIGATE_IP}")

    all_issues = []
    all_issues += check_admin_access()
    all_issues += check_firewall_policies()
    all_issues += check_dns()
    check_blocked_ips()

    # ملخص النتائج
    print("\n" + "=" * 45)
    print("  SUMMARY")
    print("=" * 45)
    if all_issues:
        print(f"  ⚠️  Found {len(all_issues)} issue(s):\n")
        for issue in all_issues:
            print(issue)
    else:
        print("  ✅ No issues found — Firewall looks secure!")
    print("=" * 45)

if __name__ == "__main__":
    run_audit()
