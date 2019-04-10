import os
os.chdir("C:/Users/y7537/Documents/GitHub/Python/Brocade")

import BrocadeFunctions as BF

IP1, IP2 = BF.BrocadeEnvironment("Dev")

Connection, Header = BF.BrocadeConnect("admin", "csx5ystems!", "10.92.238.99")
BF.BrocadeDisconnect(Arg1)