import webapp2,datetime
from django.utils import simplejson
from google.appengine.ext import ndb
from google.appengine.api import users
from models.user_model import User,Fillout,QuestionRatings,fillout_key
from models.quiz_model import Quiz,Question,getQuiz
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
  
  def post(self,idStr):
    json = simplejson.loads(self.request.body)
    if "password" not in json or json["password"]!="ruilov12": return

    if "users" in json:
      for user_dict in json["users"]:
        ndb_user = User(unique_id=user_dict["unique_id"],email=user_dict["email"],name=user_dict["name"],subscribed=user_dict["subscribed"])
        if ndb_user.email=="ruilov@gmail.com":
          ndb_user.password = ndb_user.password_hash("ruilov12")
        ndb_user.put()

    if "quizzes" in json:
      for quiz_dict in json["quizzes"]:
        quiz = getQuiz(quiz_dict["id"])
        quiz.status = quiz_dict["status"]
        if "releaseDate" in quiz_dict and quiz_dict["releaseDate"]!=None:
          quiz.releaseDate = utils.date_from_str(quiz_dict["releaseDate"])
        questionArr = []
        for question_dict in quiz_dict["questions"]:
          question = Question()
          question.text = question_dict["text"]
          question.source = question_dict["source"]
          question.answer = question_dict["answer"]
          questionArr.append(question)
        quiz.questions = questionArr
        quiz.put()

    if "fillouts" in json:
      for fillout_dict in json["fillouts"]:
        fillout = Fillout(parent=fillout_key(fillout_dict["user_email"],fillout_dict["quiz_id"]),
            user_email=fillout_dict["user_email"],quiz_id=fillout_dict["quiz_id"])

        fillout.ranked = fillout_dict["ranked"]
        fillout.guesses_low = [float(x) for x in fillout_dict["guesses_low"]]
        fillout.guesses_high = [float(x) for x in fillout_dict["guesses_high"]]
        fillout.put()

    if "ratings" in json:
      for rating_dict in json["ratings"]:
        rating = QuestionRatings(user_email=rating_dict["user_email"],quiz_id=rating_dict["quiz_id"],ratings=rating_dict["ratings"])
        rating.put()

def modelList():
  modelList = [
    {"tag": "users", "model": User},
    {"tag": "quizzes", "model": Quiz},
    {"tag": "fillouts", "model": Fillout},
    {"tag": "ratings", "model": QuestionRatings}
  ]
  return modelList