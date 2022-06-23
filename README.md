
# Network automation

This repository contains some examples of network automation developed in 3 different technologies.
These are the following:

- Netmiko
- Ansible
- Restconf

All of the examples are designed to run on Cisco IOS devices. These were simulated in
A development environment so IPs, users and passwords are stored in plain text data.


## Features
In it there are the following features:

- Shutdown not connected interfaces in switches
- Create Vlans
- Create SVI
- Deploy ACLs in Cisco routers
- Configure NAT Overload [PAT]

Some of it may not be implemented in some of the selected technologies.

## Run Locally

Clone the project

```bash
  git clone https://github.com/vvazquezm/NetworkAutomation.git
```

Go to the project directory

```bash
  cd Launcher
```

Install dependencies

```bash
  pip install requests
  pip install netmiko
```

Start the tool launcher

```bash
  python3 launcher.py
```


## Usage/Examples
It's important to keep in mind that this is just an example tool. For normal use
some configuration may be required.

First of all, Netmiko *. csvs* need to contain the following host's connection data:

  - OS
  - User
  - Password
  - IP address

A new hosts_file.ini need to be implemented to be able to use Ansible's features

The following field needs to be reconfigured in Restconf examples:
```python
device = {
   "ip": "XXX.XXX.XXX.XXX",
   "username": "user",
   "password": "password",
}
```

