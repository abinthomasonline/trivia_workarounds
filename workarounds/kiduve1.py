from uiautomator import device as d
from bs4 import BeautifulSoup
import webbrowser
import requests
import re

app = "loco"

cheat = {"loco": {"q": "com.showtimeapp:id/question", "a": "com.showtimeapp:id/answer"},
		 "qure": {"q": "", "a": ""},
		 "brba": {"q": "", "a": ""},
		 "stup": {"q": "", "a": ""},
		 "just": {"q": "", "a": ""},
		 "mobs": {"q": "", "a": ""}}

xml = d.dump()
soup = BeautifulSoup(xml, 'lxml-xml')
question=soup.findAll("node", {"resource-id": cheat[app]["q"]})[0]["text"]
answers=soup.findAll("node", {"resource-id": cheat[app]["a"]})

#search question directly
url = "https://www.google.co.in/search?q={}".format(question.encode('utf-8'))    
webbrowser.open(url)

#occurrence count
print "\nOCCURRENCE COUNT\n****************"
r = requests.get(url)
response_text = r.text
for a in answers:
	print a["text"], "\t:", sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(a["text"]), response_text))

#search results count
print "\nSEARCH RESULTS COUNT\n********************"
for a in answers:
	r = requests.get("https://www.google.co.in/search?q={}".format(question.encode('utf-8')+" "+a["text"].encode('utf-8')))
	soup = BeautifulSoup(r.text, "html.parser")
	print a["text"], "\t:", soup.find('div',{'id':'resultStats'}).text.split()[1]