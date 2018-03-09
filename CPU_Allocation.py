from pyVim.connect import SmartConnect
import pyVmomi
import ssl
import getpass

vCenter = raw_input("Please provide the vCenter name:")
username = raw_input("Please provide your username:")
password = getpass.getpass(prompt = "Please provide your password:")
s = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode = ssl.CERT_NONE
si = SmartConnect(host=vCenter, user=username, pwd=password,sslContext=s)

content = si.content

# Method that populates objects of type vimtype
def get_all_objs(content, vimtype):
        obj = {}
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
                obj.update({managed_object_ref: managed_object_ref.name})
        return obj

print "Retrieving list of Clusters..."
Clusters = get_all_objs(content, [pyVmomi.vim.ClusterComputeResource])

for cluster in Clusters:
        print (cluster.name)
