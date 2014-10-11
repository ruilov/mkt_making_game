import json
import datetime
from time import mktime

class MyEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.isoformat()
    return json.JSONEncoder.default(self, obj)

def is_admin(user):
  email = user.email()
  return email=="test2@example.com" or email=="ruilov@gmail.com" or email == "carrben12@gmail.com"