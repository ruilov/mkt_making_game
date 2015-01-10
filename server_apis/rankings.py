import webapp2,datetime,math
from django.utils import simplejson
from google.appengine.ext import ndb
from server_controllers import models,utils

class Rankings(webapp2.RequestHandler):
  def get(self,qs):
    if not utils.is_logged(self):
      utils.write_back(self,{"not_allowed": 1})
      return
      
    quiz_id = self.request.get("id")
    current_user_email = utils.get_user_email(self)

    if len(quiz_id)==0:
      # this is used for the main ranking page where all the quizzes are retrieved
      user_email_map = {}
      rank_by_user = {}
      users_query = models.User.query().fetch()
      for user in users_query:
        user_email_map[user.email] = user.name
        rank_by_user[user.name] = {}

      quiz_dates = []
      quizzes_query = models.Quiz.query().fetch()
      for quiz in quizzes_query:
        if not( quiz.status == "old" or (quiz.status == "active" and quiz.hasFilled(self))):
          continue

        quiz_id = quiz.getID()
        quiz_dates.append({"quiz_id": quiz_id, "releaseDate": quiz.releaseDate})
        points_by_ue = score_quiz(quiz,quiz_id)
        for ue,score in points_by_ue.items():
          rank_by_user[user_email_map[ue]][quiz_id] = score

      for user in users_query:
        if len(rank_by_user[user.name])==0: del rank_by_user[user.name]
        else: rank_by_user[user.name]["current"] = user.email == current_user_email

      # sort the quizzes by date
      quiz_dates.sort(key=lambda elem: elem["releaseDate"])
      utils.write_back(self,{"rank_by_user": rank_by_user, "quiz_dates": quiz_dates})
    else:
      # this is for when the user wants to know about a particular quiz id
      quiz = models.getQuiz(quiz_id)
      if not( quiz.status == "old" or (quiz.status == "active" and quiz.hasFilled(self))):
        utils.write_back(self,{"quiz_not_old": 1})
        return

      user_email_map = {}
      users_query = models.User.query().fetch()
      for user in users_query:
        user_email_map[user.email] = user.name

      points_by_ue = score_quiz(quiz,quiz_id,detailed=True)
      data_by_user = {}
      for ue,score in points_by_ue.items():
        for elem in score: 
          elem["current"] = ue == current_user_email;
        data_by_user[user_email_map[ue]] = score

      # sort the quizzes by date
      utils.write_back(self,data_by_user)

def score_quiz(quiz,quiz_id,detailed=False):
  '''if detailed is true, get the scores per question'''

  fillout_query = models.Fillout.query(models.Fillout.quiz_id == quiz_id).fetch()
  points_by_ue = {}

  # collect all answers for each question in one place
  guesses_by_q = []
  for i in range(0,len(quiz.questions)): guesses_by_q.append([])
  
  for fillout in fillout_query:
    if fillout.ranked != None and not fillout.ranked: continue
    if fillout.user_email in points_by_ue: continue
    
    if detailed: points_by_ue[fillout.user_email] = []
    else: points_by_ue[fillout.user_email] = 0

    for i in range(0,len(quiz.questions)):
      try:
        low = float(fillout.guesses_low[i])
        high = float(fillout.guesses_high[i])
      except ValueError:
        low = None
        high = None
      guesses_by_q[i].append({'user_email': fillout.user_email, 'low': low, 'high': high})

  # score each question
  for i in range(0,len(quiz.questions)):
    answer = float(quiz.questions[i].answer)
    guesses_correct = []
    guesses_incorrect = []
    guesses_problem = []
    for guess in guesses_by_q[i]:
      guess['answer'] = answer
      guess['score'] = 0
      if guess['low']==None or guess['low']>guess['high']: guesses_problem.append(guess)
      elif guess['low']<=answer and answer<=guess['high']: guesses_correct.append(guess)
      else: guesses_incorrect.append(guess)

    assign_points(guesses_correct,correct_sorter,max_points=10)
    for guess in guesses_correct: guess['score'] += 10
    max_losers = 9 + max(11-len(guesses_correct),0)
    assign_points(guesses_incorrect,incorrect_sorter,max_points=max_losers)

    all_guesses = [guesses_correct,guesses_incorrect,guesses_problem]
    for guesses_array in all_guesses:
      for guess in guesses_array:
        ue = guess['user_email']
        if detailed:
          del guess['user_email']
          del guess['answer']
          points_by_ue[ue].append(guess)
        else: points_by_ue[ue] += guess['score']

  return points_by_ue

def correct_sorter(x,y):
  xwidth = x['high'] - x['low']
  ywidth = y['high'] - y['low']
  if xwidth != ywidth: return cmp(ywidth,xwidth)

  xmid = (x['high'] + x['low']) / 2
  ymid = (y['high'] + y['low']) / 2
  
  xoff = abs(x['answer'] - xmid)
  yoff = abs(y['answer'] - ymid)
  return cmp(yoff,xoff)

def incorrect_sorter(x,y):
  if x['low'] > x['answer']: 
    xdist_small = x['low'] - x['answer']
    xdist_large = x['high'] - x['answer']
  else:
   xdist_small = x['answer'] - x['high']
   xdist_large = x['answer'] - x['low']

  if y['low'] > y['answer']: 
    ydist_small = y['low'] - y['answer']
    ydist_large = y['high'] - y['answer']
  else:
   ydist_small = y['answer'] - y['high']
   ydist_large = y['answer'] - y['low']

  if xdist_small != ydist_small: return cmp(ydist_small,xdist_small)
  return cmp(ydist_large,xdist_large)

def assign_points(users,comparator,max_points=10):
  if len(users)==0: return

  users.sort(comparator,reverse=True)
  grouped = [ [ users[0] ] ]
  for i in range(1,len(users)):
    user = users[i]
    last = grouped[-1][-1]
    if comparator(last,user)==0:
      grouped[-1].append(user)
    else:
      grouped.append([user])

  users_per_point = math.floor(len(users)/(max_points+1))
  mod = len(users)%(max_points+1)

  if users_per_point == 0: 
    users_per_point = 1
    mod = 0

  users_so_far = 0
  for user_bucket in grouped:
    # calculate how many points this bucket should get
    bucket_points = int(max_points - math.floor(users_so_far / users_per_point))
    if bucket_points < mod:
      # this is for the lower buckets where we'll have an extra user per bucket
      max_losers = mod-1  # the max points that the lower buckets get
      losers = users_so_far - (max_points+1-mod)*users_per_point # equivalent of users_so_far but for the lower buckets
      bucket_points = int(max_losers - math.floor(losers / (users_per_point+1)))

    for user in user_bucket:
      user['score'] = bucket_points
    users_so_far += len(user_bucket)
    
    # print len(user_bucket), " - ", bucket_points