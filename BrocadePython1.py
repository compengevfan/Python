import sys
import json
import pyfos.pyfos_auth as pyfos_auth
import pyfos.pyfos_brocade_interface as ports
import pyfos.pyfos_util as pyfos_util

SW1_Session = pyfos_auth.login("admin", "csx5ystems!", "10.92.238.99", "None")
SW2_Session = pyfos_auth.login("admin", "csx5ystems!", "10.92.238.100", "None")

SW1_Ports = ports.fibrechannel.get(SW1_Session)
SW1_Ports_JSON = json.loads(pyfos_util.strjson(SW1_Ports))
SW2_Ports = ports.fibrechannel.get(SW2_Session)
SW2_Ports_JSON = json.loads(pyfos_util.strjson(SW2_Ports))

SW1_Ports_JSON[0]

# with open("Ports1.json", "w") as Ports1_File:
#     json.dump(SW1_Ports_JSON, Ports1_File)
# with open("Ports2.json", "w") as Ports2_File:
#     json.dump(SW2_Ports_JSON, Ports2_File)

for Port in SW1_Ports_JSON:
    print(Port['fibrechannel']['name'])

# SW1_Zone = zone.effective_configuration.get(SW1_Session)
# SW2_Zone = zone.effective_configuration.get(SW2_Session)

# SW1_Zone_JSON = json.loads(pyfos_util.strjson(SW1_Zone))
# SW2_Zone_JSON = json.loads(pyfos_util.strjson(SW2_Zone))

pyfos_auth.logout(SW1_Session)
pyfos_auth.logout(SW2_Session)