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
    return args

args = getargs()

# DF.InvokeLogging(LogFile,LogType.Succ,"This is a Demo...")

LogFile.close()
deinit()