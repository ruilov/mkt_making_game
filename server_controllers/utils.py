import json
import datetime
from time import mktime
from google.appengine.api import users
from django.utils import simplejson

class MyEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.isoformat()
    return json.JSONEncoder.default(self, obj)

def is_admin():
    user = users.get_current_user()
    if user:
      email = user.email()
      return email=="test2@example.com" or email=="ruilov@gmail.com" or email == "carrben12@gmail.com"
    else: return False

def write_back(req,dicti):
  jsonStr = simplejson.dumps(dicti, cls = MyEncoder)
  req.response.out.write(jsonStr)