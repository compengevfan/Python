def BrocadeEnvironment(Environment):
    #Accepts an environment (or obtains it if not an argument)
    #Returns the appropriate IP addresses of the Brocade switches for that environment
    import sys

    Environments = ['PROD', 'DR', 'DEV']
    Environment = Environment.upper()

    while Environment not in Environments:
        Environment = input("Please provide the environment (PROD, DR, DEV): ")

    if Environment == "PROD":
        SW1_IP = "IP"
        SW2_IP = "IP"
    if Environment == "DR":
        SW1_IP = "IP"
        SW2_IP = "IP"
    if Environment == "DEV":
        SW1_IP = "10.92.238.99"
        SW2_IP = "10.92.238.100"

    return SW1_IP, SW2_IP

def BrocadeConnect(Username, Password, IP):
    #Accepts Brocade IP, Username and Password.
    #Creates a connection to a switch.
    #Returns the header for that switch and the session created.
    import pyfos.pyfos_auth as auth

    Connection = auth.login(Username, Password, IP, "None")

    Header = Connection.get('credential')
    Header.update({'Accept': 'application/yang-data+xml'})
    Header.update({'Content-Type': 'application/yang-data+xml'})

    return Connection, Header

def BrocadeSessionCheck(Session):
    #Accepts Brocade session and checks to see if it's still valid
    print("Place holder")

def BrocadeThrottle(Connection):
    #Accepts a Brocade session and extracts the throttle delay
    #Returns the value
    Delay = Connection.get('throttle_delay')

    return Delay

def BrocadePortList(Header, IP, Delay):
    #Accepts header and switch IP to perform REST call
    #Performs REST call and obtains all the switch port information.
    #Extracts needed info and returns that info as a list/dict
    import time
    import xmltodict
    import http.client as http

    SW1_Connection = http.HTTPConnection(IP)
    method = "GET"
    URI = "/rest/running/brocade-interface/fibrechannel"
    Body = None
    SW1_Connection.request(method, URI, Body, Header)

    if Delay > 0:
        time.sleep(Delay)
    response = SW1_Connection.getresponse()

    DataAsXML = xmltodict.parse(response.read())

    for i in range(0, len(DataAsXML['Response']['fibrechannel'])):
        DataAsXML['Response']['fibrechannel'][i]['user-friendly-name']

def BrocadeDisconnect(Session):
    #Accepts session to terminate.
    import pyfos.pyfos_auth as auth

    auth.logout(Session)