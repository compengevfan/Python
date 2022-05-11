import os, sys, datetime, argparse
import pathlib
try:
    import DupreeFunctions as DF
except ModuleNotFoundError:
    print("'DupreeFunctions' module not available!!! Please check with Dupree!!! Script exiting!!!")
    sys.exit(0)
from colorama import init, deinit

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

    if not pathlib.Path.exists("./~Logs"):
        pathlib.Path.mkdir("./~Logs")

    DF.DeleteLogFiles()

    ScriptName = pathlib.PurePath.name(__file__)
    ScriptStarted = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

    FileName = "./~Logs/" + ScriptName + "_" + ScriptStarted + ".log"
    LogFile = open(FileName, "a")

    args = getargs()

    # DF.InvokeLogging(LogFile,LogType.Succ,"This is a Demo...")
    if args.ShowType == 'TV1':
        FolderPath = '//storage1/Media/TV Shows/' + args.ShowName + '/Season ' + args.Season
    if args.ShowType == 'TV2':
        FolderPath = '//storage2/Media/TV Shows/' + args.ShowName + '/Season ' + args.Season
    if args.ShowType == 'Cartoon':
        FolderPath = '//storage1/Cartoons/TV Shows/' + args.ShowName + '/Season ' + args.Season
    # string = '//storage1/Media/TV Shows/Agents of S.H.I.E.L.D/Season 1'
    # p = pathlib.PureWindowsPath(string)
    # dir = pathlib.Path(p)
    # for child in dir.iterdir(): child
    i = 1
    files = pathlib.Path(FolderPath)

    LogFile.close()
    deinit()

if __name__ == "__main__":
        main()
