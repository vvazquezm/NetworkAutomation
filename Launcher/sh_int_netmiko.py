from asyncore import read
from netmiko import ConnectHandler
import csv
import time
start_time = time.time()    
with open('hosts_shutdown.csv',encoding='utf-8-sig', mode='r') as hosts_csv:    #Read specify csv
    csv_reader = csv.reader(hosts_csv)
    addon = 0 
    for row in csv_reader:
        if(addon == 0):
            DEVICE = {1: {'device_type':'','host':'','username':'','password':''}}  #Get csv's first line and set it as dict fields
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
    print("Interfaces before shutdown")
    output = net_connect.send_command("show int status | inc notconn")
    interfaces = output.splitlines()           #Get whole output and split it in lines
    for line in interfaces: 
        if line == '' :
            continue
        else :
            comandos_config = ["interface {}".format(line.split()[0]),"shutdown"]   
            s_output = net_connect.send_config_set(comandos_config)
    final = net_connect.send_command("show int status")
    print("Interfaces after shutdown")
    print(final)
net_connect.disconnect()
print("--- %s seconds ---" % (time.time() - start_time))