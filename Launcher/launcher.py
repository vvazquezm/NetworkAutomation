import pathlib
import os
from select import select
import time

def help(width):
    print("-----------------------------------Script Launcher-----------------------------------\n")
    print("           Avaliable commands: \n\
                            H: help\n\
                            C: print scripts \n\
                            R + script_name: run \n\
                            Q: quit".center(width))

def printer(scripts):
    netm = []
    ans = []
    rest = []
    for f in scripts:
        if("requests" in f):
            rest.append(f)
        elif("netmiko" in f):
            netm.append(f)
        else:
            ans.append(f)
    print("-----------------------------RESTCONF--------------------------------")
    print("\n")
    for elem in rest:
        print(elem)
    print("\n")
    print("-----------------------------NETMIKO--------------------------------")
    print("\n")
    for elem in netm:
        print(elem)
    print("\n")
    print("-----------------------------ANSIBLE--------------------------------")
    print("\n")
    for elem in ans:
        print(elem)
def Selection():
    width = os.get_terminal_size().columns
    print(2* "\n")
    print("-----------------------------------Script Launcher-----------------------------------\n")
    print("           Avaliable commands: \n\
                            H: help\n\
                            C: print scripts \n\
                            R + scrip_name: run \n\
                            Q: quit".center(width))
    while True:
        width = os.get_terminal_size().columns
        print(3* "\n")
        choice = input("Choose desired action:")
        choice = choice.split(' ')
        if(choice[0] == 'H'):
            help(width)
        elif(choice[0] == 'C'):
            path = pathlib.Path(__file__).parent.resolve()
            files = os.listdir(path)
            print(2*"\n")
            print("Avaliable scripts: ")
            print(2*"\n")
            script = []
            for f in files:
                if(f.endswith(".py") or f.endswith(".yml")):
                    if("launcher" not in f):
                        if("parser" not in f):
                            script.append(f)
            printer(script)
                    #print(f)
        elif(choice[0] == 'R'):
            if choice[1].endswith(".py"):
                start_time = time.time()
                os.system("python3 "+choice[1])
            else:
                start_time = time.time()
                os.system("ansible-playbook -i host_file.ini "+choice[1]+" -e 'ansible_python_interpreter=/usr/bin/python3'")
                print("--- %s seconds ---" % (time.time() - start_time))                
        elif(choice[0] == 'Q'):
            break
        else:help(width)

def main():
    Selection()

if __name__ == "__main__":
    main()