#Parameters: 
#   Environment
#   Server/Array Name
#   Port/Director Identifier.
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
    parser.add_argument('i', action='store', help='Port or Director Identifier')
    parser.add_argument('u', action='store', help='Username')
    parser.add_argument('-p', action='store', help='Password. If running from terminal, do not use this argument. You will be prompted for your password.')
    args = parser.parse_args()
    return args

args = getargs()

if args.p == None:
    args.p = getpass.getpass(prompt="Please provide your password: ")

IP1, IP2 = BF.BrocadeEnvironment(args.e)

DF.InvokeLogging(LogFile,LogType.Info,"Connecting to switch 1...")
Connection1, Header1 = BF.BrocadeConnect(args.u, args.p, IP1)
if Connection1 == 66:
    DF.InvokeLogging(LogFile,LogType.Err,"Connection to switch 1 failed!!! Script exiting!!!")
    sys.exit(0)
DF.InvokeLogging(LogFile,LogType.Info,"Connecting to switch 2...")
Connection2, Header2 = BF.BrocadeConnect(args.u, args.p, IP2)
if Connection2 == 66:
    DF.InvokeLogging(LogFile,LogType.Err,"Connection to switch 2 failed!!!")
    DF.InvokeLogging(LogFile,LogType.Info,"Disconnecting from switch 1...")
    Disconnect1 = BF.BrocadeDisconnect(Connection1)
    DF.InvokeLogging(LogFile,LogType.Info,"Script exiting!!!")
    sys.exit(0)

DF.InvokeLogging(LogFile,LogType.Succ,"Extracting throttle delay setting for switch 1...")
Delay1 = BF.BrocadeThrottle(Connection1)
DF.InvokeLogging(LogFile,LogType.Succ,"Extracting throttle delay setting for switch 2...")
Delay2 = BF.BrocadeThrottle(Connection2)

DF.InvokeLogging(LogFile,LogType.Succ,"Extracting port information from switch 1...")
PortInfo1 = BF.BrocadePortList(Header1, IP1, Delay1)
DF.InvokeLogging(LogFile,LogType.Succ,"Extracting port information from switch 2...")
PortInfo2 = BF.BrocadePortList(Header2, IP2, Delay2)

DF.InvokeLogging(LogFile,LogType.Info,"Locating name/port combo provided...")
DF.InvokeLogging(LogFile,LogType.Info,"Obtaining WWN if name found...")
DF.InvokeLogging(LogFile,LogType.Info,"And storing the switch the combo was found on...")
DF.InvokeLogging(LogFile,LogType.Info,"Checking switch 1...")
Located_SW1 = False
for i in range(0, len(PortInfo1['Response']['fibrechannel'])):
    Name = PortInfo1['Response']['fibrechannel'][i]['user-friendly-name']
    if args.n in Name and args.i in Name:
        Located_SW1 = True
        WWN1 = PortInfo1['Response']['fibrechannel'][i]['neighbor']['wwn']

Located_SW2 = False
DF.InvokeLogging(LogFile,LogType.Info,"Checking switch 2...")
for i in range(0, len(PortInfo2['Response']['fibrechannel'])):
    Name = PortInfo2['Response']['fibrechannel'][i]['user-friendly-name']
    if args.n in Name and args.i in Name:
        Located_SW2 = True
        WWN2 = PortInfo2['Response']['fibrechannel'][i]['neighbor']['wwn']

if Located_SW1 == True:
    DF.InvokeLogging(LogFile,LogType.Succ,"Name/Port Combo Found on SW1. WWN is " + WWN1)

    DF.InvokeLogging(LogFile,LogType.Info,"Submitting command to create alias " + args.n + '_' + args.i)
    ResponseCode = BF.BrocadeAliasPost(Header1, IP1, Delay1, args.n, args.i, WWN1)
    if ResponseCode != 201:
        DF.InvokeLogging(LogFile,LogType.Err,"Alias creation failed!!! Since you made it this far without hitting any errors, this probably means the alias already exists.")
        DF.InvokeLogging(LogFile,LogType.Err,"Please check your inputs and try again.")
        DF.InvokeLogging(LogFile,LogType.Info,"Terminating session on switch 1...")
        Disconnect1 = BF.BrocadeDisconnect(Connection1)
        DF.InvokeLogging(LogFile,LogType.Info,"Terminating session on switch 2...")
        Disconnect2 = BF.BrocadeDisconnect(Connection2)
        DF.InvokeLogging(LogFile,LogType.Info,"Script exiting!!!")
        sys.exit(0)
    else:
        DF.InvokeLogging(LogFile,LogType.Succ,"Alias created successfully.")

    DF.InvokeLogging(LogFile,LogType.Info,"Obtaining the switch config checksum...")
    CheckSum, CfgName = BF.BrocadeInfo(Header1, IP1, Delay1)

    DF.InvokeLogging(LogFile,LogType.Info,"Saving config...")
    ResponseCode = BF.BrocadeSave(Header1, IP1, Delay1, CheckSum)

if Located_SW2 == True:
    DF.InvokeLogging(LogFile,LogType.Succ,"Name/Port Combo Found on SW2. WWN is " + WWN2)

    DF.InvokeLogging(LogFile,LogType.Info,"Submitting command to create alias " + args.n + "_" + args.i + "...")
    ResponseCode = BF.BrocadeAliasPost(Header2, IP2, Delay2, args.n, args.i, WWN2)
    if ResponseCode != 201:
        DF.InvokeLogging(LogFile,LogType.Err,"Alias creation failed!!! Since you made it this far without hitting any errors, this probably means the alias already exists.")
        DF.InvokeLogging(LogFile,LogType.Err,"Please check your inputs and try again.")
        DF.InvokeLogging(LogFile,LogType.Info,"Terminating session on switch 1...")
        Disconnect1 = BF.BrocadeDisconnect(Connection1)
        DF.InvokeLogging(LogFile,LogType.Info,"Terminating session on switch 2...")
        Disconnect2 = BF.BrocadeDisconnect(Connection2)
        DF.InvokeLogging(LogFile,LogType.Info,"Script exiting!!!")
        sys.exit(0)
    else:
        DF.InvokeLogging(LogFile,LogType.Succ,"Alias created successfully.")

    DF.InvokeLogging(LogFile,LogType.Info,"Obtaining the switch config checksum...")
    CheckSum, CfgName = BF.BrocadeInfo(Header2, IP2, Delay2)

    DF.InvokeLogging(LogFile,LogType.Info,"Saving config...")
    ResponseCode = BF.BrocadeSave(Header2, IP2, Delay2, CheckSum)

if Located_SW1 == False and Located_SW2 == False:
    DF.InvokeLogging(LogFile,LogType.Warn,"Name/Port Combo not found!!! Please check your inputs and try again!!!")

if ResponseCode == 204:
    DF.InvokeLogging(LogFile,LogType.Succ,"Configuration save successful.")
else:
    DF.InvokeLogging(LogFile,LogType.Err,"Configuration save failed!!!")

DF.InvokeLogging(LogFile,LogType.Info,"Terminating session on switch 1...")
Disconnect1 = BF.BrocadeDisconnect(Connection1)
if Disconnect1.get('http-resp-code') == 204:
    DF.InvokeLogging(LogFile,LogType.Succ,"Switch1 session terminated.")
DF.InvokeLogging(LogFile,LogType.Info,"Terminating session on switch 2...")
Disconnect2 = BF.BrocadeDisconnect(Connection2)
if Disconnect2.get('http-resp-code') == 204:
    DF.InvokeLogging(LogFile,LogType.Succ,"Switch2 session terminated.")

LogFile.close()
deinit()