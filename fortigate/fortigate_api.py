import requests
import urllib3
urllib3.disable_warnings()

class FortigateAPI:
    def __init__(self, host, api_key):
        self.host = host
        self.api_key = api_key
        self.base_url = f"https://{host}/api/v2"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def get_interfaces(self):
        response = requests.get(
            f"{self.base_url}/cmdb/system/interface",
            headers=self.headers,
            verify=False
        )
        return response.json()

    def get_policies(self):
        response = requests.get(
            f"{self.base_url}/cmdb/firewall/policy",
            headers=self.headers,
            verify=False
        )
        return response.json()

    def backup_config(self):
        response = requests.get(
            f"{self.base_url}/monitor/system/config/backup?scope=global",
            headers=self.headers,
            verify=False
        )
        return response.text

    # ── Block IP ──────────────────────────────
    def block_ip(self, ip):
        # أولاً — أنشئ Address Object للـ IP
        address_payload = {
            "name": f"blocked-{ip}",
            "type": "ipmask",
            "subnet": f"{ip}/32"
        }
        addr_response = requests.post(
            f"{self.base_url}/cmdb/firewall/address",
            headers=self.headers,
            json=address_payload,
            verify=False
        )

        # ثانياً — أنشئ Policy تحجب هذا الـ IP
        policy_payload = {
            "name": f"block-{ip}",
            "srcintf": [{"name": "port1"}],
            "dstintf": [{"name": "port2"}],
            "srcaddr": [{"name": f"blocked-{ip}"}],
            "dstaddr": [{"name": "all"}],
            "action": "deny",
            "schedule": "always",
            "service": [{"name": "ALL"}],
            "logtraffic": "all"
        }
        policy_response = requests.post(
            f"{self.base_url}/cmdb/firewall/policy",
            headers=self.headers,
            json=policy_payload,
            verify=False
        )

        return {
            "ip": ip,
            "address_status": addr_response.status_code,
            "policy_status": policy_response.status_code
        }

    # ── Unblock IP ────────────────────────────
    def unblock_ip(self, ip):
        # احذف الـ Policy أولاً
        policies = self.get_policies()
        for policy in policies["results"]:
            if policy["name"] == f"block-{ip}":
                requests.delete(
                    f"{self.base_url}/cmdb/firewall/policy/{policy['policyid']}",
                    headers=self.headers,
                    verify=False
                )

        # ثم احذف الـ Address Object
        requests.delete(
            f"{self.base_url}/cmdb/firewall/address/blocked-{ip}",
            headers=self.headers,
            verify=False
        )

        return {"ip": ip, "status": "unblocked"}

    # ── Get Blocked IPs ───────────────────────
    def get_blocked_ips(self):
        response = requests.get(
            f"{self.base_url}/cmdb/firewall/address",
            headers=self.headers,
            verify=False
        )
        blocked = []
        for addr in response.json()["results"]:
            if addr["name"].startswith("blocked-"):
                blocked.append({
                    "ip": addr["name"].replace("blocked-", ""),
                    "subnet": addr["subnet"]
                })
        return blocked