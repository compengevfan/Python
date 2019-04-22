def DeleteLogFiles():
    import os, sys, time

    AgeToDelete = 30

    now = time.time()
    cutoff = now - (AgeToDelete * 86400)

    files = os.listdir("./~Logs/")
    for filename in files:
        if os.path.isfile("./~Logs/" + filename):
            t = os.stat("./~Logs/" + filename)
            c = t.st_ctime
            if c < cutoff:
                os.remove("./~Logs/" + filename)

def SetupLogTypes():
    class LogType:
        Succ = "Succ"
        Info = "Info"
        Warn = "Warn"
        Err = "Err"

    return LogType

def InvokeLogging(LogFile,LogType,LogString):
    import datetime

    CurrentDateTime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    LogFile.write(CurrentDateTime + " " + LogString)

    print(CurrentDateTime + " " + LogType + " " + LogString)