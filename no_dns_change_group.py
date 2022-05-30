import requests
import json
import os
import time

# edit these variables to include local ip and local router credentials, router ids, group ids
local_ip = ''
username = ''
password = ''
group_a_id = ''
group_b_id = ''
router_id = ''

# vars for Group URLs, router IDs, and r_url for initial get
# update group a vars for your environment
group_a = f'https://www.cradlepointecm.com/api/v2/groups/{group_a_id}/'
move_to_group_a = f'{"group" : "https://cradlepointecm.com/api/v2/groups/{group_a_id}/"}'

# update group b vars for your environment
group_b = f'https://www.cradlepointecm.com/api/v2/groups/{group_b_id}/'
move_to_group_b = f'{"group" : "https://cradlepointecm.com/api/v2/groups/{group_b_id}/"}'

# enter router url with router id
r_url = f'https://www.cradlepointecm.com/api/v2/routers/{router_id}/'

# api headers
headers = {
    'X-CP-API-ID': os.environ['X-CP-API-ID'],
    'X-CP-API-KEY': os.environ['X-CP-API-KEY'],
    'X-ECM-API-ID': os.environ['X-ECM-API-ID'],
    'X-ECM-API-KEY': os.environ['X-ECM-API-KEY'],
    'Content-Type': 'application/json'
}


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
        time.sleep(600)
        continue
    else:
        # conditional to tell the router to alternate between groups
        if gid != group_a:
            put = requests.put(r_url, data=move_to_group_a,  headers=headers)
            print(f'Moved Router to group {group_a} \n Status Code: {put.status_code}')
            time.sleep(600)
            continue
        else:
            put = requests.put(r_url, data=move_to_group_b, headers=headers)
            print(f'Moved Router to group {group_b} \n Status Code: {put.status_code}')
            time.sleep(600)
            continue
