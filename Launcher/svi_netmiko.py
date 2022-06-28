from asyncore import read
from netmiko import ConnectHandler
import csv
import time
def keyboard_in ():
    dict_key = input('Specify the first VLAN:\n')
    vals = input("Specify the VLAN's IP and wildcard:\n")
    vals_splited = vals.split(' ')
    vlans_dict = {dict_key : {'IP': vals_splited[0],'Masc': vals_splited[1]}}       #first iteration of input
    while(True):        #loop to get user input
        dict_key = input('Specify the next VLAN or press q to quit:\n')
        if(dict_key == 'q'):
            break
        else:
            vals = input("Specify the VLAN's IP and wildcard:\n")
            vals_splited = vals.split(' ') 
            vlans_dict[dict_key] = {'IP': vals_splited[0],'Masc': vals_splited[1]}      #Set Vlan as dict key and IP and wildcard as value
    return vlans_dict


with open('hosts_svi.csv',encoding='utf-8-sig', mode='r') as hosts_csv: #Read specific csv
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

vlans_dict = keyboard_in()
start_time = time.time()
conf_cmds_list = []
conf_cmds = []
for vlan,p_info in vlans_dict.items():      #Get dict info and create the command
    conf_cmds = ["vlan "+str(vlan),"exit","interface vlan "+ str(vlan),"no shutdown","ip address "+str(p_info['IP'])+" "+str(p_info['Masc']),"exit"]
    conf_cmds_list.append(conf_cmds)
for num,host in DEVICE.items():
    net_connect = ConnectHandler(**host)
    output = net_connect.send_command("show protocols")
    print('+++++++++++++++++++++++++++BEFORE COMMAND EXECUTION+++++++++++++++++++++++++++++++')
    print(output)
    for command in conf_cmds_list:
        net_connect.send_config_set(command)
    print('+++++++++++++++++++++++++++AFTER COMMAND EXECUTION+++++++++++++++++++++++++++++++')
    output = net_connect.send_command("show protocols")
    print(output)
net_connect.disconnect()

print("--- %s seconds ---" % (time.time() - start_time))