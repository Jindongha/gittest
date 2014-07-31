# -*- coding: utf-8 -*-
# all the imports

from flask import request, redirect, url_for,render_template
from apps import app
from database import Database

dataStorage = Database()

@app.route('/', methods=['GET', 'POST'])
def show_entries():
	entries = dataStorage.out()
	return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	
	storage={}
	storage['num'] = dataStorage.num
	storage['count'] = 0
	storage['title'] = request.form['title']
	storage['contents'] = request.form['contents']
	dataStorage.put(storage)
	dataStorage.num += 1
	return redirect(url_for('show_entries'))

@app.route('/delete/<idx>', methods=['GET'])
def delete_entry(idx):
	for item in dataStorage.database:
		if int(idx) == item['num']:
			dataStorage.database.remove(item)
			break

	return redirect(url_for('show_entries'))

@app.route('/plus/<idx>', methods=['GET'])
def plus_entry(idx):
	for data in dataStorage.database:
		if int(idx) == data['num']:
			data['count'] += 1
			break
	return redirect(url_for('show_entries'))

@app.route('/minus/<idx>', methods=['GET'])
def minus_entry(idx):
	for data in dataStorage.database:
		if int(idx) == data['num']:
			data['count'] -= 1
			break
	return redirect(url_for('show_entries'))


@app.route('/upsort', methods=['GET'])
def up_sort_entry():
	dataStorage.database = sorted(dataStorage.database, key=lambda list: list['count'], reverse=True)
	return redirect(url_for('show_entries'))

@app.route('/downsort', methods=['GET'])
def down_sort_entry():
	dataStorage.database = sorted(dataStorage.database, key=lambda list: list['count'], reverse=False)
	return redirect(url_for('show_entries'))


@app.route('/upload/<idx>', methods=['GET'])
def upload_entry(idx):
	for data in dataStorage.database:
		if int(idx) == data['num']:
			data['title'] = request.args['title']
			data['contents'] = request.args['contents']
			break

	return redirect(url_for('show_entries'))

