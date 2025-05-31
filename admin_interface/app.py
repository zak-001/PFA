from flask import Flask
from routes import waf_bp, main_bp
from db import metadata, engine



def create_app():
    app = Flask(__name__)
    app.secret_key = '6f2b7f6e72b8d3a4d8c4c013d9b3b73f914e7cdbd33b44a29c02d45c5dd5e12f'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:root@db/flask_db'  # Or your DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        metadata.create_all(engine)
    #from routes import waf_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(waf_bp, url_prefix='/waf')

    return app

