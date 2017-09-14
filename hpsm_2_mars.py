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

ta = application.split(",")
tr = resource.split(",")
ts = software.split(",")
tm = machine.split(",")

count = 1
url = "http://" + ip + ":" + port + "/SM/9/rest/YarvisCMDB?Type=CI&count=1"
print(url)
r = requests.get(url, auth=(user, password))
print(r.status_code)
data = r.json()
total_count = data['@totalcount']

print('count is: ', count)
print('total is: ', total_count)

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
		print citype

		if (citype in ta):
			print "building application node"
			print citype
			print sci_data['CI']
			outputjson = "{\"ogit/Automation/marsNodeFormalRepresentation\" : \""
			outputjson += sci_data['CI']['ConfigurationItem']
			outputjson += "\", \"ogit/_owner\" : \"cmdbintegration.stage\", \"ogit/_id\": \"CMDBIntegration.stage:Production:Application:"
			outputjson += sci_data['CI']['ConfigurationItem']
			outputjson += "\", \"ogit/name\": \""
			outputjson += sci_data['CI']['ConfigurationItem']
			outputjson += "\", \"ogit/Automation/marsNode\": \"Application\", \"ogit/id\": \"\"}"
		if (citype in tr):
			pass
		if (citype in ts):
			pass
		if (citype in tm):
			subtype = sci_data['CI']['ConfigurationItemSubType']
			if (subtype not in subtypes):
				subtype = "Appliance"
			if (subtype == "Unix"):
				subtype = "UNIX"
			if (subtype == "Wireless" or subtype == "WirelessLANController"):
				subtype = "WiFi"
			pass
	else:
		continue
    count = count + results_num

