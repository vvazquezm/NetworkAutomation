import requests
import json
import pprint
import time
start_time = time.time()
device = {
   "ip": "10.6.249.3",
   "username": "cisco",
   "password": "cisco123",
}
headers = {
      "Accept" : "application/yang-data+json", 
      "Content-Type" : "application/yang-data+json", 
}
module = "Cisco-IOS-XE-native:native"
body= { 
    "Cisco-IOS-XE-native:access-list": {
        "Cisco-IOS-XE-acl:extended": [
            {
                "name": "TEST",
                "access-list-seq-rule": [
                    {
                        "sequence": "101",
                        "ace-rule": {
                            "action": "permit",
                            "protocol": "ip",
                            "ipv4-address": "10.100.100.0",
                            "mask": "0.0.0.255",
                            "dest-ipv4-address": "10.6.252.0",
                            "dest-mask": "0.0.3.255"
                            }
                        }
                    ]
                }
            ]
        }
    }
 
url = f"https://{device['ip']}:443/restconf/data/{module}/ip/access-list"

requests.packages.urllib3.disable_warnings()
response = requests.put(url, headers=headers, data=json.dumps(body), auth=(device['username'], device['password']), verify=False)

if (response.status_code == 204):
    print(response)
    print("Successfully added ACL entry")
else:
    print("Issue with adding ACL")
    print(response)
print("--- %s seconds ---" % (time.time() - start_time))