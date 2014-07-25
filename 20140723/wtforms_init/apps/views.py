from flask import render_template, Flask, request
from apps import app

from flaskext import wtf
from flaskext.wtf import Form, TextField, TextAreaField, \
SubmitField, validators, ValidationError

# app = Flask(__name__)

class ContactForm(Form):
	name = TextField("Name",  [validators.Required("Please enter your name.")])
	email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter valid email address.")])
	subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
	message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
	submit = SubmitField("Send")

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = ContactForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('index.html', form=form)
		else:
			return "Nice to meet you, " + form.name.data + "!"
	else :
		return render_template('index.html', form=form)

# if __name__ == "__main__":
#     app.run()