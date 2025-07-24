import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin


db = SQLAlchemy()
migrate = Migrate()
lm = LoginManager()


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)


def create_app():
    app = Flask(__name__)

    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    caminho_db = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.getenv('DB_PATH'))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{caminho_db}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    db.init_app(app)
    migrate.init_app(app, db)
    lm.init_app(app)
    
    
    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp) 

    
    @lm.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app


app = create_app()