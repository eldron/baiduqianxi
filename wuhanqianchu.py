#coding=utf-8

# 武汉迁出分析

from bs4 import BeautifulSoup
import urllib.request
import sys
import os
import json
import xlsxwriter

def sumvalue(dic, days, city, startidx, endidx):
	sum = 0
	for idx in range(startidx, endidx + 1):
		sum += dic[city][days[idx]]
	return sum

if __name__ == '__main__':
	if len(sys.argv) != 5:
		print(f"usage: {sys.argv[0]} startdate enddate directory output_filename")
	else:
		monthoneandtwo = []
		for item in range(20200101, 20200132):
			monthoneandtwo.append(str(item))
		for item in range(20200201, 20200229):
			monthoneandtwo.append(str(item))
		wuhanid = '420100'
		startdate = sys.argv[1]
		enddate = sys.argv[2]
		directory = sys.argv[3]
		output_filename = sys.argv[4]
		if '/' not in directory:
			directory += '/'
		days = []
		flag = False
		if startdate == enddate:
			days.append(startdate)
		else:
			for item in monthoneandtwo:
				if startdate == item:
					flag = True
					days.append(item)
				elif enddate == item:
					flag = False
					days.append(item)
					break
				elif flag:
					days.append(item)
		for item in days:
			print(item)

		files = set(os.listdir(directory))
		details_partone = "http://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=" + wuhanid + '&type=move_out&date='
		for date in days:
			request_url = details_partone + date
			filename = u"人口迁出详情 武汉" + '.' + date + '.html'
			if filename not in files:
				print('request_url is: ' + request_url)
				request_page = urllib.request.urlopen(request_url)
				print('filename is: ' + filename)
				f = open(directory + filename, "wb")
				f.write(request_page.read())
				f.close()

		partone = "http://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id="
		parttwo = "&type="
		partthree = "&startDate="
		partfour = "&endDate="
		index_url = partone + wuhanid + parttwo + 'move_out' + partthree + startdate + partfour + enddate
		filename = "人口迁出指数 武汉" + '.' + startdate + '.' + enddate + '.html'
		if filename not in files:
			request_page = urllib.request.urlopen(index_url)
			print('filename is: ' + filename)
			f = open(directory + filename, "wb")
			f.write(request_page.read())
			f.close()

		# analysis data
		filename = "人口迁出指数 武汉" + '.' + startdate + '.' + enddate + '.html'
		f = open(directory + filename, "r")
		s = f.read()
		f.close()
		jobject = json.loads(s.split('(')[1].split(')')[0])
		datetoindex = jobject['data']['list']

		datetodetails = {}
		for date in days:
			filename = directory + u"人口迁出详情 武汉" + '.' + date + '.html'
			cityname = filename.split(' ')[1].split('.')[0]
			f = open(filename, "r")
			s = f.read()
			f.close()
			jobject = json.loads(s.split('(')[1].split(')')[0])
			detailed_data = jobject['data']['list']
			datetodetails[date] = detailed_data
			# for item in detailed_data

		citynames = set()
		for date in days:
			for item in datetodetails[date]:
				citynames.add(item['city_name'])

		# write to file
		workbook = xlsxwriter.Workbook(output_filename)
		worksheet = workbook.add_worksheet("每日单独")
		row = 0
		worksheet.write(row, 0, '迁出城市')
		worksheet.write(row, 1, '日期')
		worksheet.write(row, 2, '指数*百分比')
		# for date in days:
		# 	for item in datetodetails[date]:
		# 		row += 1
		# 		worksheet.write(row, 0, '武汉')
		# 		worksheet.write(row, 1, date)
		# 		worksheet.write(row, 2, datetoindex[date])
		# 		worksheet.write(row, 3, item['province_name'])
		# 		worksheet.write(row, 4, item['city_name'])
		# 		worksheet.write(row, 5, item['value'])
		# 		worksheet.write(row, 6, datetoindex[date] * item['value'])
		

		citynamedate_to_value = {}
		

		for name in citynames:
			citynamedate_to_value[name] = {}
		for name in citynames:
			for date in days:
				citynamedate_to_value[name][date] = 0 # initialize

		for date in days:
			for item in datetodetails[date]:
				if item['city_name'] not in citynamedate_to_value.keys():
					citynamedate_to_value[item['city_name']] = {}
				
				citynamedate_to_value[item['city_name']][date] = datetoindex[date] * item['value']
				print(f"{item['city_name']} {date} {citynamedate_to_value[item['city_name']][date]}")
		
		for name in citynames:
			for date in days:
				row += 1
				worksheet.write(row, 0, name)
				worksheet.write(row, 1, date)
				worksheet.write(row, 2, citynamedate_to_value[name][date])

		# for city in citynames:
		# 	for date in days:
		# 		print(f"{city} {date} {str(citynamedate_to_value[city][date])}")

		# 每日累加
		cityname_to_daily_accumulate = {}
		for name in citynames:
			cityname_to_daily_accumulate[name] = {}
		for city in citynames:
			sum = 0
			for date in days:
				sum += citynamedate_to_value[city][date]
				cityname_to_daily_accumulate[city][date] = sum

		worksheet = workbook.add_worksheet("每日累加")
		row = 0
		worksheet.write(row, 0, "迁出城市")
		worksheet.write(row, 1, "日期")
		worksheet.write(row, 2, "指数乘以百分比 每日累加结果")
		for city in citynames:
			for date in days:
				row += 1
				worksheet.write(row, 0, city)
				worksheet.write(row, 1, date)
				worksheet.write(row, 2, cityname_to_daily_accumulate[city][date])


		# 5天内
		fivedays = {}
		for name in citynames:
			fivedays[name] = {}
		for name in citynames:
			for date in days:
				fivedays[city][date] = 0
		
		for name in citynames:
			idx = 0
			for date in days:
				if idx < 5:
					fivedays[name][date] = sumvalue(citynamedate_to_value, days, name, 0, idx)
				else:
					fivedays[name][date] = sumvalue(citynamedate_to_value, days, name, idx - 4, idx)

				idx += 1

		worksheet = workbook.add_worksheet("五天内")
		row = 0
		worksheet.write(row, 0, '迁出城市')
		worksheet.write(row, 1, '日期')
		worksheet.write(row, 2, '五天内指数乘以百分比累加结果')
		for name in citynames:
			for date in days:
				row += 1
				worksheet.write(row, 0, name)
				worksheet.write(row, 1, date)
				worksheet.write(row, 2, fivedays[name][date])
		
		# 7天内
		sevendays = {}
		for name in citynames:
			sevendays[name] = {}
		for name in citynames:
			for date in days:
				sevendays[name][date] = 0
		for name in citynames:
			idx = 0
			for date in days:
				if idx < 7:
					sevendays[name][date] = sumvalue(citynamedate_to_value, days, name, 0, idx)
				else:
					sevendays[name][date] = sumvalue(citynamedate_to_value, days, name, idx - 6, idx)
				idx += 1

		worksheet = workbook.add_worksheet("七天内")
		row = 0
		worksheet.write(row, 0, '迁出城市')
		worksheet.write(row, 1, '日期')
		worksheet.write(row, 2, '七天内指数乘以百分比累加结果')
		for name in citynames:
			for date in days:
				row += 1
				worksheet.write(row, 0, name)
				worksheet.write(row, 1, date)
				worksheet.write(row, 2, sevendays[name][date])

		# 14天内
		fourteendays = {}
		for name in citynames:
			fourteendays[name] = {}
		for name in citynames:
			for date in days:
				fourteendays[name][date] = 0
		for name in citynames:
			idx = 0
			for date in days:
				if idx < 14:
					fourteendays[name][date] = sumvalue(citynamedate_to_value, days, name, 0, idx)
				else:
					fourteendays[name][date] = sumvalue(citynamedate_to_value, days, name, idx - 13, idx)
				idx += 1

		worksheet = workbook.add_worksheet("十四天内")
		row = 0
		worksheet.write(row, 0, '迁出城市')
		worksheet.write(row, 1, '日期')
		worksheet.write(row, 2, '十四天内指数乘以百分比累加结果')
		for name in citynames:
			for date in days:
				row += 1
				worksheet.write(row, 0, name)
				worksheet.write(row, 1, date)
				worksheet.write(row, 2, fourteendays[name][date])

		workbook.close()

