import sys
import pyfos.pyfos_auth as pyfos_auth
import pyfos.pyfos_util as pyfos_util
import pyfos.utils.brcd_util as brcd_util

session = pyfos_auth.login("admin", "csx5ystems!", "10.92.238.99", "None")

pyfos_auth.logout(session)