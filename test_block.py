from fortigate.fortigate_api import FortigateAPI
from config import FORTIGATE_IP, FORTIGATE_KEY


fg = FortigateAPI(host=FORTIGATE_IP, api_key=FORTIGATE_KEY)


# ── اختبار 1: احجب IP ──
print("=== Blocking IP ===")
result = fg.block_ip("10.10.10.10")
print(f"IP: {result['ip']}")
print(f"Address created: {result['address_status']}")
print(f"Policy created : {result['policy_status']}")

# ── اختبار 2: شوف الـ IPs المحجوبة ──
print("\n=== Blocked IPs ===")
blocked = fg.get_blocked_ips()
if blocked:
    for item in blocked:
        print(f"  ❌ {item['ip']}")
else:
    print("  No blocked IPs")

# ── اختبار 3: رفع الحجب ──
print("\n=== Unblocking IP ===")
result = fg.unblock_ip("10.10.10.10")
print(f"  ✅ {result['ip']} → {result['status']}")