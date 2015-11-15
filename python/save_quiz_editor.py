import webapp2,utils
from django.utils import simplejson
from quiz_model import getQuiz,Question
from user_model import getUser

class SaveQuizEditor(webapp2.RequestHandler):
  def post(self):
    user = getUser(self)
    if not user or not user.is_admin():
      utils.write_back(self,{"not_allowed": 1})
      return

    json = simplejson.loads(self.request.body)
    quiz_id = json["id"]
    quiz = getQuiz(quiz_id)

    # parse the json into a model quiz. There's probably an easier way to do this
    questionArr = []
    for questionJSON in json["questions"]:
      question = Question()
      question.text = questionJSON["text"]
      question.source = questionJSON["source"]
      question.answer = questionJSON["answer"]
      questionArr.append(question)

    quiz.questions = questionArr
    quiz.put()