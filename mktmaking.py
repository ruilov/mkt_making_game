import webapp2
from server_controllers import main,quizzes,quiz_editor,quiz_fillout

application = webapp2.WSGIApplication([
  (r'/quizzes_api/(.*)',quizzes.Quizzes),
  (r'/quiz_fillout_api/(.*)',quiz_fillout.QuizFillout),
  (r'/quiz_editor_api/(.*)',quiz_editor.QuizEditor),
  (r'/(.*)', main.MainPage),
], debug=True)