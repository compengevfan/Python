from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl
import getpass

#def AddToList(vm, f_vmList):
#    f_vmList.append(vm)
#    return f_vmList

def FindVMs(f_item):
    if hasattr(f_item, 'childEntity'):
        Inside_items = f_item.childEntity
        for item in Inside_items:
            FindVMs(item)

    if isinstance(f_item, vim.VirtualApp):
        Inside_items = f_item.vm
        for item in Inside_items:
            FindVMs(item)

    if isinstance(f_item, vim.VirtualMachine):
        vmList.append(f_item)

    return

#initialize list
vmList = []

#Connect to vCenter
#vCenter = raw_input("Please provide the vCenter name:")
#username = raw_input("Please provide your username:")
password = getpass.getpass(prompt = "Please provide your password:")
s = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode = ssl.CERT_NONE
si = SmartConnect(host="discography.evorigin.com", user="evorigin\cdupree", pwd=password,sslContext=s)

#Get vCenter Content
vCenterContent = si.RetrieveContent()
#Obtain Datacenters
DataCenters = vCenterContent.rootFolder.childEntity
for DataCenter in DataCenters:
    #Get the VMs, Folders and vAPPs in the datacenter
    items = DataCenter.vmFolder.childEntity
    for item in items:
        FindVMs(item)
