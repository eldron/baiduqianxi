#coding=utf-8

# 人口迁入指数分析

from bs4 import BeautifulSoup
import urllib2
import json
import xlsxwriter
import os
import sys
import chardet

# reload(sys)
# sys.setdefaultencoding('utf8')

r = os.listdir("movein_index")
print len(r)
files = []
for item in r:
	if os.path.isfile("movein_index/" + item):
		files.append(item)
print 'number of files = ' + str(len(files))

workbook = xlsxwriter.Workbook(u"人口迁入指数.xlsx") 
for filename in files:
	print 'processing ' + filename
	cityname = filename[13:].split(".")[0]
	print cityname
	print chardet.detect(cityname)
	worksheet = workbook.add_worksheet(cityname.decode('gbk'))
	worksheet.write(0, 0, u"日期")
	worksheet.write(0, 1, u"指数")

	f = open("movein_index/" + filename, "r")
	s = f.read()
	f.close()
	jobject = json.loads(s[3:-2])
	dic = jobject['data']['list']
	# key is unicode string, value is float number
	row = 1
	try:
		for date, value in dic.iteritems():
			#print date + "	" + str(value / 10000)
			worksheet.write(row, 0, date)
			worksheet.write(row, 1, value / 10000)
			row += 1
	except:
		print 'some error occured'
workbook.close()