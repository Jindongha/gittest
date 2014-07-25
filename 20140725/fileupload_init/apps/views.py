from flask import render_template, Flask, request, url_for
from apps import app
from google.appengine.ext import db



class Photo(db.Model):
	photo = db.BlobProperty()
#app = Flask(__name__)
@app.route('/')
@app.route('/index')
def index():
	
	return render_template("upload.html")

@app.route('/upload',methods = ['POST'])
def upload_db():
	urls = []
	post_data = request.files['photo']

	filestream = post_data.read()

	upload_data = Photo()
	upload_data.photo = db.Blob(filestream)
	upload_data.put()
	url = url_for("shows",key = upload_data.key())
	
	urls.append(url)
	
	return render_template("upload.html", urls = urls)

@app.route('/show/<key>')
def shows(key):
	uploaded_data = db.get(key)
	return app.response_class(uploaded_data.photo)
#if __name__ == "__main__":
#	app.run()