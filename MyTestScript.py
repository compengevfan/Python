import getpass
import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

Username = raw_input("Gimme yo username: ")
Password = getpass.getpass(prompt='Gimme yo password:')
s=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode=ssl.CERT_NONE
si= SmartConnect(host="discography.evorigin.com", user=Username, pwd=Password,sslContext=s)

content=si.content

# Method that populates objects of type vimtype
def get_all_objs(content, vimtype):
        obj = {}
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
                obj.update({managed_object_ref: managed_object_ref.name})
        return obj
 
#Calling above method
getAllVms=get_all_objs(content, [vim.VirtualMachine])
print getAllVms
