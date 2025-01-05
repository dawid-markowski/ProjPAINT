from flask_admin.contrib.sqla import ModelView
from app.models import User, Part
from flask_login import current_user
from flask_admin import AdminIndexView
from flask import render_template
from app import admin, db
#Trzeba dodać kolejne Modele które dziedziczą z ModelView i decydować co może widzieć admin i co może wyświetlać

class ModelView(ModelView):
    def is_accessible(self):
        # Sprawdza, czy użytkownik jest zalogowany i jest administratorem
        return current_user.is_authenticated and current_user.is_admin

class MyHomeView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin



admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Part,db.session))

