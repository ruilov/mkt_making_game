import hashlib,urllib,utils
from google.appengine.ext import ndb

class User(ndb.Model):
  unique_id = ndb.IntegerProperty(indexed=True)
  email = ndb.TextProperty()
  name = ndb.TextProperty()
  password = ndb.TextProperty()
  subscribed = ndb.BooleanProperty()

  def password_hash(self,plainPassword):
    return hashlib.sha224(self.email+self.name+plainPassword+"asdf!!@!asf12").hexdigest()

  def checkPassword(self,plainPassword):
    return self.password == self.password_hash(plainPassword)

  def is_admin(self):
    return self.email in admins()

def cookieHash(unique_id):
  return hashlib.sha224(str(unique_id)+"12312!@#asf").hexdigest()

def checkCookieHash(unique_id,theHash):
  return cookieHash(unique_id) == theHash

def user_id(request):
  user_id = urllib.unquote(request.request.cookies.get('id', ''))
  if user_id == '': return None
  user_id = int(user_id)
  user_hash = urllib.unquote(request.request.cookies.get('hash', ''))
  if not checkCookieHash(user_id,user_hash): return None
  return user_id

def getUser(request):
  uid = user_id(request)
  if not uid: return None
  users = User.query(User.unique_id==uid).fetch()
  if len(users)==0: return None
  return users[0]
    
def admins():
  return [ "mktmakinggame@gmail.com", "ruilov@gmail.com", "carrben12@gmail.com" ];

def fillout_key(user_email,quiz_id):
  return ndb.Key("fillout_key",user_email+quiz_id)

class Fillout(ndb.Model):
  quiz_id = ndb.TextProperty(indexed=True)
  user_email = ndb.TextProperty(indexed=True)
  guesses_low = ndb.FloatProperty(repeated=True)
  guesses_high = ndb.FloatProperty(repeated=True)
  ranked = ndb.BooleanProperty()

class QuestionRatings(ndb.Model):
  quiz_id = ndb.TextProperty(indexed=True)
  user_email = ndb.TextProperty(indexed=True)
  ratings = ndb.IntegerProperty(repeated=True)

class UserSuggestion(ndb.Model):
  user_email = ndb.TextProperty(indexed=True)
  text = ndb.TextProperty()
  time = ndb.DateTimeProperty()