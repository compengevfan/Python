#Parameters: 
#   Environment
#   Server
#   Username
#   Password - Optional. If not provided, you will be prompted.
#Looks for the server/array name in the port listing to get the WWN.
#Create the alias with appropriate name.
import os, sys, datetime
try:
    import DupreeFunctions as DF
except ModuleNotFoundError:
    print("'DupreeFunctions' module not available!!! Please check with Dupree!!! Script exiting!!!")
    sys.exit(0)
from colorama import init, deinit
init()

import time
import getpass
import http.client as http
import argparse
import BrocadeFunctions as BF

LogType = DF.SetupLogTypes()

if not os.path.exists("./~Logs"):
    os.mkdir("./~Logs")

DF.DeleteLogFiles()

ScriptName = os.path.basename(__file__)
ScriptStarted = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

FileName = "./~Logs/" + ScriptName + "_" + ScriptStarted + ".log"
LogFile = open(FileName, "a")

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('e', action='store', help='PROD, DEV, DR')
    parser.add_argument('n', action='store', help='Server or Array Name')
    parser.add_argument('u', action='store', help='Username')
    parser.add_argument('-p', action='store', help='Password. If running from terminal, do not use this argument. You will be prompted for your password.')
    args = parser.parse_args()
    return args

args = getargs()

if args.p == None:
    args.p = getpass.getpass(prompt="Please provide your password: ")

IP1, IP2 = BF.Environment(args.e)

DF.InvokeLogging(LogFile,LogType.Info,"Connecting to switch 1...")
Connection1, Header1 = BF.Connect(args.u, args.p, IP1)
if Connection1 == 66:
    DF.InvokeLogging(LogFile,LogType.Err,"Connection to switch 1 failed!!! Script exiting!!!")
    sys.exit(0)
DF.InvokeLogging(LogFile,LogType.Info,"Connecting to switch 2...")
Connection2, Header2 = BF.Connect(args.u, args.p, IP2)
if Connection2 == 66:
    DF.InvokeLogging(LogFile,LogType.Err,"Connection to switch 2 failed!!!")
    DF.InvokeLogging(LogFile,LogType.Info,"Disconnecting from switch 1...")
    Disconnect1 = BF.Disconnect(Connection1)
    DF.InvokeLogging(LogFile,LogType.Info,"Script exiting!!!")
    sys.exit(0)

DF.InvokeLogging(LogFile,LogType.Succ,"Extracting throttle delay setting for switch 1...")
Delay1 = BF.Throttle(Connection1)
DF.InvokeLogging(LogFile,LogType.Succ,"Extracting throttle delay setting for switch 2...")
Delay2 = BF.Throttle(Connection2)

DF.InvokeLogging(LogFile,LogType.Succ,"Extracting port information from switch 1...")
PortInfo1 = BF.PortList(Header1, IP1, Delay1)
DF.InvokeLogging(LogFile,LogType.Succ,"Extracting port information from switch 2...")
PortInfo2 = BF.PortList(Header2, IP2, Delay2)

DF.InvokeLogging(LogFile,LogType.Info,"Obtaining WWN for server on switch 1...")
WWN1 = []
for i in range(0, len(PortInfo1['Response']['fibrechannel'])):
    Name = PortInfo1['Response']['fibrechannel'][i]['user-friendly-name']
    if (args.n) in Name:
        WWN1.append(PortInfo1['Response']['fibrechannel'][i]['neighbor']['wwn'])
        SW1Alias = Name

DF.InvokeLogging(LogFile,LogType.Info,"Obtaining WWN for server on switch 2...")
WWN2 = []
for i in range(0, len(PortInfo2['Response']['fibrechannel'])):
    Name = PortInfo2['Response']['fibrechannel'][i]['user-friendly-name']
    if (args.n) in Name:
        WWN2.append(PortInfo2['Response']['fibrechannel'][i]['neighbor']['wwn'])
        SW2Alias = Name

if len(WWN1) == 1 and len(WWN2) == 1:
    #Performing Alias creation on switch 1...
    DF.InvokeLogging(LogFile,LogType.Info,"Submitting command to create alias " + SW1Alias)
    ResponseCode = BF.AliasPost(Header1, IP1, Delay1, SW1Alias, None, WWN1)
    if ResponseCode != 201:
        DF.InvokeLogging(LogFile,LogType.Err,"Alias creation failed!!! Since you made it this far without hitting any errors, this probably means the alias already exists.")
        DF.InvokeLogging(LogFile,LogType.Err,"Please check your inputs and try again.")
    else:
        DF.InvokeLogging(LogFile,LogType.Succ,"Alias created successfully.")

        DF.InvokeLogging(LogFile,LogType.Info,"Obtaining the switch config checksum...")
        CheckSum, CfgName = BF.Info(Header1, IP1, Delay1)

        DF.InvokeLogging(LogFile,LogType.Info,"Saving config...")
        ResponseCode = BF.Save(Header1, IP1, Delay1, CheckSum)

        if ResponseCode == 204:
            DF.InvokeLogging(LogFile,LogType.Succ,"Configuration save successful.")
        else:
            DF.InvokeLogging(LogFile,LogType.Err,"Configuration save failed!!!")

    #Performing Alias creation on switch 2...
    DF.InvokeLogging(LogFile,LogType.Info,"Submitting command to create alias " + SW2Alias)
    ResponseCode = BF.AliasPost(Header2, IP2, Delay2, SW2Alias, None, WWN2)
    if ResponseCode != 201:
        DF.InvokeLogging(LogFile,LogType.Err,"Alias creation failed!!! Since you made it this far without hitting any errors, this probably means the alias already exists.")
        DF.InvokeLogging(LogFile,LogType.Err,"Please check your inputs and try again.")
    else:
        DF.InvokeLogging(LogFile,LogType.Succ,"Alias created successfully.")

        DF.InvokeLogging(LogFile,LogType.Info,"Obtaining the switch config checksum...")
        CheckSum, CfgName = BF.Info(Header2, IP2, Delay2)

        DF.InvokeLogging(LogFile,LogType.Info,"Saving config...")
        ResponseCode = BF.Save(Header2, IP2, Delay2, CheckSum)

        if ResponseCode == 204:
            DF.InvokeLogging(LogFile,LogType.Succ,"Configuration save successful.")
        else:
            DF.InvokeLogging(LogFile,LogType.Err,"Configuration save failed!!!")

#figure out error codes...

DF.InvokeLogging(LogFile,LogType.Info,"Terminating session on switch 1...")
Disconnect1 = BF.Disconnect(Connection1)
if Disconnect1.get('http-resp-code') == 204:
    DF.InvokeLogging(LogFile,LogType.Succ,"Switch1 session terminated.")
DF.InvokeLogging(LogFile,LogType.Info,"Terminating session on switch 2...")
Disconnect2 = BF.Disconnect(Connection2)
if Disconnect2.get('http-resp-code') == 204:
    DF.InvokeLogging(LogFile,LogType.Succ,"Switch2 session terminated.")

LogFile.close()
deinit()