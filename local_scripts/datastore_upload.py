import urllib2,json,requests,datetime

# server = 'http://localhost:8080'
server = 'http://mktmakinggame.com'

api = server + '/api/datastore_ops/'
http_headers = {'content-type': 'application/json'}

data = json.load(open('backup.json'))
data["password"] = "ruilov12"

resp = requests.post(url=api,headers=http_headers,data=json.dumps(data))
print resp