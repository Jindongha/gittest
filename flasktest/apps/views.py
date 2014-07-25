from flask import render_template, Flask, request
#from apps import app

app = Flask(__name__)
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	herf = None
	post = None
	naver_herf = None
	google_herf = None
	daum_herf = None
	if request.args:
		get = request.args['text_get']
		naver_herf = "http://search.naver.com/search.naver?where=nexearch&query="+get+"&sm=top_hty&fbm=1&ie=utf8"
		google_herf = "https://www.google.co.kr/?gfe_rd=cr&ei=twrNU5HxNqSL8QeCloDAAQ&gws_rd=ssl#newwindow=1&q="+get		
		daum_herf = "http://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&o=&q="+get

	if request.form:
		post = request.form['text_post']

	return render_template("index.html", naver_get = naver_herf, variable_post = post, google_get = google_herf, daum_get = daum_herf)

if __name__ == "__main__":
	app.run(port = 5013)