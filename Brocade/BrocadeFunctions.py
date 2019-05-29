def Environment(Environment):
    #Accepts an environment (or obtains it if not an argument)
    #Returns the appropriate IP addresses of the Brocade switches for that environment
    import sys

    Environments = ['PROD', 'DR', 'DEV']
    Environment = Environment.upper()

    while Environment not in Environments:
        Environment = input("Please provide the environment (PROD, DR, DEV): ").upper()

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

def Connect(Username, Password, IP):
    #Accepts Brocade IP, Username and Password.
    #Creates a connection to a switch.
    #Returns the header for that switch and the session created.
    import pyfos.pyfos_auth as auth

    Connection = auth.login(Username, Password, IP, "None")

    if auth.is_failed_login(Connection):
        return 66, None
    else:
        Header = Connection.get('credential')
        Header.update({'Accept': 'application/yang-data+xml'})
        Header.update({'Content-Type': 'application/yang-data+xml'})

        return Connection, Header

def SessionCheck(Session):
    #Accepts Brocade session and checks to see if it's still valid
    print("Place holder")

def Throttle(Connection):
    #Accepts a Brocade session and extracts the throttle delay
    #Returns the value
    Delay = Connection.get('throttle_delay')

    return Delay

def AliasPost(Header, IP, Delay, Name, Port, WWN):
    #Accepts header, switch IP, delay time, alias name, port ID, and WWN 
    #Returns response code from the HTTP request
    import time
    import http.client as http

    HTTP_Connection = http.HTTPConnection(IP)
    method = "POST"
    URI = "/rest/running/zoning/defined-configuration/alias"
    if Port == None:
        Body = '<alias><alias-name>' + Name + '</alias-name><member-entry><alias-entry-name>' + WWN + '</alias-entry-name></member-entry></alias>'
    else:
        Body = '<alias><alias-name>' + Name + '_' + Port + '</alias-name><member-entry><alias-entry-name>' + WWN + '</alias-entry-name></member-entry></alias>'
    HTTP_Connection.request(method, URI, Body, Header)

    if Delay > 0:
        time.sleep(Delay)
    response = HTTP_Connection.getresponse()
    ResponseCode = response.code

    return ResponseCode

def ZonePatch(Header, IP, Delay):
    import time
    import http.client as http

    HTTP_Connection = http.HTTPConnection(IP)
    method = "PATCH"
    URI = "/rest/running/zoning/defined-configuration/zone"

def Enable(Header, IP, Delay, CheckSum, CfgName):
    import time
    import http.client as http

    HTTP_Connection = http.HTTPConnection(IP)
    method = "PATCH"
    URI = "/rest/running/zoning/effective-configuration/cfg-name/" + CfgName
    Body = '<checksum>' + CheckSum + '</checksum>'
    HTTP_Connection.request(method, URI, Body, Header)

    if Delay > 0:
        time.sleep(Delay)
    response = HTTP_Connection.getresponse()

    return response

def Save(Header, IP, Delay, CheckSum):
    import time
    import xmltodict
    import http.client as http

    HTTP_Connection = http.HTTPConnection(IP)
    method = "PATCH"
    URI = "/rest/running/zoning/effective-configuration/cfg-action/1"
    Body = '<checksum>' + CheckSum + '</checksum>'
    HTTP_Connection.request(method, URI, Body, Header)

    if Delay > 0:
        time.sleep(Delay)
    response = HTTP_Connection.getresponse()
    ResponseCode = response.code

    return ResponseCode

def Info(Header, IP, Delay):
    #Accepts header, switch IP and delay to obtain the checksum of the switch's effective config
    #Returns the checksum
    import time
    import xmltodict
    import http.client as http

    HTTP_Connection = http.HTTPConnection(IP)
    method = "GET"
    URI = "/rest/running/zoning/effective-configuration"
    Body = None
    HTTP_Connection.request(method, URI, Body, Header)

    if Delay > 0:
        time.sleep(Delay)
    response = HTTP_Connection.getresponse()

    RespBody = xmltodict.parse(response.read())

    CheckSum = RespBody['Response']['effective-configuration']['checksum']
    CfgName = RespBody['Response']['effective-configuration']['cfg-name']

    return CheckSum, CfgName

def Probe(Header, IP, Delay):
    import time
    import xmltodict
    import http.client as http

    HTTP_Connection = http.HTTPConnection(IP)
    method = "GET"
    URI = "/running/zoning/defined-configuration/cfg/cfg-name/zs_CSXT_TEST_G630A/member-zone"
    Body = None
    HTTP_Connection.request(method, URI, Body, Header)

    if Delay > 0:
        time.sleep(Delay)
    response = HTTP_Connection.getresponse()

    RespBody = xmltodict.parse(response.read())

    print("Place holder")

def PortList(Header, IP, Delay):
    #Accepts header, switch IP and delay time to perform REST call
    #Performs REST call and obtains all the switch port information.
    #Extracts needed info and returns that info as a list/dict
    import time
    import xmltodict
    import http.client as http

    HTTP_Connection = http.HTTPConnection(IP)
    method = "GET"
    URI = "/rest/running/brocade-interface/fibrechannel"
    Body = None
    HTTP_Connection.request(method, URI, Body, Header)

    if Delay > 0:
        time.sleep(Delay)
    response = HTTP_Connection.getresponse()

    RespBody = xmltodict.parse(response.read())

    # ReturnList = []
    # for i in range(0, len(DataAsXML['Response']['fibrechannel'])):
    #     ReturnList.append(DataAsXML['Response']['fibrechannel'][i]['user-friendly-name'])

    # return ReturnList
    return RespBody

def Disconnect(Session):
    #Accepts session to terminate.
    import pyfos.pyfos_auth as auth

    Output = auth.logout(Session)
    return Output