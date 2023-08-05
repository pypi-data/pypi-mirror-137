import requests

def veeamOneAuthToken(username, password, baseurl):
    # Get the auth token
    authUrl = f"{baseurl}/api/token"

    # If username contains '\', replace with '%5C'
    payload=f'grant_type=password&username={username}&password={password}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'Reporter_SessionId=f33050cb2f68453b89c72b14a3621025'
    }

    # Attempting authentication
    try:
        authResponse = requests.request("POST", authUrl, headers=headers, data=payload, verify=False)
    except:
        return "Could not receive Veeam One Access Token"
        exit

    # Returning authentication token
    token = authResponse.json().get('access_token')
    return token

def invokeVeeamOne(method, baseurl, endpoint, token, parameters = False):
    # Build the URL
    url = f"{baseurl}/api/v2/{endpoint}"

    # Build the headers
    payload=parameters
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer ' + token,
    'Cookie': 'Reporter_SessionId=f33050cb2f68453b89c72b14a3621025'
    }

    # Attempting request
    try:
        if parameters == False:
            response = requests.request(method, url, headers=headers, data=payload, verify=False).json()
        else:
            response = requests.request(method, url, headers=headers, data=payload, params=parameters, verify=False).json()
    except:
        return "Veeam One request failed."
        exit

    return response.get('items')

def veeamOneHyperVVMs(baseurl, token):
    # Defining endpoint
    endpoint = "hyperV/vms"

    # Attempting request
    try:
        response = invokeVeeamOne("GET", baseurl, endpoint, token)
    except:
        return "Veeam One Hyper V VMs request failed."

    # Creating dictionary array
    try:
        vms = []
        for res in response:
            dict = {
                'VMID': res.get('vmId'),
                'Name': res.get('name'),
                'OS': res.get('guestOs')
            }
            vms.append(dict)
    except:
        return "Failed to create Hyper V VM dictionary."
    return vms

def veeamOnevSphereVMs(baseurl, token):
    # Defining endpoint
    endpoint = "vSphere/vms"

    # Attempting request
    try:
        response = invokeVeeamOne("GET", baseurl, endpoint, token)
    except:
        return "Veeam One vSphere VMs request failed."
        exit

    # Creating dictionary array
    try:
        vms = []
        for res in response:
            dict = {
                'VMID': res.get('vmId'),
                'Name': res.get('name'),
                'OS': res.get('guestOs'),
                'ResourcePoolID': res.get('parentId')
            }
            vms.append(dict)
    except:
        return "Failed to create vSphere VM dictionary."
        exit
    return vms

def getPoolName(id, res):
    # Looping groups in resourcegroups
    for i in res:
        # If resource group ID matches, return resource group name
        if(i.get('ResourcePoolID') == id):
            return i.get('ResourcePoolName')

def veeamOnevSphereResourcePools(baseurl, token):
    # Defining endpoint
    endpoint = "vSphere/resourcePools"

    # Attempting request
    try:
        response = invokeVeeamOne("GET", baseurl, endpoint, token)
    except:
        return "Veeam One vSphere Resource Pools request failed."
        exit

    # Creating dictionary array
    try:
        resourcePools = []
        for res in response:
            dict = {
                'ResourcePoolID': res.get('resourcePoolId'),
                'ResourcePoolName': res.get('name') 
            }
            resourcePools.append(dict)
    except:
        return "Failed to create vSphere resource pool dictionary."
        exit

    return resourcePools

