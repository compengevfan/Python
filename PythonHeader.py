import os
import sys
import datetime
try:
    import blah as DF
except:
    print("'DupreeFunctions' module not available!!! Please check with Dupree!!! Script exiting!!!")
    sys.exit(0)

class LogType:
    Succ = "Succ"
    Info = "Info"
    Warn = "Warn"
    Err = "Err"

if not os.path.exists("./~Logs"):
    os.mkdir("./~Logs")

ScriptName = os.path.basename(__file__)
ScriptStarted = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

FileName = "./~Logs/" + ScriptName + " " + ScriptStarted + ".log"
LogFile = open(FileName, "a")

# DF.InvokeLogging(LogFile,LogType.Info,"This is a Demo...")

LogFile.close()

