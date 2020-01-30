#coding=utf-8

# 人口迁入详情分析

from bs4 import BeautifulSoup
import urllib2
import json
import xlsxwriter
import os
import sys
import chardet

# reload(sys)
# sys.setdefaultencoding('utf8')

r = os.listdir("movein_details")
print len(r)
files = []
for item in r:
	if os.path.isfile("movein_details/" + item):
		files.append(item)
print 'number of files = ' + str(len(files))

dic = {}
for filename in files:
	print 'processing ' + filename
	cityname = filename[13:].split(".")[0]
	if cityname not in dic.keys():
		dic[cityname] = {}
	date = filename[13:].split(".")[1]
	# print cityname
	# print chardet.detect(cityname)
	# worksheet = workbook.add_worksheet(cityname.decode('gbk'))
	# worksheet.write(0, 0, u"日期")
	# worksheet.write(0, 1, u"指数")

	f = open("movein_details/" + filename, "r")
	s = f.read()
	f.close()
	jobject = json.loads(s[3:-2])
	detailed_data = jobject['data']['list']
	# detailed[u'city_name']
	# detailed_data[u'province_name']
	# detailed_data[u'value']
	dic[cityname][date] = detailed_data

# now dic contains data
print 'length of dic is: ' + str(len(dic.keys()))
workbook = xlsxwriter.Workbook(u"人口迁入详情.xlsx") 
for city, data_per_day in dic.iteritems():
	worksheet = workbook.add_worksheet(city.decode('gbk'))
	worksheet.write(0, 0, u"日期")
	worksheet.write(0, 1, u"省份")
	worksheet.write(0, 2, u"城市")
	worksheet.write(0, 3, u"百分比")
	row = 1
	for date, detailed_data in data_per_day.iteritems():
		#worksheet.write(row, 0, date)
		for item in detailed_data:
			worksheet.write(row, 0, date)
			print item[u'province_name']
			#encoding = chardet.detect(item[u'province_name'])
			#print encoding
			worksheet.write(row, 1, item[u'province_name'])
			worksheet.write(row, 2, item[u"city_name"])
			worksheet.write(row, 3, item[u'value'])
			row += 1
workbook.close()