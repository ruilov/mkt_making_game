import webapp2,datetime,math
from django.utils import simplejson
from google.appengine.ext import ndb
from server_controllers import models,utils

# this API is for listing quizzes. 
# The post function can delete quizzes, activate them, or deactivate them

class Rankings(webapp2.RequestHandler):
  def get(self,qs):
    user_id_map = {}
    rank_by_user = {}
    users_query = models.User.query().fetch()
    for user in users_query:
      user_id_map[user.user_id] = user.nickname
      rank_by_user[user.nickname] = {}

    quiz_dates = []
    quizzes_query = models.Quiz.query().fetch()
    for quiz in quizzes_query:
      if quiz.status != "old": continue
      quiz_id = quiz.key.parent().id()
      quiz_dates.append({"quiz_id": quiz_id, "releaseDate": quiz.releaseDate})
      points_by_uid = score_quiz(quiz,quiz_id)
      for uid,score in points_by_uid.items():
        rank_by_user[user_id_map[uid]][quiz_id] = score

    for user in users_query:
      if len(rank_by_user[user.nickname])==0: del rank_by_user[user.nickname]

    # sort the quizzes by date
    quiz_dates.sort(key=lambda elem: elem["releaseDate"])
    utils.write_back(self,{"rank_by_user": rank_by_user, "quiz_dates": quiz_dates})

def score_quiz(quiz,quiz_id):
  fillout_query = models.Fillout.query(models.Fillout.quiz_id == quiz_id).fetch()
  points_by_uid = {}

  # collect all answers for each question in one place
  guesses_by_q = []
  for i in range(0,len(quiz.questions)): guesses_by_q.append([])
  
  for fillout in fillout_query:
    points_by_uid[fillout.user_id] = 0
    for i in range(0,len(quiz.questions)):
      try:
        low = float(fillout.guesses_low[i])
        high = float(fillout.guesses_high[i])
      except ValueError:
        low = None
        high = None
      guesses_by_q[i].append({'user_id': fillout.user_id, 'low': low, 'high': high})

  # score each question
  for i in range(0,len(quiz.questions)):
    # print quiz.questions[i].text,"|",quiz.questions[i].answer
    answer = float(quiz.questions[i].answer)
    guesses_correct = []
    guesses_incorrect = []
    guesses_problem = []
    for guess in guesses_by_q[i]:
      guess['answer'] = answer
      if guess['low']==None or guess['low']>guess['high']: guesses_problem.append(guess)
      elif guess['low']<=answer and answer<=guess['high']: guesses_correct.append(guess)
      else: guesses_incorrect.append(guess)

    assign_points(guesses_correct,correct_sorter,max_points=10)
    for guess in guesses_correct: guess['score'] += 10
    max_losers = 9 + max(11-len(guesses_correct),0)
    assign_points(guesses_incorrect,incorrect_sorter,max_points=max_losers)

    for guess in guesses_correct:
      points_by_uid[guess['user_id']] += guess['score']
      # print guess['user_id'], "|", guess['low'], "|", guess['high'], "|", guess['score']
    for guess in guesses_incorrect:
      points_by_uid[guess['user_id']] += guess['score']
      # print guess['user_id'], "|", guess['low'], "|", guess['high'], "|", guess['score']

  return points_by_uid
  # # save scores to the DB
  # rank_query = models.QuizRanking.query(ancestor=models.quiz_ranking_key(quiz_id)).fetch(1)
  # if(len(rank_query)==0):
  #   ranking = models.QuizRanking(parent=models.quiz_ranking_key(quiz_id),quiz_id=quiz_id)
  # else: 
  #   ranking = rank_query[0]
  # ranking.user_ids = points_by_uid.keys()
  # ranking.points = points_by_uid.values()
  # ranking.put()

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