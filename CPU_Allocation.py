from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl
import getpass

#vCenter = raw_input("Please provide the vCenter name:")
#username = raw_input("Please provide your username:")
password = getpass.getpass(prompt = "Please provide your password:")
s = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode = ssl.CERT_NONE
si = SmartConnect(host="discography.evorigin.com", user="evorigin\cdupree", pwd=password,sslContext=s)

#class ClusterTracker(object):
        

vCenterContent = si.RetrieveContent()
DataCenters = vCenterContent.rootFolder.childEntity
items = DataCenters[0].vmFolder.childEntity
print items[2].summary.config.numCpu

#for DataCenter in DataCenters:

for item in items:
    if isinstance(item, vim.VirtualMachine):
        print item.name
