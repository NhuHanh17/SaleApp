from eapp.models import Category, Product, User
import hashlib
from eapp import app

def get_categories():
    return Category.query.all()

def get_products(kw=None, category_id=None, page=1):
    query = Product.query
    if kw:
        query = query.filter(Product.name.contains(kw))

    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if page:
        page= int(page)

        page_size=app.config.get('PAGE_SIZE', 10)
        start = (page-1)*page_size
        query = query.slice(start, start + page_size)


    return query.all()



def count_products():
    return Product.query.count()



def get_user_by_id(user_id):
    return User.query.get(int(user_id))

def auth_user(username, password):
    pwd=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter_by(username=username.strip(),
                                 password=pwd).first()


    
