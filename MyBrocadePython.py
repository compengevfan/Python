import sys
import pyfos.pyfos_brocade_zone as zone
import pyfos.pyfos_auth as pyfos_auth
import pyfos.pyfos_util as pyfos_util
import pyfos.utils.brcd_util as brcd_util

session = pyfos_auth.login("admin", "csx5ystems!", "10.92.238.99", "None")

myzone = zone.effective_configuration.get(session)

pyfos_util.response_print(myzone.attributes_dict)

pyfos_auth.logout(session)