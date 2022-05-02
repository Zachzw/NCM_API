import os
import requests
import json

headers = {
    'X-CP-API-ID': os.environ['X-CP-API-ID'],
    'X-CP-API-KEY': os.environ['X-CP-API-KEY'],
    'X-ECM-API-ID': os.environ['X-ECM-API-ID'],
    'X-ECM-API-KEY': os.environ['X-ECM-API-KEY'],
    'Content-Type': 'application/json'
}

# list of router IDs
router_id = [1404724, 3083917]

# iterates through router_id, makes two API calls to for config manager endpoint and id
# writes router id and config manager id to rid_config_id dictionary
for r in router_id:
    url = f'https://www.cradlepointecm.com/api/v2/routers/?id__in={r}'
    rid = r
    r = requests.get(url, headers=headers)
    payload = r.json()

    # configuration manager value assigned to url var
    url = payload['data'][0]['configuration_manager']

    # API GET to configuration_manager endpoint
    r = requests.get(url, headers=headers)
    payload = r.json()

    # var for config id and assign payload to the nested list
    configuration_id = payload['id']
    payload = payload['configuration'][0]

    # tries to delete zfw section of the dictionary, if not found prints message to console
    try:
        del payload['security']['zfw']
    except KeyError:
        print(f'ZFW configuration does not exist on {rid}')
        continue

    payload = json.dumps(payload)

    # wraps payload with NCM API wrapper
    wrapped = '{"configuration": [' + payload + ', []]}'
    url = f'https://www.cradlepointecm.com/api/v2/configuration_managers/{configuration_id}/'

    # PUT pushing modified configuration to new group
    p = requests.put(url, data=wrapped, headers=headers)

    print(f'PUT Status Code:  {r.status_code} \nSuccessfully removed ZFW Options on Router: {rid}')
