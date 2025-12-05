import math
from flask import render_template, request, redirect, jsonify, session
from eapp import app, dao, login, utils
from eapp.models import User, Product

from flask_login import login_user, logout_user



from eapp.admin import admin

@app.route('/')
def index():

    return render_template('index.html',page = math.ceil(dao.count_products()/app.config.get('PAGE_SIZE')),
                            products=dao.get_products(request.args.get('kw'), request.args.get('category_id'),  page=request.args.get('page', 1)),)


@app.route('/login')
def login_view():
    return render_template('login.html')


@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route ('/register', methods=['POST'])
def register_process():
    
    confirm = request.form.get('confirm')
    password = request.form.get('password')

    if confirm != password:

        return render_template('register.html', error='Mật khẩu không khớp!')
    
    avatar = request.files.get('avatar')
    try:
       dao.add_user(request.form.get('fullname'),
                    avatar,
                    request.form.get('username'),
                    password)

    except Exception as ex:
        print(ex)
        return render_template('register.html', error='Hệ thống đang gặp sự cố! Vui lòng thử lại sau.')
    return redirect('/login')


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

@app.route('/api/carts/<int:id>', methods=['put'])
def update_to_cart(id):
    cart = session.get('cart')

    if cart and id in cart:
        quantity = int(request.json.get('quantity'))
        cart[id]['quantity'] = quantity

    session['cart'] = cart
    return jsonify(utils.count_carts(cart))

@app.route('/api/cart', methods=['delete'])
def delete_cart():
    cart = session.get('cart')

    if cart and id in cart: 
        del cart[id]
    session['cart'] = cart

    return jsonify(utils.count_carts(cart))


@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.json 

    cart = session.get('cart')

    if not cart: 
        cart = {}
    
    id = str(data.get('id'))

    name, price = data.get('name'), data.get('price')

    if id in cart:
        cart[id]['quantity'] += 1
    else: 
        cart[id] = {'id': id ,'name': name, 'price': price, 'quantity': 1}

    session['cart'] = cart
    print(cart)

    return jsonify(utils.count_carts(cart))

@app.route('/cart')
def cart_view():
    return render_template('cart.html')

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_categories():
    return {
        'categories': dao.get_categories(),
        'cart_stats': utils.count_carts(session.get('cart'))
    } 

if __name__ == '__main__':
    app.run(debug=True)