# -*- coding: utf-8 -*-
from flask import Flask,render_template,request
from apps import app
import urllib2
from bs4 import BeautifulSoup


class scrolled_data(object):
	def __init__(self, url):
		self.url = url
		self.source = urllib2.urlopen(self.url).read().decode('utf-8', 'ignore')
		self.soup = BeautifulSoup(self.source)

#app = Flask(__name__)
@app.route('/',methods = ['GET','POST'])
def get():
	return render_template("index.html")

@app.route("/crawl", methods = ['GET','POST'])
def crawl():
	dcurl = "http://gall.dcinside.com/board/lists/?id="+request.form['id']+"&page="+request.form['page']
	
	data = scrolled_data(dcurl)
	context = data.soup.findAll('td', attrs={'class': 't_subject'})
	result = ""
	for each in context:
		result += each.a.string + "<br>"

	return result
#if __name__ == "__main__":
#	app.run()