from google.appengine.ext import ndb
from server_controllers import utils

class User(ndb.Model):
  email = ndb.TextProperty(indexed=True)
  name = ndb.TextProperty()
  subscribed = ndb.BooleanProperty()

def get_db_user(request):
  user_email = utils.get_user_email(request)
  if not user_email: raise Exception("not logged")
  query = User.query(User.email==user_email).fetch()
  if len(query)==0: raise Exception("user not found")
  return query[0]

def check_user_in_db(request):
  user_name = utils.get_user_name(request)
  user_email = utils.get_user_email(request)
  if not user_name or not user_email:
    raise Exception("creating empty user!")

  query = User.query(User.email==user_email).fetch()
  if(len(query)==0):
    ndb_user = User(email=user_email,name=user_name,subscribed=True)
    ndb_user.put()
  elif utils.get_user_provider(request)=="facebook":
    old_user = query[0]
    if old_user.name != utils.get_user_name(request):
      old_user.name = utils.get_user_name(request)
      old_user.put()

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