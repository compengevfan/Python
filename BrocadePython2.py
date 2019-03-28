import sys
import time
import getpass
import xmltodict
import http.client as http
import pyfos.pyfos_auth as auth
import xml.etree.ElementTree as ET

SW_Username = "admin"
SW_Password = ""

#Connecting to Switch1
SW1_Session = auth.login(SW_Username, SW_Password, "10.92.238.99", "None")
#Connecting to Switch2
SW2_Session = auth.login(SW_Username, SW_Password, "10.92.238.100", "None")

#Building Switch 1 REST header
header1 = SW1_Session.get('credential')
header1.update({'Accept': 'application/yang-data+xml'})
header1.update({'Content-Type': 'application/yang-data+xml'})
ip1 = SW1_Session.get("ip_addr")

#Building Switch 2 REST header
header2 = SW1_Session.get('credential')
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
SW2_Connection = http.HTTPConnection(ip2)
method = "GET"
URI = "/rest/running/brocade-interface/fibrechannel"
Body = None
SW2_Connection.request(method, URI, Body, header2)

if SW2_Session.get('throttle_delay') > 0:
    time.sleep(SW2_Session.get('throttle_delay'))
response2 = SW2_Connection.getresponse()

DataAsXML2 = ET.fromstring((response2.read()))
DataAsXML2

#Closing session on Switch 1
auth.logout(SW1_Session)
#Closing session on Switch 2
auth.logout(SW2_Session)