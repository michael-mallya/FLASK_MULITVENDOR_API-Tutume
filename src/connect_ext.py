from .extension import db,bcrypt,jwt,migrate,session
# from .admin.routes import admin
# from .admin.register_model import register_model



# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user.id


# # Register a callback function that loads a user from your database whenever
# # a protected route is accessed. This should return any python object on a
# # successful lookup, or None if the lookup failed for any reason (for example
# # if the user has been deleted from the database).
# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     return User.query.filter_by(id=identity).one_or_none()



def connect_ext(app)->None:
    db.init_app(app)
    bcrypt.init_app(app)
    # admin.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app,db)
    app.config['SESSION_SQLALCHEMY'] = db
    session.init_app(app)
 
    # register_model(admin)
    
    
