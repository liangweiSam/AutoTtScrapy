# -*- coding:utf-8 -*-
from tkinter import *
import tkinter as tk
# import tkinter.messagebox as messagebox
import scrapy
import goods_Scrapy
import ImgScrapy
from PIL import Image, ImageTk 

class Application(object):

	def __init__(self):
		pass
		# self.grid()
		# self.root = tk.Tk()
		# self.createWidgets()
		# self.tel = ''

	def createWidgets(self):
		
		# self.p = ttk.Progressbar(parent, orient = "horizontal", length=200, mode="indeterminate", value=200.0)
		# self.p.grid(row = 1)
		# g = goods_Scrapy.goods_Scrapy()
		# g.processUrl()

		g = ImgScrapy.ImgScrapy()
		g.getImg()
		
		root = tk.Tk()
		self.root = root

		s = scrapy.scrapy()
		driver = s.Login()		
		# driver = self.getDriver()

		self.tel = Label(self.root, text='手机号')
		self.tel.grid(row = 3, column = 1)
		self.telInput = Text(self.root, height = 1, width = 30)
		self.telInput.grid(row = 3, column = 2, padx=10,pady=10 , sticky=W+E+N+S)
		self.icode = Label(self.root, text='验证码')
		self.icode.grid(row = 5, column = 1)
		self.icodeInput = Text(self.root, height = 1, width = 30)
		self.icodeInput.grid(row = 5, column = 2, padx=10, pady=10, sticky=W+E+N+S)

		path = s.iCode(driver)
		im = Image.open(path)
		tkimg = ImageTk.PhotoImage(im)   # 执行此函数之前， Tk() 必须已经实例化。
		self.icodeImgLabel = tk.Label(self.root, image = tkimg)
		self.icodeImgLabel.grid(row = 5, column = 3)

		self.telCode = Label(self.root, text='手机验证码')
		self.telCode.grid(row = 6, column = 1, padx=10, pady=10, sticky=W+E+N+S)
		self.telCodeInput = Text(self.root, height = 1, width = 30)
		self.telCodeInput.grid(row = 6, column = 2, padx=10, pady=10, sticky=W+E+N+S)
		self.telCodebutton = Button(self.root, text = '获取手机验证码', command =lambda :s.phoneCode(driver, self.telInput.get('0.0','end'), self.icodeInput.get('0.0','end')))
		self.telCodebutton.grid(row = 6, column = 3, padx=10, pady=10, sticky=W+E+N+S)

		self.loginButton = Button(self.root, text = '登录', command = lambda :s.pressSubmit(driver, self.telCodeInput.get('0.0','end')))
		self.loginButton.grid(row = 7, column = 2, padx=10, pady=10, sticky=W+E+N+S)
		root.mainloop()
		# self.button = Button(self, text = '开始采集', command=self.excuteScrapy)
		# self.button.pack(pady = 2)

		# self.authorLabel = Label(self, text='作者：LL_SAM')
		# self.authorLabel.pack(pady = 5)





if  __name__ == '__main__':
	app = Application()

	app.createWidgets()






