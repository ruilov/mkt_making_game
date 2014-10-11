# import urllib2,json,requests

# quiz_id = 0
# url = 'http://localhost:8080/scores_api/?id=' + str(quiz_id)
# resp = requests.get(url=url)
# data = resp.json()

# for question in data["questions"]:
#   print question["text"], ": ", question["answer"]
#   for user,guess in question["guesses"].items():
#     print user, 'guessed: ', '[', guess["low"], " - ",guess["high"], "]"
#   print ""

import re
m = re.search('/(.*)/admin_(.*)', '/#/admin_quizzes')
print m.group(0)
print m.group(1)
print m.group(2)