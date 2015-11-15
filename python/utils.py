import json, datetime, hashlib, urllib
from time import mktime
from google.appengine.api import users
from django.utils import simplejson

class MyEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.isoformat()
    return json.JSONEncoder.default(self, obj)

# this needs to match the encoder above. That format string corresponds to the isoformat
def date_from_str(dstr):
  return datetime.datetime.strptime(dstr,"%Y-%m-%dT%H:%M:%S.%f")

def write_back(req,dicti):
  jsonStr = simplejson.dumps(dicti, cls = MyEncoder)
  req.response.out.write(jsonStr)

def unsubscribeHash(useremail):
  return hashlib.sha224("@!wr!@#1fsadfdsafdasd" + useremail).hexdigest()

def resetHash(useremail,yesterday=False):
  date = datetime.date.today()
  if yesterday: date = datetime.date.fromordinal(date.toordinal()-1)
  return hashlib.sha224(str(date)+"#@$wfdsa24wr34" + useremail).hexdigest()

def checkResetHash(useremail,hashs):
  hash1 = resetHash(useremail)
  hash2 = resetHash(useremail,True)
  return hashs == hash1 or hashs == hash2

def resetLink(useremail,username):
  return "https://mktmakinggame.com/#/reset/?email="+urllib.quote(useremail)+"&username="+urllib.quote(username)+"&hash="+resetHash(useremail)

