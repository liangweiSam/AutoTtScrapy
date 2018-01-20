# -*- coding:utf-8 -*-
import requests
import json
import xlwt, xlrd
from PIL import Image
from lxml import etree
import os
import re
import time
import random
import datetime
import shutil


class goods_Scrapy(object):

	def __init__(self):
		pass

	def processDate(self, date):
		if len(str(date)) == 1:
			return '0%s' %date
		else:
			return date


	def getUrl(self):
		s = requests.Session()

		submitUrl = 'http://www.51taojinge.com/user/insert.php'
		firstUrl = 'http://www.51taojinge.com/toutiao_comm.php?tag=news_fashion&1=1&page=1'

		browserHeads = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
		Login_Data = {'phone' :'13148394312', 'password' : 'temaidaren', 'submit' : 'login'}
		s.post(submitUrl, headers = browserHeads, data = Login_Data)
		time.sleep(3)
		# response = s.get(firstUrl, headers = browserHeads)
		# html = etree.HTML(response.text)
		# total = re.search(r'.*/(\d+)',html.xpath('//b')[1].text)
		# http://www.51taojinge.com/toutiao_comm.php?tag=news_fashion&count=&str_time=2017-11-02+23%3A20%3A00&end_time=2017-11-03+23%3A20%3A00&orderY=%E8%AF%B7%E9%80%89%E6%8B%A9%E6%8E%92%E5%BA%8F%E6%96%B9%E5%BC%8F
		
		current_year = datetime.datetime.now().year
		current_month = datetime.datetime.now().month
		current_day = datetime.datetime.now().day

		#月份
		month = self.processDate(random.randint(1, 12))
		if int(month) > int(current_month):
			month = current_month
		
		#日
		date = random.randint(1, 30)

		if int(date) > int(current_day-2):
			date = current_day-2

		sdate = self.processDate(date)
		edate = self.processDate(date+1)
		
		str_time = '2017-%s-%s+0:00:00' %(month, sdate)
		end_time = '2017-%s-%s+0:00:00' %(month, edate)
		print('%s %s'%(str_time, end_time))
		# dateUrl = 'http://www.51taojinge.com/toutiao_comm.php?tag=news_fashion&count=&str_time=%s&end_time=%s&orderY=请选择排序方式' %(str_time, end_time)
		# goodsSet = s.get(dateUrl, headers = browserHeads)
		# setHtml = etree.HTML(goodsSet.text)
		# total = re.search(r'.*/(\d+)',setHtml.xpath('//b')[1].text)
		# print(setHtml.xpath('//b')[1].text)
		page = random.randint(1, 100)
		print('%s' %(page))
		finalUrl = 'http://www.51taojinge.com/toutiao_comm.php?tag=news_fashion&count=&%s=str_time&end_time=%s&orderY=请选择排序方式&page=%s' %(str_time, end_time, page)
		finalSet = s.get(finalUrl, headers = browserHeads)
		finalHtml = etree.HTML(finalSet.text)
		# print(finalSet.url)
		# print(setHtml.xpath('//tbody//tr/'))
		if 'TtExcel' not in os.listdir():
			os.makedirs('TtExcel')

		workBook = xlwt.Workbook()
		workSheet = workBook.add_sheet('Goods')
		workSheet.write(0, 0, '#')
		workSheet.write(0, 1, 'title')
		workSheet.write(0, 2, 'platform')
		workSheet.write(0, 3, 'good\'s URL')
		workSheet.col(1).width = 10000
		workSheet.col(2).width = 50000
		workSheet.col(3).width = 50000

		i = 1
		for x in range(0, 5):
			tr = finalHtml.xpath('//tbody//tr')[x]
			workSheet.write(i, 0, '%s' %(i))
			workSheet.write(i, 1, tr.xpath('td[1]/a[1]')[0].text)
			if len(tr.xpath('td[6]/span')) >0:
				workSheet.write(i, 2, tr.xpath('td[6]/span')[0].text)
				# print(tr.xpath('td[6]/span')[0].text+'\n')
			else:
				workSheet.write(i, 2, '')
				# print('无平台')
			workSheet.write(i, 3, tr.xpath('td[1]/a/@href')[0])

			i+= 1

		workBook.save('TtExcel/%s.xls' %(1))
		

	def getInfoFromExcel(self):
		data = xlrd.open_workbook('Ttexcel/1.xls')
		table = data.sheets()[0]
		nrows = table.nrows

		urlLinks = []
		for i in range(nrows):
			if i == 0:
				continue
			urlLinks.append(table.row_values(i)[3])
		return urlLinks		
	

	def getUrlFrompage(self):
		authors = xldr.open_workbook('authors.xls')
		table = authors.sheets()[0]

		urlLinks = []
		

	def processUrl(self):

		self.getUrl()

		urlLinks =  self.getInfoFromExcel()

		for url in urlLinks:
				phoneHeads = {'User-Agent' : 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'}

				response = requests.get(url, headers = phoneHeads)
				HTML = etree.HTML(response.text)
				text = HTML.xpath('//textarea[@id="gallery-data-textarea"]')
				resultSet = json.loads(text[0].text)
				workBook = xlwt.Workbook()
				workSheet = workBook.add_sheet('Goods')
				workSheet.write(0, 0, '#')
				workSheet.write(0, 1, 'Name')
				workSheet.write(0, 2, 'description')
				workSheet.write(0, 3, 'good\'s URL')
				workSheet.write(0, 4, 'img path')
				workSheet.col(1).width = 10000
				workSheet.col(2).width = 40000
				workSheet.col(3).width = 40000
				workSheet.col(4).width = 20000

				typeJudge = resultSet
				# print(typeJudge)

				# assert 1+1==3
				if isinstance(typeJudge, dict):

					newResultSet = []

					for i in range(1, len(typeJudge.keys())+1):
						name = re.search(r"'name': '(.877777777777777777777777777777777777777777777777777777777777777777777777777777777+)',?", str(typeJudge['%s' %i]))
						description = re.search(r"'description': '(.+)',?", str(typeJudge['%s' %i]))
						real_url = re.search(r"'real_url': '(.+)',?", str(typeJudge['%s' %i]))
						img = re.search(r"'img': '(.+)',?", str(typeJudge['%s' %i]),  flags = re.M)
						if img == None:
							img = re.search(r"'location': '(.+)',?", str(typeJudge['%s' %i]), flags = re.M)

						if name != None and description != None and real_url != None and img != None:
							print('%s' %i)
							print('%s\n%s\n%s\n%s\n' %(name.group(1).split(r"'")[0], description.group(1).split(r"'")[0], real_url.group(1).split(r"'")[0], img.group(1).split(r"'")[0]))
							
							good = {'name': name.group(1).split(r"'")[0], 'description': description.group(1).split(r"'")[0], 'real_url': real_url.group(1).split(r"'")[0], 'img': img.group(1).split(r"'")[0]}
							newResultSet.append(good)

					resultSet = newResultSet	

				# 'name': '新款高领中袖印花针织衫'	
				if 'img' not in os.listdir():
					os.makedirs('img')

				if 'excel' not in os.listdir():
					os.makedirs('excel')

				good_name = self.nameFgood()
				# 判定文件夹内的名字，然后再进行命名
				i = 1
				for good in resultSet:
					workSheet.write(i, 0, '%s' %(i))
					workSheet.write(i, 1, good.get('name', ''))			
					workSheet.write(i, 2, good.get('description', ''))
					workSheet.write(i, 3, good.get('real_url', ''))
					
					if good.get('img', '0') != '0':
						with open('img/%s_%s.jpg' %(good_name, i), mode = 'wb') as img:
							workSheet.write(i, 4, 'img/%s_%s.jpg' %(good_name, i))
							imgResponse = requests.get(good['img'])
							img.write(imgResponse.content)
							time.sleep(0.1)
							self.cropImg('img/%s_%s.jpg' %(good_name, i))
							time.sleep(0.1)
					i+= 1
					
				workBook.save('excel/%s.xls' %(good_name[:-1]))

	def cropImg(self, path):
		with Image.open(path) as im:
			width, height = im.size
			# print(im.size)
			box = (0, 0, width, height-30)
			im = im.crop(box)
			im.save(path, 'JPEG')

	def nameFgood(self):
		s = set()

		if len(os.listdir('img')) == 0:
			good_Name = 'Good1_'
		else:
			imgNames = os.listdir('img')
			for i in imgNames:
				good_Id = re.search(r'Good(\d{1,5})', i)
				s.add(good_Id.group(1))

			sList = list(s)
			sList.sort()
			
			good_Name = 'Good%d_' %(int(sList[-1])+1)

		return good_Name


if __name__ == '__main__':
	s = goods_Scrapy()
	s.processUrl()
	# s.processUrl('https://temai.snssdk.com/article/feed/index?id=4255859&subscribe=5569547953&source_type=6&content_type=2&create_user_id=2849&classify=2&adid=__AID__&tt_group_id=6481373671800701454')
	# if 'img' not in os.listdir():
	# 	os.makedirs('img')

	# with open('img/ss.jpg', mode = 'wb') as img:
	# 			response = requests.get('https://p3.pstatp.com/large/403a00020120990f6215?imageView2/2/w/800/h/800')
	# 			img.write(response.content)