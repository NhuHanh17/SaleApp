import math
from flask import render_template, request, redirect
from eapp import app, dao, login
from eapp.models import User, Product

from flask_login import login_user, logout_user



from eapp.admin import admin

@app.route('/')
def index():

    return render_template('index.html',page = math.ceil(dao.count_products()/app.config.get('PAGE_SIZE')),
                            products=dao.get_products(request.args.get('kw'), request.args.get('category_id'),  page=request.args.get('page', 1)),)


@app.context_processor
def common_categories():
    return {'categories': dao.get_categories()} 


@app.route('/login')
def login_view():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/login', methods=['POST'])
def login_process():
    username = request.form['username']
    password = request.form['password']
    
    user = dao.auth_user(username, password)
    if user:
        login_user(user)

    next = request.args.get('next')

    return redirect(next if next else '/')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)