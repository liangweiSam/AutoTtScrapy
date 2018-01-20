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
import sys, io, os, re


class ImgScrapy(object):

	def __init__(self):
		pass

	'''
		获取URL
	'''
	def getContent(self):

		browserHeads = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3376.400 QQBrowser/9.6.11924.400'}
		# s = requests.get('http://www.hunter-its.com/m/%s.html' %(random.randint(1, 50)), headers = browserHeads)
		# HTML = etree.HTML(s.content.decode('utf-8'))
		# text = HTML.xpath('//li/a/@href')
		# title = HTML.xpath('//li/a/img/@alt')

		# rootUrl = 'https://www.85814.com'

		# s = requests.get('https://www.85814.com/meinv/sunyunzhumeinv/', headers = browserHeads)
		# HTML = etree.HTML(s.content.decode('utf-8'))
		# content = HTML.xpath('//*[@id="l"]')
		# text = content[0].xpath('//a/@href')
		# title = content[0].xpath('//a/img/@alt')

		s = requests.get(url=r'http://tieba.baidu.com/f?kw=孙允珠&ie=utf-8&tab=good&cid=0&pn=0', headers = browserHeads)
		t = s.content.decode('utf-8').replace('<!--', '').replace('-->', '')
		HTML = etree.HTML(t)
		totalPage = HTML.xpath('//*[@id="frs_list_pager"]/a[11]/@href')

		pn = int(totalPage[0][-4:])/50
		targetHtml = requests.get(url='http://tieba.baidu.com/f?kw=孙允珠&ie=utf-8&tab=good&cid=0&pn=%s' %(random.randint(0, pn)*50), headers = browserHeads)
		HTML2 = etree.HTML(targetHtml.content.decode('utf-8').replace('<!--', '').replace('-->', ''))
		hrefs = HTML2.xpath('//*[@id="thread_list"]//a[@class="j_th_tit "]/@href')
		titles = HTML2.xpath('//*[@id="thread_list"]//a[@class="j_th_tit "]')

		rootAddress = 'http://tieba.baidu.com'
		# assert 1==0, titles

		if 'TtExcel' not in os.listdir():
			os.makedirs('TtExcel')

		workBook = xlwt.Workbook()
		workSheet = workBook.add_sheet('Goods')
		workSheet.write(0, 0, 'url')

		index = random.randint(0, len(hrefs))
		if(index > len(hrefs) - 4):
			index = index-4

		urls = []
		t = 1
		for i in range(index, index+4):
			urls.append(rootAddress+hrefs[i])
			workSheet.write(t, 0, titles[i].text)
			# urls.append(rootUrl+text[i])
			t+= 1

		workBook.save('TtExcel/%s.xls' %(1))

		return urls

	'''
		获取图片
	'''
	def getImg(self):
		urls = self.getContent()
		browserHeads = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3376.400 QQBrowser/9.6.11924.400'}

		if 'img' not in os.listdir():
			os.makedirs('img')

		if 'excel' not in os.listdir():
			os.makedirs('excel')

		for x in urls:

			workBook = xlwt.Workbook()
			workSheet = workBook.add_sheet('Goods')
			workSheet.write(0, 0, 'img')
			good_name = self.nameFgood()
			

			ImgHtml = requests.get(url = x, headers = browserHeads)
			result = etree.HTML(ImgHtml.content.decode('utf-8').replace('<!--', '').replace('-->', ''))
			imgs = result.xpath('//img[@class="BDE_Image"]')
			finalImgs = []

			for y in range(0, len(imgs)):
				if(len(imgs[y].xpath('@height')) > 0):
					finalImgs.append(imgs[y])

			fiveHun = 500
			threeHun = 300
			maxHeight = 0

			i = 1
			for y in range(0, len(finalImgs)):
				if(i<3):
					maxHeight = threeHun
				else:
					maxHeight = fiveHun

				if int(finalImgs[y].xpath('@height')[0]) > maxHeight:
					with open('img/%s_%s.jpg' %(good_name, i), mode = 'wb') as img:
						workSheet.write(i, 0, 'img/%s_%s.jpg' %(good_name, i))
						img.write(requests.get(finalImgs[y].xpath('@src')[0], headers = browserHeads).content)
						time.sleep(0.5)
					i+= 1

				
					
			# https://www.85814.com/tu/201608/169190.html
			# https://www.85814.com/tu/201608/169190_2.html

			# for y in range(1, 7):
			# 	ImgHtml = requests.get(url = x[0:-5]+'_%s.html' %(y), headers = browserHeads)
			# 	result = etree.HTML(ImgHtml.text)
			# 	imgUrl = result.xpath('//*[@id="d"]/dd/p/img/@src')

			# 	with open('img/%s_%s.jpg' %(good_name, i), mode = 'wb') as img:
			# 		workSheet.write(i, 0, 'img/%s_%s.jpg' %(good_name, i))
			# 		imgResponse = requests.get(imgUrl[0], headers = browserHeads)
			# 		img.write(imgResponse.content)
			# 		time.sleep(0.1)

			# for y in range(2, 7):
			# 	ImgHtml = requests.get(url = x[0:-6]+'%s.html' %(y), headers = browserHeads)
			# 	result = etree.HTML(ImgHtml.text)
			# 	imgUrl = result.xpath('//*[@id="content"]/a/img/@src')
			# 	with open('img/%s_%s.jpg' %(good_name, i), mode = 'wb') as img:
			# 		workSheet.write(i, 0, 'img/%s_%s.jpg' %(good_name, i))
			# 		imgResponse = requests.get(imgUrl[0])
			# 		img.write(imgResponse.content)
			# 		time.sleep(0.1)
			# 	

			workBook.save('excel/%s.xls' %(good_name[:-1]))	

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
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
	ImgScrapy = ImgScrapy()
	ImgScrapy.getImg()