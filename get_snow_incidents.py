import requests
import json

# Set the request parameters
url = 'https://url.service-now.com/api/now/table/incident'

# Eg. User name="admin", Password="admin" for this code sample.
user = 'admin'
pwd = 'pass'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
response = requests.get(url, auth=(user, pwd), headers=headers  )

# Check for HTTP codes other than 200
if response.status_code != 200:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()

# Decode the JSON response into a dictionary and use the data
data = response.json()
txt_data = json.dumps(data)
print(txt_data.encode('utf-8'))
