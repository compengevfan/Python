import os
import DupreeFunctions as DF
import datetime

ScriptName = os.path.basename(__file__)
ScriptStarted = datetime.datetime.now()

DF.InvokeLogging(ScriptStarted,ScriptName,3,4)