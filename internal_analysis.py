#coding=utf-8

import json
import xlsxwriter
import os
import sys


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print(f"usage: {sys.argv[0]} directory output_filename")
	else:
		directory = sys.argv[1]
		output_filename = sys.argv[2]
		if '/' not in directory:
			directory += '/'

		workbook = xlsxwriter.Workbook(output_filename)
		worksheet = workbook.add_worksheet()
		row = 0
		worksheet.write(row, 0, '城市')
		worksheet.write(row, 1, '日期')
		worksheet.write(row, 2, '强度')

		files = os.listdir(directory)
		for filename in files:
			cityname = filename.split('.')[1]
			f = open(directory + filename, "r")
			s = f.read()
			f.close()
			jobject = json.loads(s.split('(')[1].split(')')[0])
			dic = jobject['data']['list']
			try:
				for date, value in dic.items():
					row += 1
					print(f"{row}")
					worksheet.write(row, 0, cityname)
					worksheet.write(row, 1, date)
					worksheet.write(row, 2, value)
			except Exception as e:
				print("some error occured")
				print(e)

		workbook.close()