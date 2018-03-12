from pyVim.connect import SmartConnect
from import pyVmomi import vim
import ssl
import getpass

#vCenter = raw_input("Please provide the vCenter name:")
#username = raw_input("Please provide your username:")
password = getpass.getpass(prompt = "Please provide your password:")
s = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode = ssl.CERT_NONE
si = SmartConnect(host="iad-vc001.fanatics.corp", user="footballfanatic\cdupree", pwd=password,sslContext=s)

class ClusterTracker(object):
        

vCenterContent = si.RetrieveContent()
