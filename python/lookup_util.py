import datetime, math, hashlib, utils
from quiz_model import Quiz
from user_model import Fillout,User,fillout_key,QuestionRatings,getUser

def do_lookup(request,user=None):
  ans = {"logged": "yes"}
  if not user:
    user = getUser(request)

  if not user:
    ans["logged"] = "no"  # users who haven't logged in can't see any data
    return ans

  ans["user_name"] = user.name
  ans["user_email"] = user.email
  ans["is_admin"] = user.is_admin()

  # get all the users and their usernames
  all_users = User.query().fetch()  
  user_by_name = {user.name: user} 
  for useri in all_users:
    user_by_name[useri.name] = useri

  # get all the fillouts. This is not strongly consistent. We only need to do that for the current user
  fillout_query = Fillout.query().fetch()
  fillouts = {}
  for fillout in fillout_query:
    if fillout.quiz_id not in fillouts: fillouts[fillout.quiz_id] = {}
    fillouts[fillout.quiz_id][fillout.username] = fillout.to_dict()

  # information about quizzes
  query = Quiz.query().fetch()
  ans["quizzes"] = []
  for quiz in query:
    if not ans["is_admin"] and quiz.status=="editor": continue
    quiz_dict = quiz.to_dict();
    quiz_id = quiz.key.parent().id()
    quiz_dict["id"] = quiz_id

    # get the fillouts for this quiz
    this_fillouts = fillouts.get(quiz_id,{})
    fillout_user_query = Fillout.query(ancestor=fillout_key(user.name,quiz_id)).fetch()
    if len(fillout_user_query)>0:
      fillout = fillout_user_query[0].to_dict()
      this_fillouts[user.name] = fillout
      quiz_dict["fillout"] = fillout

    if user.name in this_fillouts or quiz_dict["status"]=="old":
      quiz_dict["scores"] = score_quiz(quiz,this_fillouts)
    else: # the user hasn't filled this quiz yet, and shouldn't be able to see the answers
      for question in quiz_dict["questions"]:
        del question["answer"]
        del question["source"]

    # question ratings
    ratingQuery = QuestionRatings.query(QuestionRatings.quiz_id==quiz_id,QuestionRatings.username==ans["user_name"]).fetch()
    if len(ratingQuery)>0:
      ratings = ratingQuery[0].ratings
      for idx,rating in enumerate(ratings):
        if(rating!=-1): quiz_dict["questions"][idx]["rating"] = rating

    ans["quizzes"].append(quiz_dict)

  return ans

def score_quiz(quiz,fillouts):
  points_by_user = {}

  guesses_by_q = []
  for i in range(0,len(quiz.questions)): guesses_by_q.append([])
  
  for user_id,fillout in fillouts.items():
    if fillout["ranked"] != None and not fillout["ranked"]: continue
    points_by_user[user_id] = []
    for i in range(0,len(quiz.questions)):
      guesses_by_q[i].append({'user_id': user_id, 'low': fillout["guesses_low"][i], 'high': fillout["guesses_high"][i]})

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
        user_id = guess['user_id']
        del guess['user_id']
        del guess['answer']
        points_by_user[user_id].append(guess)

  return points_by_user

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