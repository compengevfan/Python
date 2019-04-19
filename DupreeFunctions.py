def InvokeLogging(LogFile,LogType,LogString):
    import datetime

    CurrentDateTime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    LogFile.write(CurrentDateTime + " " + LogString)

    print(CurrentDateTime + " " + LogType + " " + LogString)