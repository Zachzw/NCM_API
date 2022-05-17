import requests
import json
import os
import time

# vars for Group URLs, router IDs, and r_url for initial get
# update group a vars for your environment
group_a = 'https://www.cradlepointecm.com/api/v2/groups/[Group ID]/'
move_to_group_a = '{"group" : "https://cradlepointecm.com/api/v2/groups/[Group ID]/"}'

# update group b vars for your environment
group_b = 'https://www.cradlepointecm.com/api/v2/groups/[Group ID]/'
move_to_group_b = '{"group" : "https://cradlepointecm.com/api/v2/groups/[Group ID]/"}'

# enter router url with router id
r_url = 'https://www.cradlepointecm.com/api/v2/routers/[Router ID]/'

# api headers
headers = {
    'X-CP-API-ID': os.environ['X-CP-API-ID'],
    'X-CP-API-KEY': os.environ['X-CP-API-KEY'],
    'X-ECM-API-ID': os.environ['X-ECM-API-ID'],
    'X-ECM-API-KEY': os.environ['X-ECM-API-KEY'],
    'Content-Type': 'application/json'
}

# edit these variables to include local ip and local router credentials
local_ip = '192.168.0.1'
username = 'admin'
password = 'password1'

# while loop to query local router api, if router is offline in NCM, move it between groups
while True:
    r = requests.get(url=f'http://{local_ip}/api/status/ecm/', auth=(f'{username}', f'{password}'))
    g = requests.get(r_url, headers=headers)
    gid = g.json()
    payload = r.json()
    state = payload['data']['state']
    gid = gid['group']
    if state != 'connected':
        print('Router is offline in NCM')
        time.sleep(5)
        continue
    else:
        # conditional to tell the router to alternate between groups
        if gid != group_a:
            put = requests.put(r_url, data=move_to_group_a,  headers=headers)
            print(f'Moved Router to group {group_a} \n Status Code: {put.status_code}')
            time.sleep(5)
            continue
        else:
            put = requests.put(r_url, data=move_to_group_b, headers=headers)
            print(f'Moved Router to group {group_b} \n Status Code: {put.status_code}')
            time.sleep(5)
            continue



