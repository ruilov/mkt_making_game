import webapp2,datetime
from django.utils import simplejson
from google.appengine.ext import ndb
from google.appengine.api import users
from server_controllers.models import User,Fillout,QuestionRatings,Quiz
from server_controllers import utils

class DatastoreOps(webapp2.RequestHandler):
  def get(self,idStr):
    if self.request.get("password") != "ruilov12": return

    modelL = modelList()
    datastore = {}
    for elem in modelL:
      datastore[elem["tag"]] = []
      query = elem["model"].query().fetch()
      for qelem in query:
        as_dict = qelem.to_dict()
        if elem["tag"]=="quizzes": as_dict["id"] = qelem.getID()
        datastore[elem["tag"]].append(as_dict)

    utils.write_back(self,datastore)

def modelList():
  modelList = [
    {"tag": "users", "model": User},
    {"tag": "quizzes", "model": Quiz},
    {"tag": "fillouts", "model": Fillout},
    {"tag": "ratings", "model": QuestionRatings}
  ]
  return modelList