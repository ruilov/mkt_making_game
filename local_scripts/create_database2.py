import urllib2,json,requests

# server = 'http://localhost:8080'
server = 'http://mktmakinggame.com'

save_quiz_url = server + '/quiz_editor_api/'
fillout_url = server + '/quiz_api/'
quizzes_url = server + '/quizzes_api/'
http_headers = {
  'content-type': 'application/json',
}
database = json.load(open('converted.txt'))

user_names = {}
for user in database["users"]:
  user_names[user["email"]] = user["name"]

starting_id = 200
for quiz in database['quizzes']:
  url_params = {'id': str(starting_id)}

  # create the quiz
  resp = requests.post(url=save_quiz_url,params=url_params,headers=http_headers,data=json.dumps(quiz))
  print resp.text

  # make the quiz active
  active_data = {'action': 'activate', 'id': str(starting_id)}
  resp = requests.post(url=quizzes_url,params=url_params,headers=http_headers,data=json.dumps(active_data))
  print resp.text
  starting_id += 1

for fillout in database['fillouts']:
  url_params = {'id': str(fillout["quiz_id"])}
  data = {}
  data["user_email"] = fillout["user_email"]
  data["user_name"] = user_names[fillout["user_email"]]
  data["questions"] = []
  for i in range(0,len(fillout["guesses_low"])):
    data["questions"].append({"guess_low": fillout["guesses_low"][i], "guess_high": fillout["guesses_high"][i]})
  resp = requests.post(url=fillout_url,params=url_params,headers=http_headers,data=json.dumps(data))
  print resp.text

  # make the quiz old
  active_data = {'action': 'deactivate', 'id': str(starting_id)}
  resp = requests.post(url=quizzes_url,params=url_params,headers=http_headers,data=json.dumps(active_data))
  print resp

starting_id = 200
for quiz in database['quizzes']:
  url_params = {'id': str(starting_id)}
  active_data = {'action': 'deactivate', 'id': str(starting_id)}
  resp = requests.post(url=quizzes_url,params=url_params,headers=http_headers,data=json.dumps(active_data))
  print resp.text
  starting_id += 1