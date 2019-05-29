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
    parser.add_argument('n', action='store', help='Server Name')
    parser.add_argument('u', action='store', help='Username')
    parser.add_argument('-p', action='store', help='Password. If running from terminal, do not use this argument. You will be prompted for your password.')
    args = parser.parse_args()
    return args

args = getargs()

if args.p == None:
    args.p = getpass.getpass(prompt="Please provide your password: ")

#ReturnCode = 0

IP1, IP2 = BF.Environment(args.e)
DF.InvokeLogging(LogFile,LogType.Info,"Connecting to switch 1...")
Connection1, Header1 = BF.Connect(args.u, args.p, IP1)
if Connection1 == 66:
    DF.InvokeLogging(LogFile,LogType.Err,"Connection to Switch 1 (A side) failed!!!")
    SW1Connection = False
    ReturnCode = 1
else:
    DF.InvokeLogging(LogFile,LogType.Succ,"Connection to switch 1 successful.")
    SW1Connection = True
    DF.InvokeLogging(LogFile,LogType.Succ,"Extracting throttle delay setting for switch 1...")
    Delay1 = BF.Throttle(Connection1)
    DF.InvokeLogging(LogFile,LogType.Succ,"Extracting port information from switch 1...")
    PortInfo1 = BF.PortList(Header1, IP1, Delay1)

DF.InvokeLogging(LogFile,LogType.Info,"Connecting to switch 2...")
Connection2, Header2 = BF.Connect(args.u, args.p, IP2)
if Connection2 == 66:
    DF.InvokeLogging(LogFile,LogType.Err,"Connection to Switch 2 (B side) failed!!!")
    SW2Connection = False
    ReturnCode = 1
else:
    DF.InvokeLogging(LogFile,LogType.Succ,"Connection to switch 2 successful.")
    SW2Connection = True
    DF.InvokeLogging(LogFile,LogType.Succ,"Extracting throttle delay setting for switch 2...")
    Delay2 = BF.Throttle(Connection2)
    DF.InvokeLogging(LogFile,LogType.Succ,"Extracting port information from switch 2...")
    PortInfo2 = BF.PortList(Header2, IP2, Delay2)

#Stuff
CheckSum1, CfgName1 = BF.Info(Header1, IP1, Delay1)

#Disconnect from Switch 1 if connected
if SW1Connection:
    DF.InvokeLogging(LogFile,LogType.Info,"Terminating session on switch 1...")
    Disconnect1 = BF.Disconnect(Connection1)
    if Disconnect1.get('http-resp-code') == 204:
        DF.InvokeLogging(LogFile,LogType.Succ,"Switch1 session terminated.")

#Disconect from Switch 2 if connected
if SW2Connection:
    DF.InvokeLogging(LogFile,LogType.Info,"Terminating session on switch 2...")
    Disconnect2 = BF.Disconnect(Connection2)
    if Disconnect2.get('http-resp-code') == 204:
        DF.InvokeLogging(LogFile,LogType.Succ,"Switch2 session terminated.")

LogFile.close()
deinit()