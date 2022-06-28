from asyncore import read
from netmiko import ConnectHandler
from parsers import parser_general
import csv
import time
start_time = time.time()
acls = []
acls = parser_general('acls.csv')       #Parser acls
stringer = 'access-list'
conf_cmds = []
for p_id, p_info in acls.items():
    for item in p_info:
        stringer += ' ' + str(p_info[item])     #append strings to create command
    conf_cmds.append(stringer)                  #save them in only one list to send them all at once
    stringer = 'access-list'

with open('hosts_acls.csv',encoding='utf-8-sig', mode='r') as hosts_csv:        #Read specify csv
    csv_reader = csv.reader(hosts_csv)
    addon = 0 
    for row in csv_reader:
        if(addon == 0):
            DEVICE = {1: {'device_type':'','host':'','username':'','password':''}}      #Get csv's first line and set it as dict fields
            addon += 1
        else:
            info = [x.strip() for x in row[0].split(';')]
            DEVICE[addon] = {}
            DEVICE[addon]['device_type'] = info[0]
            DEVICE[addon]['host'] = info[1]
            DEVICE[addon]['username'] = info[2]
            DEVICE[addon]['password'] = info[3]
            addon += 1
for num,host in DEVICE.items():
    net_connect = ConnectHandler(**host)        #Netmiko connection function
    output = net_connect.send_command("show access-list")
    print("Existing ACLs before execution: ")
    print(output)
    s_output = net_connect.send_config_set(conf_cmds)        #Send ACLs
    output = net_connect.send_command("show access-list")           
    print("Existing ACLs after execution: ")
    print(output)
net_connect.disconnect()
print("--- %s seconds ---" % (time.time() - start_time))
