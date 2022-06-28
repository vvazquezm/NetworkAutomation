from asyncore import read
from netmiko import ConnectHandler
import csv
import time

vlans_raw = input("Specify wanted VLANs separated by ';'. Use '-' for ranges:\n")
vlans_refined = []      #initializing vlans lists
vlans_range = []        #initializing vlans range list

if(vlans_raw == '' or vlans_raw ==' '):
    while(vlans_raw == '' or vlans_raw == ' '):
        vlans_raw = input("specify wanted VLANs separated by ';'. Use '-' for ranges:\n")
    
start_time = time.time()       
vlans_refined = [line.strip() for line in vlans_raw.split(';')]     #extracting user input
for x in vlans_refined:
    if('-' in x):           
        vlans_refined.remove(x)         
        tmp_range = x.split('-')
        tmp_range2 = list(range(int(tmp_range[0]),int(tmp_range[1])+1))     #generate vlans within defined range
        vlans_refined = vlans_refined + tmp_range2          #concatenate the 2 lists
        vlans_refined = list(map(int, vlans_refined))       #check for duplicates and sort the list
conf_cmds = []
for vlan in vlans_refined:
    if conf_cmds:
        command_p1 = "vlan "+str(vlan)
        command_p2 = "name netmiko vlan "+str(vlan)
        conf_cmds.append(command_p1)
        conf_cmds.append(command_p2)
        conf_cmds.append("exit")
    else:
        conf_cmds = ["vlan "+ str(vlan),"name netmiko vlan "+str(vlan),"exit"]
with open('hosts_vlans.csv',encoding='utf-8-sig', mode='r') as hosts_csv:   #Read specific csv
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
        net_connect = ConnectHandler(**host)         #Netmiko connection function
        print("VLANs before execution:")
        output = net_connect.send_command("show vlan brief")
        print(output)
        s_output = net_connect.send_config_set(conf_cmds)
        final = net_connect.send_command("show vlan brief")
        print("VLANs after execution:")
        print("")
        print(final)
    
net_connect.disconnect()

print("--- %s seconds ---" % (time.time() - start_time))