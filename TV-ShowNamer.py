import os, sys, datetime, argparse
try:
    import DupreeFunctions as DF
except ModuleNotFoundError:
    print("'DupreeFunctions' module not available!!! Please check with Dupree!!! Script exiting!!!")
    sys.exit(0)
from colorama import init, deinit
from pathlib import Path

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('ShowType', action='store', help='TV1,TV2,Cartoon')
    parser.add_argument('ShowName', action='store')
    parser.add_argument('Season', action='store')
    args = parser.parse_args()
    return args

def main():
    init()

    LogType = DF.SetupLogTypes()

    if not os.path.exists("./~Logs"):
        os.mkdir("./~Logs")

    DF.DeleteLogFiles()

    ScriptName = os.path.basename(__file__)
    ScriptStarted = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

    FileName = "./~Logs/" + ScriptName + "_" + ScriptStarted + ".log"
    LogFile = open(FileName, "a")

    args = getargs()

    # DF.InvokeLogging(LogFile,LogType.Succ,"This is a Demo...")

    LogFile.close()
    deinit()

if __name__ == "__main__":
        main()
