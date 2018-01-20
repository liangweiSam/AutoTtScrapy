# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import xlwt, xlrd
from PIL import Image
from urllib import request
import requests
import time
import io
import sys, os
import re
import goods_Scrapy
import shutil


class scrapy(object):


	def __init__(self):
		self.url = 'https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=JTJG'		
		self.js = "arguments[0].scrollIntoView()"


	def iCode(self, driver):
		imgCode = driver.find_element_by_xpath('//img[@class="y-right captcha"]')
		imgUrl = imgCode.get_attribute('src')

		if 'iImg' not in os.listdir():
			os.makedirs('iImg')
		response =  request.urlopen(imgUrl)
		name = str(int(time.time()))
		with open('iImg/%s.jpg' %(name), mode = 'wb') as iImg:
			iImg.write(response.read())

		time.sleep(0.5)
		return 'iImg/%s.jpg' %(name)

		# s = io.BytesIO()
		# s.write(response.read())
		# image = Image.open(s)
		# image.show()
		# return input('请输入验证码:')

	def phoneCode(self, driver, tel, codeN):
		
		mobile = driver.find_element_by_id('mobile')
		captcha1 = driver.find_element_by_id('captcha1')
		code_btn = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/form/div[3]/span')

		mobile.send_keys(tel)
		captcha1.send_keys(codeN)

		time.sleep(1.5)
		code_btn.click()


		# return input('请输入手机验证码:')

	def pressSubmit(self, driver, phoneCode):
		submitBtn = driver.find_elements_by_name('submitBtn')
		code = driver.find_element_by_id('code')
		code.send_keys(phoneCode)

		submitBtn[0].click()
		time.sleep(1)

		self.Work(driver)


	def getInfoFromExcel(self, times):
		data = xlrd.open_workbook('excel/Good%s.xls' %str(times+1))
		table = data.sheets()[0]
		nrows = table.nrows
		urlLinks = []
		descriptions = []
		imgPaths = []

		for i in range(nrows):
			if i == 0:
				continue
			descriptions.append(table.row_values(i)[0])
			urlLinks.append(table.row_values(i)[0])
			imgPaths.append(table.row_values(i)[0])
		return descriptions, urlLinks, imgPaths

	def elementExist(self, driver):
		while True:
			time.sleep(1)
			try:
				element = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[6]/div[2]/div[2]/span/div/div[2]/div[3]/button[1]')
				element.click()
				time.sleep(1)
				return True
				break
				
			except Exception as e:
				return False
				break

	def is_element_exist(self, xpath, driver):
		# s = driver.find_element_by_xpath(xpath)
		# driver.implicitly_wait(1)
		try:
			s = driver.find_element_by_xpath(xpath)
			driver.implicitly_wait(1)
			return True
		except Exception as e:
			return False
		
		# if s == None:
		# # 	print("元素未找到")
		# 	return False
		# else:
		# 	return True
	


	'''

	'''
	def Work(self, driver):
		times = 0
		'''
			上传图片
		'''
		while times < 4:
				current_handle = driver.current_window_handle

				print(times)
				while True:
					if driver.current_url != self.url:
						break

				print('准备开始上传图片')
				driver.get('https://mp.toutiao.com/profile_v2/figure')
				driver.implicitly_wait(1)
				if times > 0:
						# delete = driver.find_element_by_xpath()
					delete_exist = self.is_element_exist('//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div/div/span[2]', driver)
					if delete_exist == True:
						delete = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div/div/span[2]')
						driver.execute_script(self.js, delete)
						delete.click()
				
				upLoadBtn = driver.find_element_by_xpath('//button[@class="tui-btn tui-btn-negative pgc-button"]')
				driver.implicitly_wait(5)
				driver.execute_script(self.js, upLoadBtn)
				time.sleep(2)
				upLoadBtn.click()
				time.sleep(1)

				descriptions, urlLinks, imgPaths = self.getInfoFromExcel(times)
				# goodList = os.listdir('img')
				
				# need imgUrl
				newGoodList = []
				for i in imgPaths:
					a = os.path.abspath(i)
					newGoodList.append(a)
				

				for y in newGoodList[:10]:
					print(y)
					fileInput = driver.find_element_by_xpath('//*[@id="pgc-upload-img"]//input')
					fileInput.send_keys(y)
					time.sleep(0.5)


				while True:
					try:
						enter = driver.find_element_by_xpath('//*[@id="pgc-upload-img"]/div/div[2]/div[2]/button[1]')
						enter.click()
						continue
					except Exception as e:
						break
				time.sleep(0.5)
				print('success to upload data')

				'''
					编辑数据
				'''
				'''
				for i in range(0, len(urlLinks[:10])):
					if urlLinks[i] != '':
						good_info = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[%s]/div[4]/span' %(i+1))
						time.sleep(1)
						driver.execute_script(self.js, good_info)
						good_info.click()

						# need good_link 
						# linkUrls = self.getInfoFromExcel(times)
						good_link = driver.find_element_by_xpath('//*[@id="pgc-add-product"]/div[2]/div/span[1]/input')
						good_link.send_keys(urlLinks[i])

						get_info_btn = driver.find_element_by_xpath('//*[@id="pgc-add-product"]/div[2]/div/span[2]')
						driver.execute_script(self.js, get_info_btn)
						get_info_btn.click()
						time.sleep(0.5)
						# need descrition
						refermence = driver.find_element_by_xpath('//*[@id="pgc-add-product"]/div[3]/div[2]/div[3]/span/textarea')
						refermence.send_keys(descriptions[i])

						time.sleep(1.5)
						btn = driver.find_element_by_xpath('//*[@id="pgc-add-product"]/div[4]/button[1]')
						driver.execute_script(self.js, btn)
						btn.click()
					else:
						refermence_txt = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/textarea')
						driver.execute_script(self.js, refermence_txt)
						refermence_txt.send_keys(descriptions[i])
				'''		
				
				# need title
				data = xlrd.open_workbook('TtExcel/1.xls')
				table = data.sheets()[0]
				nrows = table.nrows
				title_txt = table.row_values(times+1)[0]
				title = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[3]/div[2]/div/input')
				title.send_keys(title_txt)

				auto = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[4]/div[2]/div/div[1]/div/label[3]/div/input')
				driver.execute_script(self.js, auto)
				auto.send_keys(Keys.SPACE)

				time.sleep(0.5)
				# save = driver.find_element_by_link_text('#root > div > div.layout > div.stage > div > div.content-wrapper > div.edit-cell.figure-footer > div.edit-input > div:nth-child(2) > div')
				# //*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[6]/div[2]/div[2]
				
				save = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[6]/div[2]/div[2]')
				driver.execute_script(self.js, save)
				save.click()
				print('success to write data')


				b = self.elementExist(driver)
				if b == True: 
					handles = driver.window_handles
					for handle in handles:
						if handle != current_handle:
							driver.switch_to_window(handle)
						break
					driver.implicitly_wait(5)
					save = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[6]/div[2]/div[2]/div')
					driver.execute_script(self.js, save)
					time.sleep(1)
					save.click()
				times+= 1

				if times == 4:
					self.rmdir()
					time.sleep(5)
					driver.quit()
				time.sleep(2)
				
	def rmdir(self):
		shutil.rmtree('excel')
		shutil.rmtree('img')
		shutil.rmtree('TtExcel')			
		# shutil.rmtree('iImg')



	'''
		登陆，获取driver
	'''
	def Login(self):
		# dcap = dict(DesiredCapabilities.PHANTOMJS)
		# dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2 ")
		# s = goods_Scrapy.goods_Scrapy()
		# s.processUrl()

		driver = webdriver.Chrome(executable_path = 'webdriver/chromedriver.exe')
		driver.get(self.url)
		
		mail_phone = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/ul/li[1]') 
		driver.execute_script(self.js, mail_phone)
		time.sleep(2)
		mail_phone.click()
		# mobile = driver.find_element_by_id('mobile')
		# imgCode = driver.find_element_by_xpath('//img[@class="y-right captcha"]')
		# submitBtn = driver.find_elements_by_name('submitBtn')
		# captcha1 = driver.find_element_by_id('captcha1')
		# code = driver.find_element_by_id('code')

		# mobile.send_keys('17727759494')
		# mobile.send_keys('17727759494')
		# imgUrl = imgCode.get_attribute('src')
		# icodeUrl = self.iCode(imgUrl)
		# self.iCode(imgUrl)
		# captcha1.send_keys(codeN)
		# return icodeUrl

		return driver
		## 
		# phoneCode = self.phoneCode(driver)
		# code.send_keys(phoneCode)
		# time.sleep(1.5)
		# submitBtn[0].click()

		# self.Work(driver)

		# time.sleep(10)
		# driver.quit()


	# def sss(self):
	# 	url = 'https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=JTJG'		
	# 	driver = webdriver.Chrome(executable_path = 'C:/Users/Administrator/Desktop/python/webdriver/chromedriver.exe')
	# 	driver.get(url)
	# 	mail_phone = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/ul/li[7]') 
	# 	print(typemail_phone)


if __name__ == '__main__':
	s = scrapy()
	s.Login()
	# goodList = os.listdir('img')
	# newGoodList = []
	# for i in goodList:
	# 	a = os.path.abspath('img/%s' %(i))
	# 	newGoodList.append(a)
	# print(newGoodList)