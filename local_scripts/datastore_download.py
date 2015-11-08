import urllib2,json,requests

server = 'http://localhost:8080'
# server = 'http://mktmakinggame.com'

api = server + '/api/datastore_ops/'
http_headers = {'content-type': 'application/json'}

resp = requests.get(url=api,params={"password": "ruilov12"})
data = resp.json()
fp = open("backup.json","w")
json.dump(data,fp,indent=2);