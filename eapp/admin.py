from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from eapp import app, db
from eapp.models import Category, Product 
from flask_login import logout_user, current_user

from flask import redirect

admin = Admin(app, name='SaleApp Admin')


class AuthenticatedView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.role.name == 'ADMIN'

class ProductView(AuthenticatedView):
    pass
    

class CategoryView(AuthenticatedView):
    pass


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')
    def is_accessible(self) -> bool:
        return current_user.is_authenticated


admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))


