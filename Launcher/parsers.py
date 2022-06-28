import csv

def parser_IP(c,addon,acls):
    acls[addon] = {}
    acls[addon]['ACL_num'] = c[0]
    acls[addon]['Access'] = c[1]
    acls[addon]['Protocol'] = c[2]
    acls[addon]['Source_IP'] = c[3]
    acls[addon]['Source_NM'] = c[4]
    acls[addon]['Dest_IP'] = c[5]
    acls[addon]['Dest_NM'] = c[6]
def parser_ICMP(c,addon,acls):
    acls[addon] = {}
    acls[addon]['ACL_num'] = c[0]
    acls[addon]['Access'] = c[1]
    acls[addon]['Protocol'] = c[2]
    acls[addon]['Source_IP'] = c[3]
    acls[addon]['Source_NM'] = c[4]
    acls[addon]['Dest_IP'] = c[5]
    acls[addon]['Dest_NM'] = c[6]
    acls[addon]['Icmp_tp'] = c [7]
def parser_TCP(c,addon,acls):
    acls[addon] = {}
    acls[addon]['ACL_num'] = c[0]
    acls[addon]['Access'] = c[1]
    acls[addon]['Protocol'] = c[2]
    acls[addon]['Source_IP'] = c[3]
    acls[addon]['Source_NM'] = c[4]
    acls[addon]['Operator_1'] = c [5]
    acls[addon]['Dest_IP'] = c[6]
    acls[addon]['Dest_NM'] = c[7]
    acls[addon]['Operator_2'] = c [8]
    acls[addon]['Established'] = c [9]
def parser_UDP(c,addon,acls):
    acls[addon] = {}
    acls[addon]['ACL_num'] = c[0]
    acls[addon]['Access'] = c[1]
    acls[addon]['Protocol'] = c[2]
    acls[addon]['Source_IP'] = c[3]
    acls[addon]['Source_NM'] = c[4]
    acls[addon]['Operator_1'] = c [5]
    acls[addon]['Dest_IP'] = c[6]
    acls[addon]['Dest_NM'] = c[7]
    acls[addon]['Operator_2'] = c [8]
def parser_general(csv_name):
    with open(csv_name,encoding='utf-8-sig', mode='r') as acls_csv:
        acls_reader = csv.reader(acls_csv)
        acls = {}
        addon = 0
        for row in acls_reader:
            if (addon == 0):
                addon += 1
                continue
            else:
                content = [x.strip() for x in row[0].split(';')]
                if(content[2] == 'ip'):
                    parser_IP(content,addon,acls)
                elif(content[2] == 'icmp'):
                    parser_ICMP(content,addon,acls)
                elif(content[2] == 'tcp'):
                    parser_TCP(content,addon,acls)
                elif(content[2] == 'udp'):
                    parser_UDP(content,addon,acls)
                addon += 1
    return acls
parser_general('acls.csv')