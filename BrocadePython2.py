import sys
import time
import getpass
import xmltodict
import http.client as http
import pyfos.pyfos_auth as auth
#import xml.etree.ElementTree as ET

Environments = ['Prod', 'DR', 'DEV']

if len(sys.argv) == 3:
    SW_Username = sys.argv[0]
    SW_Password = sys.argv[1]
    Environment = sys.argv[2]
else:
    print("Incorrect number of arguments provided...")
    SW_Username = input("Please provide the switch username")
    SW_Password = getpass.getpass("Please provide the switch password")
    while Environment not in Environments:
        Environment = input("Please provide the environment (Prod, DR, Test)")

if Environment == "Prod":
    SW1_IP = "IP"
    SW2_IP = "IP"
if Environment == "DR":
    SW1_IP = "IP"
    SW2_IP = "IP"
if Environment == "DEV":
    SW1_IP = "10.92.238.99"
    SW2_IP = "10.92.238.100"

#Connecting to Switch1
SW1_Session = auth.login(SW_Username, SW_Password, SW1_IP, "None")
#Connecting to Switch2
SW2_Session = auth.login(SW_Username, SW_Password, SW2_IP, "None")

#Building Switch 1 REST header
header1 = SW1_Session.get('credential')
header1.update({'Accept': 'application/yang-data+xml'})
header1.update({'Content-Type': 'application/yang-data+xml'})
ip1 = SW1_Session.get("ip_addr")

#Building Switch 2 REST header
header2 = SW2_Session.get('credential')
header2.update({'Accept': 'application/yang-data+xml'})
header2.update({'Content-Type': 'application/yang-data+xml'})
ip2 = SW2_Session.get("ip_addr")

#Getting port list from Switch 1
SW1_Connection = http.HTTPConnection(ip1)
method = "GET"
URI = "/rest/running/brocade-interface/fibrechannel"
Body = None
SW1_Connection.request(method, URI, Body, header1)

if SW1_Session.get('throttle_delay') > 0:
    time.sleep(SW1_Session.get('throttle_delay'))
response1 = SW1_Connection.getresponse()

Data = response1.read()
doc = xmltodict.parse(Data)

for i in range(0, len(doc['Response']['fibrechannel'])):
    doc['Response']['fibrechannel'][i]['user-friendly-name']

#Getting port list from Switch 2


#Closing session on Switch 1
auth.logout(SW1_Session)
#Closing session on Switch 2
auth.logout(SW2_Session)