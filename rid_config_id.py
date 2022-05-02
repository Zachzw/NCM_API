import requests
import json

# headers for NCM API
headers = {
    'X-CP-API-ID': 'xx',
    'X-CP-API-KEY': 'xx',
    'X-ECM-API-ID': 'xx',
    'X-ECM-API-KEY': 'xx',
    'Content-Type': 'application/json'
}
# list of router IDs
router_id = [1, 2]
# creating dictionary as this is where the Router ID to Configuration Manager mapping will be stored
rid_config_id = {}

# iterates through router_id, makes two API calls to for config manager endpoint and id
# writes router id and config manager id to rid_config_id dictionary
for r in router_id:
    url = f'https://www.cradlepointecm.com/api/v2/routers/?id__in={r}'
    # x = r
    req = requests.get(url, headers=headers)
    payload = req.json()
    payload = payload['data'][0]['configuration_manager']
    req = requests.get(payload, headers=headers)
    payload = req.json()
    rid_config_id[f'Router ID: {r}'] = f"Configuration Manager ID: {payload['id']}"

print(rid_config_id)