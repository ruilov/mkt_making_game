import webapp2
from server_controllers import *

application = webapp2.WSGIApplication([
  ('/datastore_api/',api_datastore.Datastore),
  ('/send_mail_api/',api_sendmail.SendMail),
  ('/is_logged_api',api_is_logged.IsLogged),
  (r'/rate_question_api/(.*)',api_question_rating.QuestionRating),
  (r'/unsubscribe/(.*)',api_unsubscribe.Unsubscribe),
  (r'/rankings_api/(.*)',api_rankings.Rankings),
  (r'/scores_api/(.*)',api_scores.Scores),
  (r'/quizzes_api/(.*)',api_quizzes.Quizzes),
  (r'/quiz_api/(.*)',api_quiz.Quiz),
  (r'/quiz_editor_api/(.*)',api_quiz_editor.QuizEditor),
  webapp2.Route(r'/login/<:.*>', login.Login, handler_method='any'),
  ('/logout/',logout.Logout),
  (r'/(.*)', template.TemplatePage),
], debug=True)