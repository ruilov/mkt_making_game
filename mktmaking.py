import webapp2
from server_controllers import *
from server_apis import *

application = webapp2.WSGIApplication([
  ('/api/datastore/',datastore.Datastore),
  ('/api/send_mail/',sendmail.SendMail),
  ('/api/is_logged/',is_logged.IsLogged),
  (r'/api/datastore_ops/(.*)',datastore_ops.DatastoreOps),
  (r'/api/rate_question/(.*)',question_rating.QuestionRating),
  (r'/api/rankings/(.*)',rankings.Rankings),
  (r'/api/scores/(.*)',scores.Scores),
  (r'/api/quizzes/(.*)',quizzes.Quizzes),
  (r'/api/quiz/(.*)',quiz.Quiz),
  (r'/api/quiz_editor/(.*)',quiz_editor.QuizEditor),
  ('/api/suggestion/',suggestion.Suggestion),
  webapp2.Route(r'/login/<:.*>', login.Login, handler_method='any'),
  ('/logout/',logout.Logout),
  (r'/unsubscribe/(.*)',unsubscribe.Unsubscribe),
  (r'/(.*)', template.TemplatePage),
], debug=True)