import requests
import json
import configparser
import urllib

config = configparser.ConfigParser()
config.read('config.ini')

ip = config['HPSM']['IP']
port = config['HPSM']['PORT']
user = config['HPSM']['USER']
password = config['HPSM']['PASSWORD']
machine = config['MARS']['MACHINE']
software = config['MARS']['SOFTWARE']
resource = config['MARS']['RESOURCE']
application = config['MARS']['APPLICATION']
subtypes = config['MARS']['SUBTYPES']
graphit = config['HIRO']['GRAPH']
cliemtkey = config['HIRO']['KEY']
clientsecret = config['HIRO']['SECRET']
wso2 = config['HIRO']['WSO2']
hirouser = config['HIRO']['HIROUSER']
hiropassword = config['HIRO']['HIROPASS']

ta = (application.encode('utf-8')).split(',')
tr = (resource.encode('utf-8')).split(",")
ts = (software.encode('utf-8')).split(",")
tm = (machine.encode('utf-8')).split(",")

application_node = '{"ogit/Automation/marsNodeFormalRepresentation" : "<DataManagement xmlns=\\"https://graphit.co/schemas/v2/MARSSchema\\" ApplicationClass=\\"Data\\" ApplicationSubClass=\\"DataManagement\\" ID=\\"CMDBIntegration:Production:Application:ApplicationDummy\\" NodeName=\\"ApplicationDummy\\" NodeType=\\"Application\\" CustomerID=\\"cmdbintegration\\" CustomerName=\\"CMDBIntegration\\"> <SourceCiId> <Content Value=\\"id1\\"/> </SourceCiId> <Dependencies> <Node ID=\\"CMDBIntegration:Production:Resource:ResourceDummy\\"/> </Dependencies> </DataManagement>",  "ogit/_owner" : "cmdb",  "ogit/_id": "CMDBIntegration:Production:Application:ApplicationDummy",  "ogit/name": "ApplicationDummy",  "ogit/Automation/marsNodeType": "Application",  "ogit/id": ""}'
resource_node = '{"ogit/Automation/marsNodeFormalRepresentation" : "<Database xmlns=\\"https://graphit.co/schemas/v2/MARSSchema\\" ResourceClass=\\"Database\\" ID=\\"CMDBIntegration:Production:Resource:ResourceDummy\\" NodeName=\\"ResourceDummy\\" NodeType=\\"Resource\\" CustomerID=\\"cmdbintegration\\" CustomerName=\\"CMDBIntegration\\"> <Dependencies> <Node ID=\\"CMDBIntegration:Production:Application:ApplicationDummy\\"/> </Dependencies></Database>",  "ogit/_owner" : "cmdbintegration",  "ogit/_id": "CMDBIntegration:Production:Resource:ResourceDummy",  "ogit/name": "ResourceDummy",  "ogit/Automation/marsNodeType": "Resource",  "ogit/id": ""}'
software_node = '{"ogit/Automation/marsNodeFormalRepresentation" : "<MySQL xmlns=\\"https://graphit.co/schemas/v2/MARSSchema\\" SoftwareClass=\\"DBMS\\" SoftwareSubClass=\\"MySQL\\" ID=\\"CMDBIntegration:Production:Software:SoftwareDummy\\" NodeName=\\"SoftwareDummy\\" NodeType=\\"Software\\" CustomerID=\\"cmdbintegration\\" CustomerName=\\"CMDBIntegration\\"><Dependencies> <Node ID=\\"CMDBIntegration:Production:Resource:ResourceDummy\\"/></Dependencies></MySQL>","ogit/_owner" : "cmdbintegration","ogit/_id": "CMDBIntegration:Production:Resource:SoftwareDummy","ogit/name": "SoftwareDummy", "ogit/Automation/marsNodeType": "Software", "ogit/id": ""}'

headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
payload = {'grant_type': 'password', 'username': hirouser, 'password': hiropassword, 'scope': 'individual,department,company', 'client_id': cliemtkey, 'client_secret': clientsecret}
access_token = requests.post(wso2, headers=headers, verify=False, data=payload)
access_data = access_token.json()
token = access_data['access_token']

token2 = json.loads(json.dumps(access_data))
strtok = token2['access_token']
app_payload = json.loads(json.dumps(application_node))
res_payload = json.loads(json.dumps(resource_node))
sof_payload = json.loads(json.dumps(software_node))
headers = {'Content-Type': 'application/json', '_TOKEN': strtok}
url = graphit + "/new/ogit%2FAutomation%2FMARSNode"
post = requests.post(url, headers=headers, data=app_payload, verify=False)
post = requests.post(url, headers=headers, data=res_payload, verify=False)
post = requests.post(url, headers=headers, data=sof_payload, verify=False)

count = 1
url = "http://" + ip + ":" + port + "/SM/9/rest/YarvisCMDB?Type=CI&count=1"
r = requests.get(url, auth=(user, password))
data = r.json()
total_count = data['@totalcount']

while count < total_count:
    curl = "http://" + ip + ":" + port + "/SM/9/rest/YarvisCMDB?Type=CI&start=" + str(count)
    ci = requests.get(curl, auth=(user, password))
    results_data = ci.json()
    results_num = results_data['@count']

    for value in results_data['content']:
	single_ci = value['CI']['ConfigurationItem']
	surl = "http://" + ip + ":" + port + "/SM/9/rest/YarvisCMDB/" + urllib.quote_plus(single_ci.encode('utf8'))
	sci_r = requests.get(surl, auth=(user, password))
	if (sci_r.status_code == 200):
		sci_data = sci_r.json()
		citype = sci_data['CI']['ConfigurationItemType']
		if (citype in ta):
			pass
		if (citype in tr):
			pass
		if (citype in ts):
			pass
		if (citype in tm):
			try:
				subtype = sci_data['CI']['ConfigurationItemSubType']
			except:
				subtype = "Appliance"
			if (subtype not in subtypes):
				subtype = "Appliance"
			if (subtype == "Unix"):
				subtype = "UNIX"
			if (subtype == "Wireless" or subtype == "WirelessLANController"):
				subtype = "WiFi"

			outputjson = "{\"ogit/Automation/marsNodeFormalRepresentation\" : \"<"
			outputjson += subtype
			outputjson += " xmlns=\\\"https://graphit.co/schemas/v2/MARSSchema\\\" ID=\\\"CMDBIntegration:Production:Machine:"
                        outputjson += sci_data['CI']['ConfigurationItem']
                        outputjson += "\\\" MachineClass=\\\""
			outputjson += subtype
			outputjson += "\\\" NodeName=\\\""
			outputjson += sci_data['CI']['ConfigurationItem']
			outputjson += "\\\" NodeType=\\\"Machine\\\" CustomerID=\\\"cmdbintegration\\\" CustomerName=\\\"CMDBIntegration\\\"><IP> <Content Value=\\\"no-ip\\\"/></IP><Dependencies> <Node ID=\\\"CMDBIntegration:Production:Software:CMDB_Integration\\\"/></Dependencies></Appliance>\", \"ogit/_owner\" : \"cmdbintegration\", \"ogit/_id\": \"CMDBIntegration:Production:Machine:"
                        outputjson += sci_data['CI']['ConfigurationItem']
                        outputjson += "\", \"ogit/name\": \""
                        outputjson += sci_data['CI']['ConfigurationItem']
                        outputjson += "\", \"ogit/Automation/marsNodeType\": \"Machine\", \"ogit/id\": \"\" }"
			url = graphit + "/new/ogit%2FAutomation%2FMARSNode"
			headers = {'Content-Type': 'application/json', '_TOKEN': strtok}
			data = json.loads(json.dumps(outputjson))
			post = requests.post(url, headers=headers, data=data, verify=False)

			if (post.status_code == 200):
				print "Sucessfully created node", sci_data['CI']['ConfigurationItem'], "of type: ", subtype
			else:
				ciname = sci_data['CI']['ConfigurationItem']
				url = graphit + "/CMDBIntegration%3AProduction%3AMachine%3A" + urllib.quote_plus(ciname.encode('utf8'))
				post = requests.post(url, headers=headers, data=data, verify=False)
				if (post.status_code == 200):
					print "Succesfully updated node", sci_data['CI']['ConfigurationItem']
	else:
		continue
    count = count + results_num
