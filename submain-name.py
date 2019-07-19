#!/usr/bin/env python
#-*-coding:utf-8-*-
import requests
import sys
from Queue import Queue
import threading
import re
from bs4 import BeautifulSoup as bs
import os
import socket
from multiprocessing.dummy import Pool as ThreadPool
import time

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',}
class Submain(threading.Thread):
	def __init__(self,queue):
		threading.Thread.__init__(self)
		self._queue = queue
	def run(self):
		while not self._queue.empty():
			url= self._queue.get()
			try:
				self.Getsubmain(url)
			except Exception as e:
				pass
	def Getsubmain(self,url):
		r = requests.get(url=url,headers=headers,timeout=1.3)
		soup = bs(r.content,'html.parser')
		urls = soup.find_all(name='a',attrs={'data-click':re.compile(('.')),'class':None,'data-is-main-url':None})
		for i in urls:
			result= requests.get(url=i['href'],headers=headers)
			if result.status_code == 200:
				tmp=result.url.split('/')
				submainUrl=tmp[2]+'\n'
				this_ip=self.Getip(tmp[2])
				with open(filename) as file:
					if submainUrl not in file.read():
						sys.stdout.write('\033[5;32m'+'[Yes]'+'['+this_ip+']'+'\t'+submainUrl)
						f = open(filename,"a+")
						f.write(submainUrl)
						f.close()
	def Getip(self,url):
		result = socket.getaddrinfo(url, None)
		with open(ipfilename) as file:
			if result[0][4][0] not in file.read():
				f2 = open(ipfilename,'a+')
				f2.write(result[0][4][0]+"\n")
				f2.close()
		return result[0][4][0]	

def main(keywords,threadsnum):
	queue = Queue()
	for i in range(0,760,10):
		l = 'https://www.baidu.com/s?wd='+'inurl:'+keywords+'&pn='+str(i)
		queue.put(l)
	threads=[]
	threadsCount=int(threadsnum)
	for i in range(threadsCount):
		threads.append(Submain(queue))
	for j in threads:
		j.start()
	for j in threads:
		j.join()
	print '\033[0m'+"The log file is in:"+filename
	print  '\033[0m'+"The log file is in:"+path+"/ip.txt"
if __name__=='__main__':
		if len(sys.argv) != 3:
			print "Enter:python %s url threads" %(sys.argv[0])
			print'eg:python %s baidu.com 50' %(sys.argv[0])
			sys.exit(-1)
		else:
			filename = "log/"+sys.argv[1]+"/submain-name.txt"
			path="log/"+sys.argv[1]
			isExists=os.path.exists(path)
			if not isExists:
				os.makedirs(path) 
			ipfilename=path+"/ip.txt"
			f = open(ipfilename,"w+")
			f.close()	
			f = open(filename,"w+")
			f.close()
			print "Find the following subdomains:"
			main(sys.argv[1],sys.argv[2])