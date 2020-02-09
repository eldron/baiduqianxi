import xlrd
import sys
import xlsxwriter

if __name__ == '__main__':
	if len(sys.argv) != 4:
		print(f"usage: {sys.argv[0]} qianchu_file quezhen_file output_file")
	else:
		qianchu_file = sys.argv[1]
		quezhen_file = sys.argv[2]
		output_file = sys.argv[3]

		qianchu_book = xlrd.open_workbook(qianchu_file)
		quezhen_book = xlrd.open_workbook(quezhen_file)
		output_book = xlsxwriter.Workbook(output_file)
		output_sheet = output_book.add_worksheet()
		output_sheet.write(0, 0, "城市名称")
		output_sheet.write(0, 1, "每日单独指数")
		output_sheet.write(0, 2, "每日指数累加")
		output_sheet.write(0, 3, "五天内指数累加")
		output_sheet.write(0, 4, "七天内指数累加")
		output_sheet.write(0, 5, "十四天内指数累加")
		output_sheet.write(0, 6, "2.7确诊总数")
		output_sheet.write(0, 7, "2.7新增确诊人数")

		quezhen_sheet = quezhen_book.sheets()[0]
		quezhen_dic = {}
		for row in range(2, quezhen_sheet.nrows):
			quezhen_dic[quezhen_sheet.cell(row, 2).value] = [quezhen_sheet.cell(row, 3).value, quezhen_sheet.cell(row, 4).value]

		qianchu_dic = {}
		dandu_dic = {}
		sheet = qianchu_book.sheet_by_name("每日单独")
		specific_date = '20200207'
		for row in range(1, sheet.nrows):
			if sheet.cell(row, 1).value == specific_date:
				dandu_dic[sheet.cell(row, 0).value] = sheet.cell(row, 2).value

		leijia_dic = {}
		sheet = qianchu_book.sheet_by_name("每日累加")
		for row in range(1, sheet.nrows):
			if sheet.cell(row, 1).value == specific_date:
				leijia_dic[sheet.cell(row, 0).value] = sheet.cell(row, 2).value

		fiveday_dic = {}
		sheet = qianchu_book.sheet_by_name("五天内")
		for row in range(1, sheet.nrows):
			if sheet.cell(row, 1).value == specific_date:
				fiveday_dic[sheet.cell(row, 0).value] = sheet.cell(row, 2).value

		sevenday_dic = {}
		sheet = qianchu_book.sheet_by_name("七天内")
		for row in range(1, sheet.nrows):
			if sheet.cell(row, 1).value == specific_date:
				sevenday_dic[sheet.cell(row, 0).value] = sheet.cell(row, 2).value
		
		fourteen_dic = {}
		sheet = qianchu_book.sheet_by_name("十四天内")
		for row in range(1, sheet.nrows):
			if sheet.cell(row, 1).value == specific_date:
				fourteen_dic[sheet.cell(row, 0).value] = sheet.cell(row, 2).value


		row = 0
		for city, values in quezhen_dic.items():
			if city in dandu_dic.keys():
				dandu_index = dandu_dic[city]
				leijia_index = leijia_dic[city]
				five_index = fiveday_dic[city]
				seven_index = sevenday_dic[city]
				fourteen_index = fourteen_dic[city]
				row += 1
				output_sheet.write(row, 0, city)
				output_sheet.write(row, 1, dandu_index)
				output_sheet.write(row, 2, leijia_index)
				output_sheet.write(row, 3, five_index)
				output_sheet.write(row, 4, seven_index)
				output_sheet.write(row, 5, fourteen_index)
				output_sheet.write(row, 6, values[0])
				output_sheet.write(row, 7, values[1])
			elif city + '市' in dandu_dic.keys():
				city += '市'
				dandu_index = dandu_dic[city]
				leijia_index = leijia_dic[city]
				five_index = fiveday_dic[city]
				seven_index = sevenday_dic[city]
				fourteen_index = fourteen_dic[city]
				row += 1
				output_sheet.write(row, 0, city)
				output_sheet.write(row, 1, dandu_index)
				output_sheet.write(row, 2, leijia_index)
				output_sheet.write(row, 3, five_index)
				output_sheet.write(row, 4, seven_index)
				output_sheet.write(row, 5, fourteen_index)
				output_sheet.write(row, 6, values[0])
				output_sheet.write(row, 7, values[1])

		output_book.close()


