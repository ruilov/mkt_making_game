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

def unsubscribeHash(username):
  return hashlib.sha224("fsadfdsafdasd" + username).hexdigest()