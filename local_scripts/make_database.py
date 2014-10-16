import urllib2,json,requests

server = 'http://localhost:8080'
server = 'http://mktmakinggame.com'

save_quiz_url = server + '/quiz_editor_api/'
fillout_url = server + '/quiz_api/'
quizzes_url = server + '/quizzes_api/'
http_headers = {
  # 'Cookie': 'dev_appserver_login="test2@example.com:False:167176955777861719774"',
  'Cookie': 'ACSID=AJKiYcEuSnhDPUrKDQSs93m6K_SMjNBGF-yzo-XYW6uvby3e56G95SK4P7udOAeyXWuaARJ1t1G0GK49b5EGPDVbiToZ58gaRQr-009mPyWFCSCvS5bKPK2RXkT41TYyBbkUIH_FHhcOP6Oe_2LCUpzM-sXkM1-I_Bexsz-J89Z6lD1c7GBBB_Ls7TcGofByigJEuTyggpXWRib85BqQg3eMAdljIin39Ac_uUwpMC8PRmJbZWA_h_m79ZUxhhEWanQ7neLvRTm7TROAJK169uK7qBUJxYNfRYTTfNkD-JTWjZ9wnYXcQ-T9MCHuXa_xhH7UHCmmvRNunMtjntixRLi8jC-TyTLYnKuD-2v5riqXEoVxzXPgmK4szGUnA24vFmemvwiRFfyX6SFK7Qtw4N4o9-8gDgTVzkFSpYXst1E2hg7H4aYR5Ksja0bxHI1hKgti_b5m6yPVnog9PObGq_L_TKRFGU_hfuRDVTSy_0_5RrAGiWI2H8quzOuv-7CbGDYqMccwZcZVgnjbxbGqbPtkO_otgQF08uFckwLwHZvIf4VuKuNTq-Yy-It6pPnP7tmZwwlmNlyQJLSdV0DeDxfULuGc2VSeiUVhtiGf2FZEpAo7v8XBSSuzYrNQnA0bxS1KOYkAMspDr1WJmg1htnA8iy9egdCdCQlE_UF2A5yYwXn7oNtSKuTNdLy6e1C6asyRMnqys7ib',
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
        'user_id': str(1000 + count),
        'user_email': 'user' + str(count) + '@gmail.com', 
        'user_nickname': 'user' + str(count)
      }
      count += 1

for quiz in database['quizzes']:
  url_params = {'id': str(starting_id)}

  # create the quiz
  resp = requests.post(url=save_quiz_url,params=url_params,headers=http_headers,data=json.dumps(quiz['quiz']))
  print resp

  # make the quiz active
  active_data = {'action': 'activate', 'id': str(starting_id)}
  resp = requests.post(url=quizzes_url,params=url_params,headers=http_headers,data=json.dumps(active_data))
  print resp

  # fill out the quiz
  for user, answers in quiz['fillouts'].items():
    answers['user_id'] = all_users[user]['user_id']
    answers['user_email'] = all_users[user]['user_email']
    answers['user_nickname'] = all_users[user]['user_nickname']
    resp = requests.post(url=fillout_url,params=url_params,headers=http_headers,data=json.dumps(answers))
    print user, ": ",resp

  # make the quiz old
  active_data = {'action': 'deactivate', 'id': str(starting_id)}
  resp = requests.post(url=quizzes_url,params=url_params,headers=http_headers,data=json.dumps(active_data))
  print resp

  starting_id += 1