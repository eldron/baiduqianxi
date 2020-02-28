from bs4 import BeautifulSoup
import urllib.request
import sys
import os

part1 = "https://x.cnki.net/resource/CMFD/2006158909.NH/images/Dissertation_2006158909_"
#  1.jpg"
for i in range(1, 80):
	url = part1 + str(i) + ".jpg"
	request_page = urllib.request.urlopen(url)
	f = open(str(i) + ".jpg", "wb")
	f.write(request_page.read())
	f.close()
