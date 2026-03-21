from fortigate.fortigate_api import FortigateAPI
from config import FORTIGATE_IP, FORTIGATE_KEY


fg = FortigateAPI(host=FORTIGATE_IP, api_key=FORTIGATE_KEY)



print("=== Interfaces ===")
interfaces = fg.get_interfaces()
for iface in interfaces["results"]:
    print(f"  {iface['name']} → {iface['ip']}")

print("\n=== Firewall Policies ===")
policies = fg.get_policies()
for policy in policies["results"]:
    print(f"  [{policy['policyid']}] {policy['name']}")
