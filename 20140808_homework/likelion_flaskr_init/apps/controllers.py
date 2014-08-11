# -*- coding: utf-8 -*-
from flask import render_template, request, flash, url_for, redirect
from apps.models import	Article,Comment
from sqlalchemy import desc
from apps import app, db

@app.route('/', methods=['GET'])
def article_list():
	context = {}
	context['article_list'] = Article.query.all()
	return render_template("home.html", context=context, active_tab='timeline')

@app.route('/create', methods=['GET','POST'])
def article_create():
	if request.method == 'GET':
		return render_template("article/create.html",active_tab = 'article_create')
	elif request.method == 'POST':
		article_data  = request.form
		article = Article(
			title = article_data['title'],
			author = article_data['author'],
			category = article_data['category'],
			content = article_data['content']
			)
		db.session.add(article)
		db.session.commit()
		flash(u'게시글이 작성되었습니다..','success')
		return render_template("home.html",active_tab = 'article_create')

@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    article = Article.query.get(id)
    if request.method == 'GET':
        return render_template('article/update.html', article=article)
    elif request.method == 'POST':

        article_data = request.form

        article.title = article_data['title']
        article.author = article_data['author']
        article.category = article_data['category']
        article.content = article_data['content']

        db.session.commit()

        flash(u'게시글이 수정되었습니다.', 'success')
        return redirect(url_for('article_detail', id=id))

@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
	article = Article.query.get(id)
	comments = article.comments.order_by(desc(Comment.date_created)).all()
	return render_template('article/detail.html', article=article, comments = comments)

@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
	if request.method == 'GET':
		return render_template("article/delete.html", article_id = id)
	elif request.method == 'POST':

		article_data = request.form
		article = Article.query.get(article_data['article_id'])
		
		db.session.delete(article)
		db.session.commit()

		flash(u'게시글을 삭제하였습니다.', 'success')
		return redirect(url_for('article_list'))


#
# @comment controllers
#
@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
    if request.method =='GET':
        return render_template('comment/create.html')
    elif request.method == 'POST':
		comment_data  = request.form
		comment = Comment(
			article = Article.query.get(article_id),
			author = comment_data['author'],
			email = comment_data['email'],
			content = comment_data['content'],
			password = comment_data['password'],
			like = 0
			)
		db.session.add(comment)
		db.session.commit()
		flash(u'댓글이 작성되었습니다..','success')
		return redirect(url_for('article_detail', id=article_id))

@app.route('/article/like/<int:comment_id>, <int:article_id>', methods=['GET', 'POST'])
def comment_like(comment_id, article_id):
	comment = Comment.query.get(comment_id)
	comment.like += 1
	db.session.commit()
	return redirect(url_for('article_detail', id=article_id))

@app.route('/comment/delete/<int:comment_id>, <int:article_id>', methods=['GET', 'POST'])
def comment_delete(comment_id, article_id):
	if request.method == 'GET':
		return render_template("comment/delete.html", comment_id = comment_id)
	elif request.method == 'POST':

		comment_data = request.form
		comment = Comment.query.get(comment_id)
		if comment.password == str(comment_data['password']):
			db.session.delete(comment)
			db.session.commit()

			flash(u'댓글을 삭제하였습니다.', 'success')
			article = Article.query.get(article_id)
			comments = article.comments.order_by(desc(Comment.date_created)).all()
			return render_template("article/detail.html", article=article, comments = comments)
		else:
			flash(u'비밀번호가 일치하지 않습니다..', 'success')
			article = Article.query.get(article_id)
			comments = article.comments.order_by(desc(Comment.date_created)).all()
			return render_template("article/detail.html", article=article, comments = comments)

#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500