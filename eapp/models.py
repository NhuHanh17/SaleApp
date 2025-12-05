from eapp import app, db
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, Enum
from sqlalchemy.orm import relationship
from flask_login import UserMixin 
from enum import Enum as PyEnum
import hashlib


class UserRole(PyEnum):
    ADMIN = 1
    USER = 2


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    name = Column(String(200), nullable=False)
    products = relationship('Product', backref='category', lazy=True)
    
    def __str__(self):
        return self.name

class Product(BaseModel):
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    image = Column(String(500),default='default.jpg',)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    
    def __str__(self):
        return self.name
    

class User(BaseModel, UserMixin):
    username = Column(String(150), unique=True, nullable=False)
    avatar = Column(String(500), default='https://thumbs.dreamstime.com/b/default-avatar-profile-icon-vector-social-media-user-photo-183042379.jpg')
    password = Column(String(200), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    
    def __str__(self):
        return self.username
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        pwd=str(hashlib.md5('111111'.encode('utf-8')).hexdigest())
        u = User(username='admin', password=pwd, role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()

        category ={'Điện thoại', 'Laptop', 'Máy tính bảng'}
        for c in category: 
            cate = Category(name=c)
            db.session.add(cate)
        db.session.commit()


        products = [{
            "name": "iPhone 7 Plus",
            "description": "Apple, 32GB, RAM: 3GB, iOS13",
            "price": 17000000,
            "image":
                "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
            "category_id": 1
        }, {
            "name": "iPad Pro 2020",
            "description": "Apple, 128GB, RAM: 6GB",
            "price": 37000000,
            "image":
                "https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg",
            "category_id": 2
        }, {
            "name": "Galaxy Note 10 Plus",
            "description": "Samsung, 64GB, RAM: 6GB",
            "price": 24000000,
            "image":
                "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
            "category_id": 1
        }
        ]

        for p in products:
            pro = Product(**p)
            db.session.add(pro)
        db.session.commit()