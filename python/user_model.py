import hashlib,urllib,utils
from google.appengine.ext import ndb

class User(ndb.Model):
  name = ndb.TextProperty(indexed=True)
  email = ndb.TextProperty()
  password = ndb.TextProperty()
  subscribed = ndb.BooleanProperty()

  def password_hash(self,plainPassword):
    return hashlib.sha224(self.email+self.name+plainPassword+"asdf!!@!asf12").hexdigest()

  def checkPassword(self,plainPassword):
    return self.password == self.password_hash(plainPassword)

  def is_admin(self):
    return self.email in admins()

def cookieHash(username):
  return hashlib.sha224(username+"12312!@#asf").hexdigest()

def checkCookieHash(username,theHash):
  return cookieHash(username) == theHash

def user_name(request):
  name = urllib.unquote(request.request.cookies.get('username', ''))
  if name == '': return None
  user_hash = urllib.unquote(request.request.cookies.get('hash', ''))
  if not checkCookieHash(name,user_hash): return None
  return name

def getUser(request):
  name = user_name(request)
  if not name: return None
  users = User.query(User.name==name).fetch()
  if len(users)==0: return None
  return users[0]
    
def admins():
  return [ "mktmakinggame@gmail.com", "ruilov@gmail.com", "carrben12@gmail.com" ];

def fillout_key(user_name,quiz_id):
  return ndb.Key("fillout_key",user_name+quiz_id)

class Fillout(ndb.Model):
  quiz_id = ndb.TextProperty(indexed=True)
  username = ndb.TextProperty(indexed=True)
  guesses_low = ndb.FloatProperty(repeated=True)
  guesses_high = ndb.FloatProperty(repeated=True)
  ranked = ndb.BooleanProperty()

class QuestionRatings(ndb.Model):
  quiz_id = ndb.TextProperty(indexed=True)
  username = ndb.TextProperty(indexed=True)
  ratings = ndb.IntegerProperty(repeated=True)

class UserSuggestion(ndb.Model):
  username = ndb.TextProperty(indexed=True)
  text = ndb.TextProperty()
  time = ndb.DateTimeProperty()