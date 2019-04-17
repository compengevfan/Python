#Parameters: 
#   Environment
#   Username
#   Password
#   Server/Array Name
#   Port/Director Identifier.
#Looks for the server/array name in the port listing to get the WWN.
#Create the alias with appropriate name.
import time
import http.client as http
import argparse
import BrocadeFunctions as BF

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', required=True, action='store', help='PROD, DEV, DR')
    parser.add_argument('-u', required=True, action='store', help='Username')
    parser.add_argument('-p', required=True, action='store', help='Password')
    parser.add_argument('-n', required=True, action='store', help='Server or Array Name')
    parser.add_argument('-i', required=True, action='store', help='Port or Director Identifier')
    args = parser.parse_args()
    return args

def main():
    args = getargs()

    #print(args.e + '-' + args.u + '-' + args.p + '-' + args.n + '-' + args.i)

    IP1, IP2 = BF.BrocadeEnvironment(args.e)
    
    print("Connecting to switch 1...")
    Connection1, Header1 = BF.BrocadeConnect(args.u, args.p, IP1)
    print("Connecting to switch 2...")
    Connection2, Header2 = BF.BrocadeConnect(args.u, args.p, IP2)

    print("Extracting throttle delay setting for switch 1...")
    Delay1 = BF.BrocadeThrottle(Connection1)
    print("Extracting throttle delay setting for switch 2...")
    Delay2 = BF.BrocadeThrottle(Connection2)

    print("Extracting port information from switch 1...")
    PortInfo1 = BF.BrocadePortList(Header1, IP1, Delay1)
    print("Extracting port information from switch 2...")
    PortInfo2 = BF.BrocadePortList(Header2, IP2, Delay2)

    print("Locating name/port combo provided...")
    print("Obtaining WWN if name found...")
    print("And storing the switch the combo was found on...")
    print("Checking switch 1...")
    Located_SW1 = False
    for i in range(0, len(PortInfo1['Response']['fibrechannel'])):
        Name = PortInfo1['Response']['fibrechannel'][i]['user-friendly-name']
        if args.n in Name and args.i in Name:
            Located_SW1 = True
            WWN1 = PortInfo1['Response']['fibrechannel'][i]['neighbor']['wwn']

    Located_SW2 = False
    print("Checking switch 2...")
    for i in range(0, len(PortInfo2['Response']['fibrechannel'])):
        Name = PortInfo2['Response']['fibrechannel'][i]['user-friendly-name']
        if args.n in Name and args.i in Name:
            Located_SW2 = True
            WWN2 = PortInfo2['Response']['fibrechannel'][i]['neighbor']['wwn']

    if Located_SW1 == True:
        print("Name/Port Combo Found on SW1. WWN is " + WWN1)

        ResponseCode = BF.BrocadeAliasPost(Header1, IP1, Delay1, args.n, args.i, WWN1)
        if ResponseCode != 201:
            print("Alias Creation Failed!!!")

        CheckSum, CfgName = BF.BrocadeInfo(Header1, IP1, Delay1)

        ResponseCode = BF.BrocadeSave(Header1, IP1, Delay1, CheckSum)

    if Located_SW2 == True:
        print("Name/Port Combo Found on SW2. WWN is " + WWN2)

        ResponseCode = BF.BrocadeAliasPost(Header2, IP2, Delay2, args.n, args.i, WWN2)
        if ResponseCode != 201:
            print("Alias Creation Failed!!!")

        CheckSum, CfgName = BF.BrocadeInfo(Header2, IP2, Delay2)

        ResponseCode = BF.BrocadeSave(Header2, IP2, Delay2, CheckSum)

        #BF.BrocadeEnable(Header2, IP2, Delay2, CheckSum, CfgName)

    print("Terminating session on switch 1...")
    Disconnect1 = BF.BrocadeDisconnect(Connection1)
    if Disconnect1.get('http-resp-code') == 204:
        print("Switch1 session terminated.")
    print("Terminating session on switch 2...")
    Disconnect2 = BF.BrocadeDisconnect(Connection2)
    if Disconnect2.get('http-resp-code') == 204:
        print("Switch2 session terminated.")

if __name__ == "__main__":
    main()
