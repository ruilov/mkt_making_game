import urllib2,json,requests

server = 'http://localhost:8080'
# server = 'http://mktmakinggame.com'

save_quiz_url = server + '/api/quiz_editor/'
fillout_url = server + '/api/quiz/'
quizzes_url = server + '/api/quizzes/'
http_headers = {
  'content-type': 'application/json',
}
database = json.load(open('database.json'))
starting_id = 200

# annonamize the users
all_users = {}
count = 0
for quiz in database['quizzes']:
  for user in quiz['fillouts']:
    if user not in all_users:
      all_users[user] = {
        'user_email': 'user' + str(count) + '@gmail.com', 
        'user_name': 'user' + str(count)
      }
      count += 1

for quiz in database['quizzes']:
  url_params = {'id': str(starting_id)}

  # create the quiz
  resp = requests.post(url=save_quiz_url,params=url_params,headers=http_headers,data=json.dumps(quiz['quiz']))
  print resp.text
  
  # make the quiz active
  active_data = {'action': 'activate', 'id': str(starting_id)}
  resp = requests.post(url=quizzes_url,params=url_params,headers=http_headers,data=json.dumps(active_data))
  print resp

  # fill out the quiz
  for user, answers in quiz['fillouts'].items():
    answers['user_email'] = all_users[user]['user_email']
    answers['user_name'] = all_users[user]['user_name']
    resp = requests.post(url=fillout_url,params=url_params,headers=http_headers,data=json.dumps(answers))
    print user, ": ",resp

  # make the quiz old
  active_data = {'action': 'deactivate', 'id': str(starting_id)}
  resp = requests.post(url=quizzes_url,params=url_params,headers=http_headers,data=json.dumps(active_data))
  print resp

  starting_id += 1