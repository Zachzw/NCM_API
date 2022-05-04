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
router_id = '1404724, 3083917'

# base url var
base_url = 'https://www.cradlepointecm.com/api/v2/configuration_managers/?router__in='
# url var combining base url and router_id list
url = f'{base_url}{router_id}'


# get req to grab all config ID's as one call
r = requests.get(url, headers=headers)
payload = r.json()

# for loop to iterate through payload, extract router ID, Configuration ID and assign to f
for f in payload['data']:
    rid = f['router']
    cid = f['id']
    # for loop to grab configuration, delete security object, then push config to router in NCM
    for g in f['configuration']:
        l = (len(g))
        if l <= 0:
            continue
        else:
            try:
                del g['security']
            except (NameError, KeyError):
                print(f'ZFW configuration does not exist on Router: {rid}')
                continue
        payload = json.dumps(g)
        # wraps payload with NCM API wrapper
        wrapped = '{"configuration": [' + payload + ', []]}'
        url = f'https://www.cradlepointecm.com/api/v2/configuration_managers/{cid}/'
        # PUT pushing modified configuration to router configuration manager
        p = requests.put(url, data=wrapped, headers=headers)
        print(f'PUT Status Code:  {p.status_code} \nSuccessfully removed ZFW Options on Router: {rid}')
        continue
    else:
        continue
