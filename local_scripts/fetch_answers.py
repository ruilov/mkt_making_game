import urllib2,json,requests

quiz_id = 200
url = 'http://localhost:8080/scores_api/?id=' + str(quiz_id)
# url = 'http://mktmakinggame.com/scores_api/?id=' + str(quiz_id)
resp = requests.get(url=url)
data = resp.json()

for question in data["questions"]:
  print question["text"], ": ", question["answer"]
  for user,guess in question["guesses"].items():
    if user!="user14@gmail.com": continue
    print user, 'guessed: ', '[', guess["low"], " - ",guess["high"], "]"
  print ""