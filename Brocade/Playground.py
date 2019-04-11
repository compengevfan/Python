import os
os.chdir("C:/Users/y7537/Documents/GitHub/Python/Brocade")

import BrocadeFunctions as BF

IP1, IP2 = BF.BrocadeEnvironment("Dev")

Connection1, Header1 = BF.BrocadeConnect("admin", "", IP1)
Connection2, Header2 = BF.BrocadeConnect("admin", "", IP2)

Delay1 = BF.BrocadeThrottle(Connection1)
Delay2 = BF.BrocadeThrottle(Connection2)

Disconnect1 = BF.BrocadeDisconnect(Connection1)
if Disconnect1.get('http-resp-code') == 204:
    print("Switch1 session terminated.")
Disconnect2 = BF.BrocadeDisconnect(Connection2)
if Disconnect2.get('http-resp-code') == 204:
    print("Switch2 session terminated.")

