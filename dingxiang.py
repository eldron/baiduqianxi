import urllib.request
from bs4 import BeautifulSoup
import json
import sys
import xlsxwriter


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print(f"usage: {sys.argv[0]} filename")
	else:
		filename = sys.argv[1]
		url = 'http://ncov.dxy.cn/ncovh5/view/pneumonia'
		page = urllib.request.urlopen(url)
		data = page.read()
		soup = BeautifulSoup(data, 'lxml')
		script = soup.find_all('script', {'id':'getAreaStat'})[0]
		s = script.get_text()
		alen = len(s.split('[')[0])
		blen = len(s.split(']')[-1])
		j = json.loads(s[alen:0-blen])
		workbook = xlsxwriter.Workbook(filename)
		province_sheet = workbook.add_worksheet("省份")
		city_sheet = workbook.add_worksheet("城市")
		gloabl_sheet = workbook.add_worksheet("国际")
		row = 0
		province_sheet.write(row, 0, '省份')
		province_sheet.write(row, 1, '确诊')
		province_sheet.write(row, 2, '疑似')
		province_sheet.write(row, 3, '死亡')
		province_sheet.write(row, 4, '治愈')
		for province in j:
			row += 1
			province_sheet.write(row, 0, province['provinceName'])
			province_sheet.write(row, 1, province['confirmedCount'])
			province_sheet.write(row, 2, province['suspectedCount'])
			province_sheet.write(row, 3, province['deadCount'])
			province_sheet.write(row, 4, province['curedCount'])
		
		row = 0
		city_sheet.write(row, 0, '城市')
		city_sheet.write(row, 1, '省份')
		city_sheet.write(row, 2, '确诊')
		city_sheet.write(row, 3, '疑似')
		city_sheet.write(row, 4, '死亡')
		city_sheet.write(row, 5, '治愈')
		for province in j:
			for city in province['cities']:
				row += 1
				city_sheet.write(row, 0, city['cityName'])
				city_sheet.write(row, 1, province['provinceName'])
				city_sheet.write(row, 2, city['confirmedCount'])
				city_sheet.write(row, 3, city['suspectedCount'])
				city_sheet.write(row, 4, city['deadCount'])
				city_sheet.write(row, 5, city['curedCount'])

		script = soup.find_all('script', {'id':'getListByCountryTypeService2'})[0]
		s = script.get_text()
		alen = len(s.split('[')[0])
		blen = len(s.split(']')[-1])
		j = json.loads(s[alen:0-blen])
		row = 0
		gloabl_sheet.write(row, 0, "州")
		gloabl_sheet.write(row, 1, "国家")
		gloabl_sheet.write(row, 2, "确诊")
		gloabl_sheet.write(row, 3, "疑似")
		gloabl_sheet.write(row, 4, "死亡")
		gloabl_sheet.write(row, 5, "治愈")
		for item in j:
			row += 1
			gloabl_sheet.write(row, 0, item['continents'])
			gloabl_sheet.write(row, 1, item['provinceName'])
			gloabl_sheet.write(row, 2, item['confirmedCount'])
			gloabl_sheet.write(row, 3, item['suspectedCount'])
			gloabl_sheet.write(row, 4, item['deadCount'])
			gloabl_sheet.write(row, 5, item['curedCount'])

		workbook.close()