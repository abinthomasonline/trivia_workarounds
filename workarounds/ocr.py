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

cv2.imwrite('screen.png', gray)

pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

text = pytesseract.image_to_string(Image.open('screen.png'))
print text
lis = text.split("\n\n")

opt3 = lis[-1]
opt2 = lis[-2]
opt1 = lis[-3]
que = lis[-4].replace("\n", " ")

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