import subprocess


def getVMID():
    id = subprocess.run(['pvesh', 'get', '/cluster/nextid'], stdout = subprocess.PIPE)
    id = id.stdout.decode('utf-8').strip()
    return id

def getStorageIDsByContent(content):
    storages = subprocess.run(['pvesm', 'status', '-content' , content] ,stdout = subprocess.PIPE)
    storages = storages.stdout.decode('utf-8').strip()
    storages = storages.splitlines()
    if len(storages) == 1: 
        print('No {} Found'.format(content))
        return
    storages = storages[1:]
    storages = [result.split(" ")[0] for result in storages]
    return storages

def getTemplateName(search):
    subprocess.run(["pveam", "update"])
    templateName = subprocess.run(['pveam', 'available', '-section', 'system'], stdout = subprocess.PIPE)
    templateName = templateName.stdout.decode('utf-8').strip()
    templateName = templateName.splitlines()
    for result in templateName[1:]:
        if search in result:
            result = result.split()
            return result[1]
    print('No Template Found: {}'.format(search))

            
def getOSTemplate(search):
    storages = getStorageIDsByContent("vztmpl")
    templateName = getTemplateName(search)
    for storage in storages:
        a = subprocess.run(['pveam', 'list', storage], stdout = subprocess.PIPE)
        a = a.stdout.decode('utf-8').strip()
        if templateName in a:
            return '{}:vztmpl/{}'.format(storage,templateName)
    # download the template
    print('Downloading {}'.format(templateName))
    subprocess.run(['pveam', 'download', storages[0], templateName], stdout = subprocess.PIPE)
    return '{}:vztmpl/{}'.format(storage[0],templateName)

# def createArchLxc(configObject):
#     config = configObject.config
#     # advanced = configObject.advanced
#     # advanced_config = configObject.advanced_config
#     vmid = config["vmid"]
#     ostemplate = config["ostemplate"]
#     # cores = config["cores"]
#     # if advanced:
#     #     advanced_config = advanced_config
#     # else:
#     #     advanced_config = None
#     # if ostemplate == None:
#     #     print('No Template Found')
#     #     return
#     # ostemplate = getOSTemplate(ostemplate)
#     # if advanced_config:
#     subprocess.run(['pvesh', 'create',  vmid, ostemplate ])