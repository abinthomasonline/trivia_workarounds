# coding=utf-8
from uiautomator import device as d
from bs4 import BeautifulSoup
import webbrowser
import requests
import re

app = "mobs"

cheat = {"qure": {"q": "qureka.live.game.show:id/question", "a": ["qureka.live.game.show:id/option_one", "qureka.live.game.show:id/option_two", "qureka.live.game.show:id/option_three"]},
		 "brba": {"q":	"", "a": ["", "", ""]},
		 "mobs": {"q":	"com.portkey.mobshow:id/question_text", "a": ["com.portkey.mobshow:id/option_button_a", "com.portkey.mobshow:id/option_button_b", "com.portkey.mobshow:id/option_button_c"]},
		 "just": {"q":	"", "a": ["", "", ""]},
		 "stup": {"q":	"", "a": ["", "", ""]},
		 "loco": {"q":	"", "a": ["", "", ""]}}

xml = d.dump()
soup = BeautifulSoup(xml, 'lxml-xml')
question=soup.findAll("node", {"resource-id": cheat[app]["q"]})[0]["text"]
answer_one=soup.findAll("node", {"resource-id": cheat[app]["a"][0]})[0]
answer_two=soup.findAll("node", {"resource-id": cheat[app]["a"][1]})[0]
answer_three=soup.findAll("node", {"resource-id": cheat[app]["a"][2]})[0]

#search question directly
url = "https://www.google.co.in/search?q={}".format(question.encode('utf-8'))    
webbrowser.open(url)

#occurrence count
print "\nOCCURRENCE COUNT\n****************"
r = requests.get(url)
response_text = r.text
print answer_one["text"], "\t:", sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(answer_one["text"]), response_text))
print answer_two["text"], "\t:", sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(answer_two["text"]), response_text))
print answer_three["text"], "\t:", sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(answer_three["text"]), response_text))

#search results count
print "\nSEARCH RESULTS COUNT\n********************"
r = requests.get("https://www.google.co.in/search?q={}".format(question.encode('utf-8')+" "+answer_one["text"].encode('utf-8')))
soup = BeautifulSoup(r.text, "html.parser")
print answer_one["text"], "\t:", soup.find('div',{'id':'resultStats'}).text.split()[1]
r = requests.get("https://www.google.co.in/search?q={}".format(question.encode('utf-8')+" "+answer_two["text"].encode('utf-8')))
soup = BeautifulSoup(r.text, "html.parser")
print answer_two["text"], "\t:", soup.find('div',{'id':'resultStats'}).text.split()[1]
r = requests.get("https://www.google.co.in/search?q={}".format(question.encode('utf-8')+" "+answer_three["text"].encode('utf-8')))
soup = BeautifulSoup(r.text, "html.parser")
print answer_three["text"], "\t:", soup.find('div',{'id':'resultStats'}).text.split()[1]