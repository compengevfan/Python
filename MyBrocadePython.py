import sys
import json
import pyfos.pyfos_brocade_zone as zone
import pyfos.pyfos_auth as pyfos_auth
import pyfos.pyfos_util as pyfos_util
import pyfos.utils.brcd_util as brcd_util
import pyfos.pyfos_brocade_fibrechannel_logical_switch as switch

SW1_Session = pyfos_auth.login("admin", "csx5ystems!", "10.92.238.99", "None")
SW2_Session = pyfos_auth.login("admin", "csx5ystems!", "10.92.238.100", "None")

SW1_Zone = zone.effective_configuration.get(SW1_Session)
SW2_Zone = zone.effective_configuration.get(SW2_Session)

SW1_Zone_JSON = json.loads(pyfos_util.strjson(SW1_Zone))
SW2_Zone_JSON = json.loads(pyfos_util.strjson(SW2_Zone))

SW1 = switch.fibrechannel_logical_switch.get(SW1_Session)

pyfos_auth.logout(SW1_Session)
pyfos_auth.logout(SW2_Session)