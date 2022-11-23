from flask import Flask
import pyodbc

cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-4KB59VJ\SQLEXPRESS;"
            "Database=UST;"
            "Trusted_Connection=yes;")
cnxn = pyodbc.connect(cnxn_str)
cursor = cnxn.cursor()

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-4KB59VJ\SQLEXPRESS/UST'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app