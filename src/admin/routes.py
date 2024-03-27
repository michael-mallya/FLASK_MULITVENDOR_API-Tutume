from flask import Blueprint, current_app
from flask_admin import Admin
from src.admin.views import MyAdminIndexView

admin = Admin(name="Ecomerce Api", template_mode="bootstrap4",index_view=MyAdminIndexView(
    name="Dashboard",menu_icon_type="fa",menu_icon_value="fa-dashboard"
))
#Init admin




