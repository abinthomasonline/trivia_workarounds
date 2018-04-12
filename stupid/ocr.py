try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import webbrowser
import requests
import re
from bs4 import BeautifulSoup
import cv2

image = cv2.imread("raw.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#threshold
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

#blur
gray = cv2.medianBlur(gray, 3)

question = gray[625:976, 0:1070]
option1 = gray[994:1156, 124:964]
option2 = gray[1233:1395, 124:964]
option3 = gray[1470:1633, 124:964]

que = pytesseract.image_to_string(Image.fromarray(question))
opt1 = pytesseract.image_to_string(Image.fromarray(option1))
opt2 = pytesseract.image_to_string(Image.fromarray(option2))
opt3 = pytesseract.image_to_string(Image.fromarray(option3))

#search question directly
url = "https://www.google.co.in/search?q={}".format(que.encode('utf-8'))    
webbrowser.open(url)

#occurrence count
print "\nOCCURRENCE COUNT\n****************"
r = requests.get(url)
response_text = r.text
print opt1, "\t:", sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(opt1), response_text))
print opt2, "\t:", sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(opt2), response_text))
print opt3, "\t:", sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(opt3), response_text))

#search results count
print "\nSEARCH RESULTS COUNT\n********************"
r = requests.get("https://www.google.co.in/search?q={}".format(que.encode('utf-8')+" "+opt1.encode('utf-8')))
soup = BeautifulSoup(r.text, "html.parser")
print opt1, "\t:", soup.find('div',{'id':'resultStats'}).text.split()[1]
r = requests.get("https://www.google.co.in/search?q={}".format(que.encode('utf-8')+" "+opt2.encode('utf-8')))
soup = BeautifulSoup(r.text, "html.parser")
print opt2, "\t:", soup.find('div',{'id':'resultStats'}).text.split()[1]
r = requests.get("https://www.google.co.in/search?q={}".format(que.encode('utf-8')+" "+opt3.encode('utf-8')))
soup = BeautifulSoup(r.text, "html.parser")
print opt3, "\t:", soup.find('div',{'id':'resultStats'}).text.split()[1], "\n"