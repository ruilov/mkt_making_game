import urllib2,json,requests

quiz_id = 200
url = 'http://localhost:8080/api/scores/?id=' + str(quiz_id)
# url = 'http://mktmakinggame.com/api/scores/?id=' + str(quiz_id)
resp = requests.get(url=url)
data = resp.json()

for question in data["questions"]:
  print question["text"], ": ", question["answer"]
  for user,guess in question["guesses"].items():
    # if "user" in user: continue
    print user, '|', guess["low"], "|",guess["high"]
  print ""