import json, datetime, hashlib, urllib
from time import mktime
from google.appengine.api import users
from django.utils import simplejson

class MyEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.isoformat()
    return json.JSONEncoder.default(self, obj)

def admins():
  return [ "test2@example.com", "ruilov@gmail.com", "carrben12@gmail.com" ];

def is_admin(request):
  user_email = get_user_email(request)
  if user_email: return (user_email in admins())
  else: return False

def write_back(req,dicti):
  jsonStr = simplejson.dumps(dicti, cls = MyEncoder)
  req.response.out.write(jsonStr)

def unsubscribeHash(username):
  return hashlib.sha224("fsadfdsafdasd" + username).hexdigest()

def userHash(email,name):
  return hashlib.sha224(email+name+"dasdfsfa1sdfa").hexdigest()

def checkUserHash(email,name,hash):
  return hash == userHash(email,name)

def get_user_name(request):
    user = users.get_current_user()
    if user: 
      return user.nickname()  # this is for the google style login
      
    # this is for the facebook style login
    user_name = urllib.unquote(request.request.cookies.get('user_name', ''))
    user_email = urllib.unquote(request.request.cookies.get('user_email', ''))
    user_hash = urllib.unquote(request.request.cookies.get('user_hash', ''))
    if user_name and user_email and user_hash and checkUserHash(user_email,user_name,user_hash):
        return user_name

    return None

def get_user_email(request):
  user = users.get_current_user()
  if user: 
    return user.email()   # this is for the google style login
    
  # this is for the facebook style login
  user_name = urllib.unquote(request.request.cookies.get('user_name', ''))
  user_email = urllib.unquote(request.request.cookies.get('user_email', ''))
  user_hash = urllib.unquote(request.request.cookies.get('user_hash', ''))
  if user_name and user_email and user_hash and checkUserHash(user_email,user_name,user_hash):
      return user_email

  return None

def is_logged(request):
  return get_user_email(request)!=None

def get_login_url(provider):
  if provider == "gmail":
    return users.create_login_url('/login/gmail')
  if provider == "facebook":
    return "/login/fb"

def get_logout_url():
  user = users.get_current_user()
  if user: 
    return users.create_logout_url('/')

  return "/logout/"

def get_user_provider(request):
  user = users.get_current_user();
  if user: return "gmail"

  user_email = get_user_email(request)
  if user_email: return "facebook"

  return None