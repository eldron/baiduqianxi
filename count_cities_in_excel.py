from xlrd import open_workbook
import sys

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print(f'usage: {sys.argv[0]} filename')
	else:
		filename = sys.argv[1]
		book = open_workbook(filename)
		sheet = book.sheets()[0]

		names = []
		for i in range(1, sheet.nrows):
			#print(str(i))
			if sheet.cell(i, 0).value not in names:
				names.append(sheet.cell(i, 0).value)
		print(f'{len(names)} cities in file {filename}')
		#book.close()