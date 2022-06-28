import requests
import json
import pprint
import time
start_time = time.time()
device = {
   "ip": "10.6.249.4",
   "username": "cisco",
   "password": "cisco123",
}
headers = {
      "Accept" : "application/yang-data+json", 
      "Content-Type" : "application/yang-data+json", 
}
module = "Cisco-IOS-XE-native:native"
body= { 
    "Cisco-IOS-XE-nat:nat": [
    {
        "pool":{
            "id":"POOL-VLAN16",
            "start-address": "192.0.6.16",
            "end-address": "192.0.6.16",
            "netmask":"255.255.255.0"
        },
        "inside": {
            "source": {
                "list": {
                    "id": "10",
                    "pool":{
                        "name": "POOL-VLAN16", 
                        "overload": ""
                    }
                }
            }
        }
    }]
}
 
url = f"https://{device['ip']}:443/restconf/data/{module}/ip/Cisco-IOS-XE-nat:nat"

requests.packages.urllib3.disable_warnings()
response = requests.put(url, headers=headers, data=json.dumps(body), auth=(device['username'], device['password']), verify=False)


if (response.status_code == 204):
    print(response)
    print("Successfully added NAT entry")
else:
    print("Issue with adding NAT")
    print(response)
print("--- %s seconds ---" % (time.time() - start_time))