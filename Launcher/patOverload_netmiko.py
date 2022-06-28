import cmd
from multiprocessing import pool
from netmiko import ConnectHandler
import csv
from tomlkit import string
from ipaddress import IPv4Address
import time


def keyboard_in (listing):
    inp_lst = []
    rang_lst = []
    data = []
    acls_num = 1
    print("You have selected keyboard configuration:")
    print(2 * '\n')
    check = input('Are inside and outside interfaces configured?\n \
                    [Y] - Configuration will be skipped \n \
                    [N] - Interfaces will be configured \n')
    if(check == 'N'):
        print(2* '\n')
        insider = input('Provide inside interface: \n')
        data.append(['interface '+insider,'ip nat inside'])
        outsider = input('Provide outside interface: \n')
        data.append(['interface '+outsider,'ip nat outside'])
    while True:
        net_priv = input('Provide a private network address and wildcard or press q to exit :\n')
        if(net_priv == 'q'):
            break
        else:
            while True:             #if ID for acls exists then +1
                if acls_num in listing:
                    acls_num += 1
                else: break
            inp_lst = net_priv.split('/')
            inp_lst[1] = str(IPv4Address(int(IPv4Address._make_netmask(inp_lst[1])[0])^(2**32-1)))  #Translates prefix length to wildcard
            data.append("access-list "+str(acls_num)+" permit "+inp_lst[0]+" "+inp_lst[1])
            tmp = input("Establish a public IP range and wildcard\n")
            rang_lst = tmp.split(' ')
            sv = rang_lst[2]
            sv = sv.replace('/','')
            sv = str(IPv4Address(int(IPv4Address._make_netmask(sv)[0])^(2**32-1)))              #Translates prefix length to wildcard
            sv = str(IPv4Address(int(IPv4Address(sv))^(2**32-1)))                               #Translates wildcard to netmask
            rang_lst[2] = sv
            inp_lst.extend(rang_lst)
            data.append("ip nat pool POOL-VLAN"+str(acls_num)+" "+rang_lst[0]+' '+rang_lst[1]+' netmask '+rang_lst[2])
            data.append("ip nat inside source list "+str(acls_num)+' pool POOL-VLAN'+str(acls_num)+' overload')
            listing.append(acls_num)
    return data

def file_in (filename):
    print('You have selected file input '+filename)
    with open(filename,encoding='utf-8-sig', mode='r') as pat_csv:
        pat_reader = csv.reader(pat_csv)
        data = []
        for row in pat_reader:
            info = [x.strip() for x in row[0].split(';')]
            if(info[0] == 'interface' or info[0] == 'int'):
                data.append([info[0]+' '+info[1],info[2]])
            elif(info[0] == 'access-list'):
                data.append(' '.join(str(x) for x in info))
            elif(info[0] == 'ip'):
                if(info[2] == 'pool'):
                    data.append(' '.join(str(x) for x in info))
                elif(info[3] == 'source'):
                    data.append(' '.join(str(x) for x in info))
    return data


with open('hosts_pat.csv',encoding='utf-8-sig', mode='r') as hosts_csv:
    csv_reader = csv.reader(hosts_csv)
    addon = 0 
    for row in csv_reader:
        if(addon == 0):
            DEVICE = {1: {'device_type':'','host':'','username':'','password':''}}
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
    net_connect = ConnectHandler(**host)
    config = []
    select = input('Select an input method: \n \
            [1] - Keyboard input\n \
            [2] - csv input, file name will be required\n')
    if(select == '1'):
        output = net_connect.send_command("show access-lists")
        interfaces = output.splitlines()
        listing = []
        for line in interfaces:
            if line == '' :
                continue
            else :
                sh_acl=line.split(' ')
                if(sh_acl[0] == 'Standard' or sh_acl[0] =='Extended'):
                    listing.append(int(sh_acl[4]))
                else:
                    continue
        config = keyboard_in(listing)
    else:
        fn = input('csv name: ')
        config = file_in(fn)
    start_time = time.time()
    for i in config :
        output = net_connect.send_config_set(i)
net_connect.disconnect()

print("--- %s seconds ---" % (time.time() - start_time))