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

# url var & urlencoding
url = f'https://www.cradlepointecm.com/api/v2/configuration_managers/?router__in={router_id}'

# get req to grab all config ID's are once
r = requests.get(url, headers=headers)
payload = r.json()
payload = payload['data']
# var for loop
x = 0

for r in payload:
    rid = r['router']
    cid = r['id']
    req = requests.get(url, headers=headers)
    loop_payload = req.json()
    # try except to allow script to function when the for loops reach last item in payload
    try:
        loop_payload = loop_payload['data'][x]['configuration'][0]
    except:
        loop_payload = loop_payload['configuration'][0]

    #tries to delete zfw section of the dictionary, if not found prints message to console
    try:
        del loop_payload['security']['zfw']
        delete = True
        x += 1
    except:
        print(f'ZFW configuration does not exist on Router: {rid}')
        x += 1
        continue

    # encodes JSON to a s tring
    payload = json.dumps(loop_payload)

    # wraps payload with NCM API wrapper
    wrapped = '{"configuration": [' + payload + ', []]}'
    url = f'https://www.cradlepointecm.com/api/v2/configuration_managers/{cid}/'
    # PUT pushing modified configuration to new group
    p = requests.put(url, data=wrapped, headers=headers)

    print(f'PUT Status Code:  {p.status_code} \nSuccessfully removed ZFW Options on Router: {rid}')
    continue
