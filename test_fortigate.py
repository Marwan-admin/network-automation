from fortigate.fortigate_api import FortigateAPI

fg = FortigateAPI(
    host="192.168.8.29",
    api_key="ffGzfzhfzcz0q0NHj19dgd615dNtxx"
)

print("=== Interfaces ===")
interfaces = fg.get_interfaces()
for iface in interfaces["results"]:
    print(f"  {iface['name']} → {iface['ip']}")

print("\n=== Firewall Policies ===")
policies = fg.get_policies()
for policy in policies["results"]:
    print(f"  [{policy['policyid']}] {policy['name']}")
