import webapp2
from django.utils import simplejson
from server_controllers import models,utils

# this API is for admins of the site to create quizzes

class QuizEditor(webapp2.RequestHandler):
  def get(self,idStr):
    quiz_id = self.request.get("id")
    if len(quiz_id)==0:
      utils.write_back(self,{"no_quiz_id": 1})
      return

    if not utils.is_admin(self):
      utils.write_back(self,{"not_allowed": 1})
      return

    quiz = models.getQuiz(quiz_id)
    utils.write_back(self,quiz.to_dict())

  def post(self,idStr):
    quiz_id = self.request.get("id")
    if len(quiz_id)==0:
      utils.write_back(self,{"no_quiz_id": 1})
      return

    if not utils.is_admin(self):
      utils.write_back(self,{"not_allowed": 1})
      return

    quiz = models.getQuiz(quiz_id)

    # parse the json into a model quiz. There's probably an easier way to do this
    json = simplejson.loads(self.request.body)
    questionArr = []
    for questionJSON in json["questions"]:
      question = models.Question()
      question.text = questionJSON["text"]
      question.source = questionJSON["source"]
      question.answer = questionJSON["answer"]
      questionArr.append(question)
    quiz.questions = questionArr
    quiz.put()



    