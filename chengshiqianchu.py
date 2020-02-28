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
	if len(sys.argv) != 6:
		print(f"usage: {sys.argv[0]} startdate enddate directory output_filename chengshi")
	else:

		beijingid = '110000'
		shanghaiid = '310000'
		guangzhouid = '440100'
		shenzhenid = '440300'

		provinces = [u"河北", u"山西", u"辽宁", u"吉林", u"黑龙江", u"江苏", u"浙江", u"安徽", u'福建', u'江西', u'山东', u'河南', u'湖北', u'湖南', u'广东', u'海南', u'四川', u'贵州', u'云南', u'陕西', u'甘肃', u'青海', u'台湾']
		autonomous = [u'内蒙古', u'广西', u'西藏', u'宁夏', u'新疆']
		autonomous_regions = [u'内蒙古自治区', u'广西壮族自治区', u'西藏自治区', u'宁夏回族自治区', u'新疆维吾尔自治区']

		s = u"北京|110000,天津|120000,兴安盟|152200,巢湖|340181,定安|469021,屯昌|469022,澄迈|469023,临高|469024,海东地区|630200,香港|810000,澳门|820000,昌都|540300,昌都地区|540300,山南|540500,山南地区|540500,日喀则|540200,日喀则地区|540200,那曲|540600,那曲地区|540600,林芝|540400,林芝地区|540400,吐鲁番|650400,吐鲁番地区|650400,铜仁|520600,铜仁地区|520600,毕节|520500,毕节地区|520500,广西|450000,广西壮族自治区|450000,内蒙古|150000,内蒙古自治区|150000,宁夏|640000,宁夏回族自治区|640000,新疆|650000,新疆维吾尔自治区|650000,西藏|540000,西藏自治区|540000,石家庄|130100,唐山|130200,秦皇岛|130300,邯郸|130400,邢台|130500,保定|130600,张家口|130700,承德|130800,沧州|130900,廊坊|131000,衡水|131100,太原|140100,大同|140200,阳泉|140300,长治|140400,晋城|140500,朔州|140600,晋中|140700,运城|140800,忻州|140900,临汾|141000,吕梁|141100,呼和浩特|150100,包头|150200,乌海|150300,赤峰|150400,通辽|150500,鄂尔多斯|150600,呼伦贝尔|150700,巴彦淖尔|150800,乌兰察布|150900,沈阳|210100,大连|210200,鞍山|210300,抚顺|210400,本溪|210500,丹东|210600,锦州|210700,营口|210800,阜新|210900,辽阳|211000,盘锦|211100,铁岭|211200,朝阳|211300,葫芦岛|211400,长春|220100,吉林市|220200,四平|220300,辽源|220400,通化|220500,白山|220600,松原|220700,白城|220800,哈尔滨|230100,齐齐哈尔|230200,鸡西|230300,鹤岗|230400,双鸭山|230500,大庆|230600,伊春|230700,佳木斯|230800,七台河|230900,牡丹江|231000,黑河|231100,绥化|231200,上海|310000,南京|320100,无锡|320200,徐州|320300,常州|320400,苏州|320500,南通|320600,连云港|320700,淮安|320800,盐城|320900,扬州|321000,镇江|321100,泰州|321200,宿迁|321300,浙江|330000,杭州|330100,宁波|330200,温州|330300,嘉兴|330400,湖州|330500,绍兴|330600,金华|330700,衢州|330800,舟山|330900,台州|331000,丽水|331100,合肥|340100,芜湖|340200,蚌埠|340300,淮南|340400,马鞍山|340500,淮北|340600,铜陵|340700,安庆|340800,黄山|341000,滁州|341100,阜阳|341200,宿州|341300,六安|341500,亳州|341600,池州|341700,宣城|341800,福州|350100,厦门|350200,莆田|350300,三明|350400,泉州|350500,漳州|350600,南平|350700,龙岩|350800,宁德|350900,南昌|360100,景德镇|360200,萍乡|360300,九江|360400,新余|360500,鹰潭|360600,赣州|360700,吉安|360800,宜春|360900,抚州|361000,上饶|361100,济南|370100,莱芜|370100,青岛|370200,淄博|370300,枣庄|370400,东营|370500,烟台|370600,潍坊|370700,济宁|370800,泰安|370900,威海|371000,日照|371100,临沂|371300,德州|371400,聊城|371500,滨州|371600,菏泽|371700,郑州|410100,开封|410200,洛阳|410300,平顶山|410400,安阳|410500,鹤壁|410600,新乡|410700,焦作|410800,濮阳|410900,许昌|411000,漯河|411100,三门峡|411200,南阳|411300,商丘|411400,信阳|411500,周口|411600,驻马店|411700,武汉|420100,黄石|420200,十堰|420300,宜昌|420500,襄阳|420600,鄂州|420700,荆门|420800,孝感|420900,荆州|421000,黄冈|421100,咸宁|421200,随州|421300,仙桃|429004,潜江|429005,天门|429006,长沙|430100,株洲|430200,湘潭|430300,衡阳|430400,邵阳|430500,岳阳|430600,常德|430700,张家界|430800,益阳|430900,郴州|431000,永州|431100,怀化|431200,娄底|431300,广州|440100,韶关|440200,深圳|440300,珠海|440400,汕头|440500,佛山|440600,江门|440700,湛江|440800,茂名|440900,肇庆|441200,惠州|441300,梅州|441400,汕尾|441500,河源|441600,阳江|441700,清远|441800,东莞|441900,济源|419001,中山|442000,潮州|445100,揭阳|445200,云浮|445300,南宁|450100,柳州|450200,桂林|450300,梧州|450400,北海|450500,防城港|450600,钦州|450700,贵港|450800,玉林|450900,百色|451000,贺州|451100,河池|451200,来宾|451300,崇左|451400,海口|460100,三亚|460200,三亚|460300,五指山|469001,琼海|469002,儋州|460400,文昌|469005,万宁|469006,东方|469007,重庆|500000,成都|510100,自贡|510300,攀枝花|510400,泸州|510500,德阳|510600,绵阳|510700,广元|510800,遂宁|510900,内江|511000,乐山|511100,南充|511300,眉山|511400,宜宾|511500,广安|511600,达州|511700,雅安|511800,巴中|511900,资阳|512000,贵阳|520100,六盘水|520200,遵义|520300,安顺|520400,昆明|530100,曲靖|530300,玉溪|530400,保山|530500,昭通|530600,丽江|530700,临沧|530900,普洱|530800,拉萨|540100,西安|610100,铜川|610200,宝鸡|610300,咸阳|610400,渭南|610500,延安|610600,汉中|610700,榆林|610800,安康|610900,商洛|611000,兰州|620100,嘉峪关|620200,金昌|620300,白银|620400,天水|620500,武威|620600,张掖|620700,平凉|620800,酒泉|620900,庆阳|621000,定西|621100,陇南|621200,西宁|630100,银川|640100,石嘴山|640200,吴忠|640300,固原|640400,中卫|640500,乌鲁木齐|650100,克拉玛依|650200,石河子|659001,阿拉尔|659002,图木舒克|659003,五家渠|659004,北屯|659005,铁门关|659006,双河|659007,可克达拉|659008,昆玉|659009,恩施|422800,恩施土家族苗族自治州|422800,延边|222400,延边朝鲜族自治州|222400,神农架地区|429021,神农架林区|429021,湘西州|433100,湘西土家族苗族自治州|433100,大兴安岭地区|232700,白沙县|469025,白沙黎族自治县|469025,昌江黎族自治县|469026,乐东黎族自治县|469027,陵水黎族自治县|469028,保亭黎族苗族自治县|469029,琼中黎族苗族自治县|469030,阿坝州|513200,阿坝藏族羌族自治州|513200,甘孜州|513300,甘孜藏族自治州|513300,凉山州|513400,凉山彝族自治州|513400,黔西南布依族苗族自治州|522300,黔东南苗族侗族自治州|522600,黔南布依族苗族自治州|522700,楚雄州|532300,楚雄彝族自治州|532300,红河州|532500,红河哈尼族彝族自治州|532500,文山|532600,文山壮族苗族自治州|532600,西双版纳傣族自治州|532800,大理州|532900,大理白族自治州|532900,德宏州|533100,德宏傣族景颇族自治州|533100,怒江州|533300,怒江傈僳族自治州|533300,迪庆州|533400,迪庆藏族自治州|533400,阿里地区|542500,临夏回族自治州|622900,甘南藏族自治州|623000,海北州|632200,海北藏族自治州|632200,黄南州|632300,黄南藏族自治州|632300,海南州|632500,海南藏族自治州|632500,果洛州|632600,果洛藏族自治州|632600,玉树州|632700,玉树藏族自治州|632700,海西州|632800,海西蒙古族藏族自治州|632800,昌吉州|652300,昌吉回族自治州|652300,博尔塔拉州|652700,博尔塔拉蒙古自治州|652700,巴音郭楞蒙古自治州|652800,哈密|650500,哈密地区|650500,阿克苏地区|652900,克孜勒苏州|653000,克孜勒苏柯尔克孜自治州|653000,伊犁州|654000,伊犁哈萨克自治州|654000,喀什地区|653100,和田地区|653200,塔城地区|654200,阿勒泰地区|654300,锡林郭勒盟|152500,阿拉善盟|152900,安徽|340000,福建|350000,甘肃|620000,广东|440000,贵州|520000,海南|460000,河北|130000,黑龙江|230000,河南|410000,湖北|420000,湖南|430000,江苏|320000,江西|360000,吉林|220000,辽宁|210000,青海|630000,山东|370000,山西|140000,陕西|610000,四川|510000,云南|530000"
		cities = s.split(u",")
		cdic = {}# city id to name
		nametoid = {}
		#ids = []
		for city in cities:
			r = city.split(u"|")
			print('city name is: ' + r[0] + ' id is: ' + r[1])
			if r[0] not in provinces and r[0] not in autonomous and r[0] not in autonomous_regions:
				nametoid[r[0]] = r[1]
				if r[1] not in cdic.keys():
					cdic[r[1]] = r[0]

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
		chengshi = sys.argv[5]
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

		chengshiid = beijingid
		if chengshi == '北京':
			chengshiid = beijingid
		elif chengshi == '上海':
			chengshiid = shanghaiid
		elif chengshi == '广州':
			chengshiid = guangzhouid
		elif chengshi == '深圳':
			chengshiid = shenzhenid
		else:
			chengshiid = nametoid[chengshi]

		files = set(os.listdir(directory))
		details_partone = "http://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=" + chengshiid + '&type=move_out&date='
		for date in days:
			request_url = details_partone + date
			filename = u"人口迁出详情 " + chengshi + '.' + date + '.html'
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
		index_url = partone + chengshiid + parttwo + 'move_out' + partthree + startdate + partfour + enddate
		filename = "人口迁出指数 " + chengshi + '.' + startdate + '.' + enddate + '.html'
		if filename not in files:
			request_page = urllib.request.urlopen(index_url)
			print('filename is: ' + filename)
			f = open(directory + filename, "wb")
			f.write(request_page.read())
			f.close()

		# analysis data
		filename = "人口迁出指数 " + chengshi + '.' + startdate + '.' + enddate + '.html'
		f = open(directory + filename, "r")
		s = f.read()
		f.close()
		jobject = json.loads(s.split('(')[1].split(')')[0])
		datetoindex = jobject['data']['list']

		datetodetails = {}
		for date in days:
			filename = directory + u"人口迁出详情 " + chengshi + '.' + date + '.html'
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
