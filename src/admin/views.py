from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView,expose


class MyModelView(ModelView):
    def is_accessible(self):
        return True
    
    
class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return super(MyAdminIndexView,self).index()