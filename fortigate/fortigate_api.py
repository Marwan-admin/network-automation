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
